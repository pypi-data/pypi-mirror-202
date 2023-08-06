import torch.nn as nn
import torch
from typing import Callable

from src.HGNM.modules.abstract.AbstractModules import AbstractMetaModule
from src.HGNM.util.Types import *
from src.HGNM.util.Keys import AGGR_AGGR



class HeterogeneousMetaModule(AbstractMetaModule):
    """
    Base class for the heterogeneous modules used in the GNN.
    They are used for updating node-, edge-, and global features.
    """

    def __init__(self, *,
                 mlps: nn.ModuleDict,
                 scatter_reducers: Union[Callable, List[Callable]],
                 use_global_features: bool,
                 latent_dimension: int,
                 outer_aggregation: str):
        """
        Args:
            mlps: Dictionary of {{{node, edge}_type: List[MLP]} of MLPs to use for each respective node/edge.
                Implemented as nn.ModuleDict/nn.ModuleList to correctly register parameters
            scatter_reducers: How to aggregate over the nodes/edges/globals. Can for example be [torch.scatter_mean]
            use_global_features: Whether global features are used
        """
        super().__init__(scatter_reducers=scatter_reducers)
        self._mlps = mlps
        if use_global_features:
            self._maybe_global = self._concat_global
        else:
            self._maybe_global = lambda *args, **kwargs: args[0]

        self.latent_dimension = latent_dimension  # latent_dimension

        if outer_aggregation == AGGR_AGGR:
            self._maybe_outer_aggregate = self._outer_aggregate
        else:
            self._maybe_outer_aggregate = lambda *args, **kwargs: args[0]

    def _outer_aggregate(self, features: torch.Tensor, num_types: int) -> torch.Tensor:
        """
        On aggr(aggr()) we want to aggregate all the (edge-)features we have concatenated dimension-wise, i.e., do an
          outer aggregation
        Args:
            features: features of shape (#nodes, num_incoming_edge_types*latent_dimension*n_scatter_ops)
                of inner-aggregated edge features per node
            num_types: Number of edge types that feed into this node

        Returns:
            aggregated features of shape (#nodes, latent_dimension*n_scatter_ops*n_scatter_ops)
            num_incoming_edge_types has been reduced n_scatter_ops times.

        """

        aggregation_dimension = self.latent_dimension * self._n_scatter_reducers
        indices = torch.arange(aggregation_dimension, dtype=torch.int64).repeat(num_types)
        # counterintuitive: dim_size gets multiplied by n_scatter_ops internally due to the concat op.
        # so this is correct.
        ret = self.multiscatter(features=features, indices=indices, dim=1, dim_size=aggregation_dimension)
        return ret

    def _concat_global(self, *args, **kwargs):
        raise NotImplementedError(f"Module {type(self)} needs to implement _concat_global(self,*args, **kwargs)")


class HeterogeneousEdgeModule(HeterogeneousMetaModule):
    def forward(self, graph: Batch):
        """
        Compute edge updates for the edges of the Module for heterogeneous graphs
        Args:
            graph: HeteroData object of pytorch geometric. Represents a (batch of) of heterogeneous graph(s)
        Returns: An updated representation of the edge attributes for all edge_types
        """
        for position, (edge_type, edge_store) in enumerate(zip(graph.edge_types, graph.edge_stores)):
            edge_attr = edge_store.get("edge_attr")
            edge_indices = edge_store.get("edge_index")
            source_indices, dest_indices = edge_indices

            source_node_type, _, dest_node_type = edge_type
            source_node_index = graph.node_types.index(source_node_type)
            dest_node_index = graph.node_types.index(dest_node_type)

            edge_source_nodes = graph.node_stores[source_node_index]["x"][source_indices]
            edge_dest_nodes = graph.node_stores[dest_node_index]["x"][dest_indices]

            # concatenate everything
            aggregated_features = torch.cat([edge_source_nodes, edge_dest_nodes, edge_attr], 1)
            aggregated_features = self._maybe_global(aggregated_features, graph, source_node_type, source_indices)

            edge_store["edge_attr"] = self._mlps["".join(edge_type)][0](aggregated_features)
            # todo this assumes that there is only a single edge_mlp of output size latent_dimension in the mlp list.
            #   instead, we want to extend this to use an arbitrary number of mlps whose sum of output dimensions
            #   needs to equal the latent dimension.

    def _concat_global(self, features, graph, source_node_type, source_indices):
        indices = graph[source_node_type].batch
        global_features = graph.u[indices[source_indices]]
        return torch.cat([features, global_features], 1)


