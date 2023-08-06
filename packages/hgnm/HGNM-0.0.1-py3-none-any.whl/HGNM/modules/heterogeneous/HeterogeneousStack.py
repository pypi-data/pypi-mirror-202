from torch import nn
from typing import Callable, Tuple

from src.HGNM.modules.common.hmpn_util import count_in_node_features
from src.HGNM.util.Types import *
from src.HGNM.modules.abstract.AbstractStack import AbstractStack
from src.HGNM.modules.heterogeneous.HeterogeneousBlock import HeterogeneousBlock
from src.HGNM.modules.common.LatentMLP import LatentMLP
from src.HGNM.util.Keys import AGGR_AGGR


class HeterogeneousStack(AbstractStack):
    """
    Message Passing module that acts on both node and edge features.
    Internally stacks multiple instances of MessagePassingBlocks.
    This implementation is used for heterogeneous observation graphs.
    """

    def __init__(self, in_node_features: Dict[str, int],
                 in_edge_features: Dict[Tuple[str, str, str], int],
                 latent_dimension: int,
                 scatter_reducers: List[Callable],
                 stack_config: ConfigDict,
                 use_global_features: bool = False):
        """
        Builds a heterogeneous message passing stack
        Args:
            in_node_features:
                Dictionary {node_type: #node_features} of node_types and their input sizes for a heterogeneous graph.
                Node features may have size 0, in which case an empty input graph of the appropriate shape/batch_size
                is expected and the initial embeddings are learned constants
            in_edge_features:
                Dictionary {edge_type: #edge_features} of edge_types and their input sizes for a heterogeneous graph.
                Edge features may have size 0, in which case an empty input graph of the appropriate shape/batch_size
                is expected and the initial embeddings are learned constants
            stack_config: Dictionary specifying the way that the message passing network base should look like.
                num_blocks: how many blocks this stack should have
                use_residual_connections: if the blocks should use residual connections. If True,
              the original inputs will be added to the outputs.
            latent_dimension: Dimensionality of the latent space of the MLPs in the network
            scatter_reducers: List of Functions to use to aggregate message for nodes (and potentially global information).
                Must be permutation invariant. Examples include sum, mean, min, std, max. Uses the torch.scatter
                implementation of these functions
            use_global_features: Wether to use global features.
        """
        super().__init__(latent_dimension=latent_dimension, stack_config=stack_config,
                         use_global_features=use_global_features)
        # todo we do not need the node/edge values for the computation, so we should probably simplify the data
        #  structure here accordingly. However, we have to make sure that we do not shuffle around the sizes

        # todo different weighting mechanisms
        n_scatter_ops = len(scatter_reducers)
        # compute number of incoming edge types and thus input features per node type
        in_node_features, num_edge_types = count_in_node_features(
            in_edge_features=in_edge_features,
            in_node_features=in_node_features,
            latent_dimension=latent_dimension,
            outer_aggregation=stack_config.get("outer_aggregation"),
            n_scatter_ops=n_scatter_ops)

        mlp_config = stack_config.get("mlp")
        self._message_passing_blocks = nn.ModuleList([])
        for _ in range(self._num_blocks):
            # todo
            #  the HeterogeneousBlock expects a dictionary over node/edge types of lists of MLPs to use for that type
            #  We use a list of MLPs instead of a simple MLP to enable partial weight sharing, i.e., to enable
            #  sharing some but not all weights across different modules. If no weights are shared, these lists have
            #  a size of 1
            if use_global_features:
                global_features = latent_dimension
                if stack_config.get("outer_aggregation") == AGGR_AGGR:
                    global_in_features = latent_dimension * (n_scatter_ops * n_scatter_ops * 2 + 1)
                    # node types and edge types reduced.
                else:
                    edge_types_count = len(in_edge_features.keys())
                    node_types_count = len(in_node_features.keys())

                    global_in_features = latent_dimension * (
                            ((edge_types_count + node_types_count) * n_scatter_ops) + 1)
                global_mlp = LatentMLP(in_features=global_in_features,
                                       latent_dimension=latent_dimension,
                                       config=mlp_config)
            else:
                global_mlp = None
                global_features = 0

            node_mlps = nn.ModuleDict({node_name: nn.ModuleList([
                LatentMLP(
                    in_features=in_features + global_features,
                    latent_dimension=latent_dimension,
                    config=mlp_config)]) for node_name, in_features in in_node_features.items()})

            edge_mlps = nn.ModuleDict(
                {"".join(edge_name): nn.ModuleList([
                    LatentMLP(
                        in_features=3 * latent_dimension + global_features,
                        latent_dimension=latent_dimension,
                        config=mlp_config)]) for edge_name in in_edge_features.keys()})

            self._message_passing_blocks.append(HeterogeneousBlock(edge_mlps=edge_mlps,
                                                                   node_mlps=node_mlps,
                                                                   num_edge_types=num_edge_types,
                                                                   stack_config=stack_config,
                                                                   latent_dimension=latent_dimension,
                                                                   scatter_reducers=scatter_reducers,
                                                                   use_global_features=use_global_features,
                                                                   global_mlp=global_mlp)
                                                )

        if stack_config.get("use_layer_norm"):
            self._node_layer_norms = nn.ModuleList(
                [nn.ModuleDict({node_name: nn.LayerNorm(normalized_shape=latent_dimension)
                                for node_name in in_node_features.keys()})
                 for _ in range(self._num_blocks)])
            self._edge_layer_norms = nn.ModuleList(
                [nn.ModuleDict({"".join(edge_name): nn.LayerNorm(normalized_shape=latent_dimension)
                                for edge_name in in_edge_features.keys()})
                 for _ in range(self._num_blocks)])

        else:
            self._node_layer_norms = None
            self._edge_layer_norms = None

    def _store_old_graph(self, graph: Batch):
        """
        Copies the graph so that it can be added to the new one in order to do inplace operations.
        Args:
            graph: of type pytorch_geometric.data.Batch
        Returns:
            Nothing

        """
        self._old_graph = {"node_stores": [{"x": node_store_dict.get("x")}
                                           for node_store_dict in graph.node_stores],
                           "edge_stores": [{"edge_attr": edge_store_dict.get("edge_attr")}
                                           for edge_store_dict in graph.edge_stores]}
        self._maybe_store_global(graph)

    def _store_global(self, graph):
        self._old_graph["u"] = graph.u

    def _add_residual(self, graph: Batch):
        """
        Add output features of previous block to the current feature output in order to create residual connections
        Args:
            graph: of type pytorch_geometric.data.Batch

        Returns:
            Nothing
        """
        for position, node_type in enumerate(graph.node_types):
            graph.node_stores[position]["x"] = graph.node_stores[position]["x"] + \
                                               self._old_graph.get("node_stores")[position]["x"]

        for position, edge_type in enumerate(graph.edge_types):
            graph.edge_stores[position]["edge_attr"] = graph.edge_stores[position]["edge_attr"] + \
                                                       self._old_graph.get("edge_stores")[position]["edge_attr"]

        self._maybe_add_global_residual(graph)

    def _layer_norm(self, graph: Batch, layer_position: int) -> None:
        """
        Applies layer normalization to the output of the message passing block for all node and edge types
        Args:
            graph:
            layer_position:

        Returns:

        """
        for position, node_type in enumerate(graph.node_types):
            graph.node_stores[position]["x"] = self._node_layer_norms[layer_position][node_type](
                graph.node_stores[position]["x"])

        for position, edge_type in enumerate(graph.edge_types):
            graph.edge_stores[position]["edge_attr"] = self._edge_layer_norms[layer_position]["".join(edge_type)](
                graph.edge_stores[position]["edge_attr"])
        self._maybe_global_layer_norm(graph=graph, layer_position=layer_position)
