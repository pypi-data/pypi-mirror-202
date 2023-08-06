import torch
import torch_geometric
from typing import Optional, Tuple

from src.HGNM.util.Types import *
from src.HGNM.util.Keys import AGENT
from src.HGNM.modules.common.hmpn_util import noop, unpack_heterogeneous_features
from src.HGNM.modules.common.hmpn_util import get_create_copy
from src.HGNM.modules.homogeneous.HomogeneousMessagePassingBase import HomogeneousMessagePassingBase


class MockHeteroBase(HomogeneousMessagePassingBase):
    """
    Calls like a heterogeneous base but uses a homogeneous base with broad input features that get sparsely populated.
    """

    def __init__(self, *, in_node_features: Dict[str, int],
                 in_edge_features: Dict[Tuple[str, str, str], int],
                 in_global_features: Optional[int],
                 latent_dimension: int,
                 scatter_reduce_strs: List[str],
                 stack_config: ConfigDict,
                 embedding_config: ConfigDict,
                 output_type: str = "features",
                 create_graph_copy: bool = True,
                 assert_graph_shapes: bool = True,
                 device: Optional[torch.device] = None,
                 agent_node_type: str = AGENT):
        """
                Arguments:
            in_node_features:
                Dictionary {node_type: #node_features} of node_types and their input sizes for a heterogeneous graph.
                Node features may have size 0, in which case an empty input graph of the appropriate shape/batch_size
                is expected and the initial embeddings are learned constants
            in_edge_features:
                Dictionary {edge_type: #edge_features} of edge_types and their input sizes for a heterogeneous graph.
                Edge features may have size 0, in which case an empty input graph of the appropriate shape/batch_size
                is expected and the initial embeddings are learned constants
            in_global_features:
                If None, no global features will be used (and no GlobalModules created)
                May have size 0, in which case the initial values are a learned constant. This expects (empty) global
                 input tensors and will use the GlobalModule
            latent_dimension:
                Latent dimension of the network. All modules internally operate with latent vectors of this dimension
            scatter_reduce_strs:
                Names of the scatter reduce to use to aggregate messages of the same type.
                Can be any list of "sum", "mean", "max", "min", "std"
            stack_config:
                Configuration of the stack of GNN blocks
            embedding_config:
                Configuration of the embedding stack (can be empty by choosing None, resulting in linear embeddings).
            output_type:
                Either "features" or "graph". Specifies whether the output of the forward pass is a graph
                or a tuple of (node_features, edge_features, global_features)
            create_graph_copy:
                If True, a copy of the input graph is created and modified in-place.
                If False, the input graph is modified in-place.
            assert_graph_shapes:
                If True, the input graph is checked for consistency with the input shapes.
                If False, the input graph is not checked for consistency with the input shapes.
            device:
                Device to use for the module. If None, the default device is used.
            agent_node_type:
                Node type of the agent. Used to determine the node type of the agent.
        """
        if isinstance(scatter_reduce_strs, str):
            scatter_reduce_strs = [scatter_reduce_strs]

        self.homo_node_features = 0
        self.homo_edge_features = 0
        self.node_feature_dims = [0]
        self.edge_feature_dims = [0]
        for node_type in in_node_features.keys():
            self.homo_node_features += in_node_features[node_type]
            self.node_feature_dims.append(self.homo_node_features)
        for edge_type in in_edge_features.keys():
            self.homo_edge_features += in_edge_features[edge_type]
            self.edge_feature_dims.append(self.homo_edge_features)
        self.in_node_features = in_node_features
        self.in_edge_features = in_edge_features
        super().__init__(in_node_features=self.homo_node_features,
                         in_edge_features=self.homo_edge_features,
                         in_global_features=in_global_features,
                         latent_dimension=latent_dimension,
                         scatter_reduce_strs=scatter_reduce_strs,
                         stack_config=stack_config,
                         embedding_config=embedding_config,
                         output_type=output_type,  # if we do not call the super.forward(), this works
                         create_graph_copy=create_graph_copy,  # if we do not call the super.forward(), this is fine
                         assert_graph_shapes=assert_graph_shapes,
                         device=device,
                         agent_node_type=agent_node_type)

        self.maybe_create_heterogeneous_copy: Callable = get_create_copy(create_graph_copy=create_graph_copy)

        if not create_graph_copy:
            self.maybe_overwrite_graph = lambda x, y: y
        else:
            self.maybe_overwrite_graph = lambda x, y: x

    def forward(self, graph: Batch):
        """
        Overwrites the forward method of the base class because the input needs
        to be transformed to a homogeneous graph. The forward method of the base class is called in this method.

        Args:
            graph: A Batch object of HeteroData.

        Returns: either a modified graph or a tuple of (node_features, edge_features, global_features),
        depending on the configuration of the class at initialization.
        """
        self.maybe_assertions(graph)
        graph = self.maybe_create_copy(graph)

        homo_graph = self._to_homogeneous(graph)
        self.input_embeddings(homo_graph)
        self.message_passing_stack(homo_graph)
        graph = self._to_heterogeneous(homo_graph)
        return self.maybe_transform_output(graph)

    def _to_homogeneous(self, graph: Batch):
        """
        Converts a heterogeneous graph to a homogeneous graph. The resulting homogeneous graph has
        a node feature dimension of the sum over all node types' feature dimensions of the heterogeneous graph,
        and an edge feature dimension of the sum over all edge types' feature dimensions of the heterogeneous graph.

        All feature inputs of the homogeneous graph are initialized to zero.

        Then slices of those features are filled with the heterogeneous features, such that nodes of equal corresponding
        heterogeneous type have the same slice filled. This is done for all node and edge types.

        Finally, the connectivity of the homogeneous graph is calculated.
        Args:
            graph: A Batch of HeteroData.

        Returns: A Batch of HomoData.

        """
        # calculating feature dimensions
        node_count = 0
        edge_count = 0
        for node_type in graph.node_types:
            node_count += graph[node_type].x.shape[0]
        for edge_type in graph.edge_types:
            edge_count += graph[edge_type].edge_attr.shape[0]

        # initializing features to zero
        x = torch.zeros(size=(node_count, self.homo_node_features))
        edge_attr = torch.zeros(size=(edge_count, self.homo_edge_features))

        # needed for constructing homogeneous edges and later restoring heterogeneous graph
        node_mapping = {}
        # needed for later restoring heterogeneous graph
        edge_mapping = {}
        # filling slices of node features with heterogeneous node features
        it = 0
        for i, node_type in enumerate(graph.node_types):
            # it is the index of the first feature of the current node type
            # it2-1 is the index of the last feature of the current node type
            it2 = it + graph[node_type].x.shape[0]
            # node_feature_dims contains the indices in the feature vector of the homogeneous graph for this node type
            x[it:it2, self.node_feature_dims[i]:self.node_feature_dims[i + 1]] = graph[node_type].x
            # node_mapping[node_type] contains the list of indices in the homogeneous node features that
            # correspond to this node type.
            node_mapping[node_type] = list(range(it, it2))
            it = it2
        # filling slices of edge features with heterogeneous edge features
        it = 0
        for i, edge_type in enumerate(graph.edge_types):
            # it is the index of the first feature of the current edge type
            # it2-1 is the index of the last feature of the current edge type
            it2 = it + graph[edge_type].edge_attr.shape[0]
            # edge_feature_dims contains the slice locations for this edge type in the feature vector
            # of the homogeneous graph
            edge_attr[it:it2, self.edge_feature_dims[i]:self.edge_feature_dims[i + 1]] = graph[edge_type].edge_attr
            # edge_mapping[edge_type] contains the list of indices in the homogeneous edge features that
            # correspond to this edge type.
            edge_mapping[edge_type] = list(range(it, it2))
            it = it2

        # calculating connectivity
        edge_index = []
        # edge_dict is just the original edge_index of the heterogeneous graph so that it can be directly restored.
        edge_dict = {}
        for edge_type in graph.edge_types:
            source, _, target = edge_type
            edge_dict[edge_type] = graph[edge_type].edge_index
            # iterating over all edges of this type
            for i in range(graph[edge_type].edge_index.shape[1]):
                # source_index is the index of the source node in the homogeneous graph
                source_index = node_mapping[source][graph[edge_type].edge_index[0, i]]
                # target_index is the index of the target node in the homogeneous graph
                target_index = node_mapping[target][graph[edge_type].edge_index[1, i]]
                edge_index.append([source_index, target_index])
        edge_index = torch.LongTensor(edge_index).T

        # calculating batch argument
        batch_list = []
        hetero_batch = {}
        for node_type in graph.node_types:
            hetero_batch[node_type] = graph[node_type].batch
            batch_list.append(graph[node_type].batch)
        batch = torch.cat(batch_list)

        # constructing the homogeneous graph from the calculated data
        ret = torch_geometric.data.Data(
            x=x,
            edge_attr=edge_attr,
            edge_index=edge_index
        )
        ret.batch = batch

        # copying global features if they exist
        if hasattr(graph, "u"):
            ret.u = graph.u

        # adding information about the heterogeneous graph such that it can be reconstructed
        ret.hetero_info = {
            "node_mapping": node_mapping,
            "edge_mapping": edge_mapping,
            "edge_index": edge_dict,
            "batch": hetero_batch
        }
        return ret

    def _to_heterogeneous(self, graph: Batch):
        """
        Converts a homogeneous graph that was created by _to_homogeneous to a heterogeneous graph.
        Args:
            graph: A Batch of HomoData. needs to be created by _to_homogeneous.

        Returns: A Batch of HeteroData.

        """
        info = graph.hetero_info

        node_mapping = info["node_mapping"]
        edge_mapping = info["edge_mapping"]
        batch_info = info["batch"]
        edge_index_info = info["edge_index"]
        ret = torch_geometric.data.HeteroData()
        for node_type in batch_info.keys():
            ret[node_type].batch = batch_info[node_type]
            # todo bug(s) with batch_info:
            #    will create a list of tensors instead of a single tensor,
            #    currently creates a list over all node types for each node type
            ret[node_type].x = graph.x[node_mapping[node_type][0]: node_mapping[node_type][-1] + 1]

        for edge_type in edge_index_info.keys():
            ret[edge_type].edge_index = edge_index_info[edge_type]
            ret[edge_type].edge_attr = graph.edge_attr[edge_mapping[edge_type][0]: edge_mapping[edge_type][-1] + 1]

        if hasattr(graph, "u"):
            ret.u = graph.u

        return ret

    def transform_to_features(self, graph: HeteroData) -> HeteroData:
        """
        Unpacking important data from heterogeneous graphs.

        Params:
            graph – The input heterogeneous observation

        Returns:
            Tuple of (edge_features, edge_index, node_features, global_features, batch)

        """
        return unpack_heterogeneous_features(graph)