class HeterogeneousNodeModule(HeterogeneousMetaModule):
    def __init__(self, *,
                 mlps: nn.ModuleDict,
                 num_edge_types: Dict[str, int],
                 latent_dimension: int,
                 outer_aggregation: str,
                 scatter_reducers: List[Callable],
                 use_global_features: bool):
        """
        Args:
            mlps: Dictionary of {node_type: List[MLP]} of MLPs to use for each respective node
                Implemented as nn.ModuleDict/nn.ModuleList to correctly register parameters
            num_edge_types: How many edge types feed into each kind of node type
            latent_dimension: Dimensionality of the latent space. Also corresponds to the dimension of each node/edge
              message
            outer_aggregation: scatter reduce to use over different incoming edge types.
            scatter_reducers: How to aggregate over the nodes/edges/globals. Can for example be [torch.scatter_mean]
        """

        super().__init__(mlps=mlps,
                         scatter_reducers=scatter_reducers,
                         use_global_features=use_global_features,
                         latent_dimension=latent_dimension,
                         outer_aggregation=outer_aggregation)

        self.in_features = {node_type: mlp_list[0].in_features
                            for node_type, mlp_list in mlps.items()}  # in_features
        self.num_edge_types = num_edge_types

    def forward(self, graph: Batch):
        """
        Compute updates for each node feature vector as x_i' = f2(x_i, agg_j f1(e_ij, x_j), u),
        where f1 and f2 are MLPs
            graph: HeteroData object of pytorch geometric. Represents a (batch of) of heterogeneous graph(s)
        Returns: An updated representation of the edge attributes for all edge_types
        """
        for position, (node_type, node_store) in enumerate(zip(graph.node_types, graph.node_stores)):
            node_features = node_store.get("x")
            num_nodes = node_features.shape[0]
            n_edge_features = self.num_edge_types[node_type] * self.latent_dimension * self._n_scatter_reducers

            # define empty tensor that will store edge features
            all_edge_features = torch.zeros(size=(num_nodes, n_edge_features),
                                            device=node_features.device)

            relevant_edge_ids = [position
                                 for position, (_, _, dest_node_type) in enumerate(graph.edge_types)
                                 if dest_node_type == node_type]
            # look for all edges that have the current node type as destination

            edge_increment = self.latent_dimension * self._n_scatter_reducers
            for pos, edge_index in enumerate(relevant_edge_ids):
                edge_features = graph.edge_stores[edge_index].get("edge_attr")
                _, dest_indices = graph.edge_stores[edge_index].get("edge_index")
                aggr_features = self.multiscatter(features=edge_features, indices=dest_indices, dim=0,
                                                  dim_size=num_nodes)
                # aggr_features now has shape (num_nodes, latent_dimension * n_scatter_reducers)
                # this inner loop is across edge types
                all_edge_features[:, pos * edge_increment:(pos + 1) * edge_increment] = aggr_features
            all_edge_features = self._maybe_outer_aggregate(all_edge_features, num_types=self.num_edge_types[node_type])

            # we need to repeat that with each type of aggregation. aggr_features

            aggregated_features = torch.cat([node_features, all_edge_features], 1)
            aggregated_features = self._maybe_global(aggregated_features, graph, node_type)
            # update
            node_store["x"] = self._mlps[node_type][0](aggregated_features)
            # todo this assumes that there is only a single edge_mlp of output size latent_dimension in the mlp list.
            #   instead, we want to extend this to use an arbitrary number of mlps whose sum of output dimensions
            #   needs to equal the latent dimension.

    def _concat_global(self, features, graph, node_type):
        batch = graph[node_type].batch
        return torch.cat([features, graph.u[batch]], 1)


class HeterogeneousGlobalModule(HeterogeneousMetaModule):
    def forward(self, graph: Batch):
        """
        computes the forward pass for the global module
        Args:
            graph: of type torch_geometric.data.Batch

        Returns: None, in-place operation

        """
        edge_feature_list = []  # stores the reduced edge features per edge type
        node_feature_list = []  # stores the reduced node features per node type
        for edge_type, edge_store in zip(graph.edge_types, graph.edge_stores):
            edge_attr = edge_store.get("edge_attr")
            edge_indices = edge_store.get("edge_index")
            source_indices, _ = edge_indices
            source_node_type, _, _ = edge_type
            indices = graph[source_node_type].batch
            # indices assigns each node to a graph in the batch of graphs. We use this to aggregate over the edges
            # by querying this for the source node of each edge
            reduced_edge_features = self.multiscatter(features=edge_attr,
                                                      indices=indices[source_indices],  # query source node of each edge
                                                      dim=0,
                                                      dim_size=graph.u.shape[0])
            edge_feature_list.append(reduced_edge_features)

        for node_type, node_store in zip(graph.node_types, graph.node_stores):
            node_attr = node_store.get("x")
            reduced_node_features = self.multiscatter(features=node_attr,
                                                      indices=graph[node_type].batch,
                                                      dim=0,
                                                      dim_size=graph.u.shape[0])
            node_feature_list.append(reduced_node_features)

        aggregated_edge_features = torch.cat(edge_feature_list, 1)
        aggregated_node_features = torch.cat(node_feature_list, 1)

        num_edge_types = len(graph.edge_types)
        num_node_types = len(graph.node_types)
        aggregated_edge_features = self._maybe_outer_aggregate(aggregated_edge_features, num_edge_types)
        aggregated_node_features = self._maybe_outer_aggregate(aggregated_node_features, num_node_types)
        aggregated_features = torch.cat([aggregated_node_features, aggregated_edge_features, graph.u], 1)

        graph.u = self._mlps["u"](aggregated_features)
