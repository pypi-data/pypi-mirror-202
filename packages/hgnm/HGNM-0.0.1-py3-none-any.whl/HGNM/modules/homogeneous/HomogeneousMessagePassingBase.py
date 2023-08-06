import torch
from typing import Optional

# from modules.abstract.AbstractGraphAssertions import AbstractGraphAssertions
from src.HGNM.util.Types import *
from src.HGNM.util.Keys import AGENT
from src.HGNM.modules.homogeneous.HomogeneousInputEmbedding import HomogeneousInputEmbedding
from src.HGNM.modules.homogeneous.HomogeneousStack import HomogeneousStack
from src.HGNM.modules.homogeneous.HomogeneousGraphAssertions import HomogeneousGraphAssertions
from src.HGNM.modules.abstract.AbstractMessagePassingBase import AbstractMessagePassingBase
from src.HGNM.modules.common.hmpn_util import noop, unpack_homogeneous_features


class HomogeneousMessagePassingBase(AbstractMessagePassingBase):
    """
    # todo write nice comments

        Graph Neural Network (GNN) Base module processes the graph observations of the environment.
        It uses a stack of GNN Blocks. Each block defines a single GNN pass.
    """

    def __init__(self, *, 
                 in_node_features: int,
                 in_edge_features: int,
                 in_global_features: Optional[int],
                 latent_dimension: int,
                 scatter_reduce_strs: Union[List[str], str],
                 stack_config: ConfigDict, # not in AbstractMessagePassingBase
                 embedding_config: ConfigDict, # not in AbstractMessagePassingBase
                 output_type: str = "features",
                 create_graph_copy: bool = True,
                 assert_graph_shapes: bool = True,
                 device: Optional[torch.device] = None,
                 agent_node_type: str = AGENT):
        """
        Args:
            in_node_features:
                Node feature input size for a homogeneous graph.
                Node features may have size 0, in which case an empty input graph of the appropriate shape/batch_size
                is expected and the initial embeddings are learned constants
            in_edge_features:
                Edge feature input size for a homogeneous graph.
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
                Can be multiple of "sum", "mean", "max", "min", "std"
                e.g. ["sum","max"]
            stack_config:
                Configuration of the stack of GNN blocks. See the documentation of the stack for more information.
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
        super().__init__(in_node_features=in_node_features,
                         in_edge_features=in_edge_features,
                         in_global_features=in_global_features,
                         latent_dimension=latent_dimension,
                         scatter_reduce_strs=scatter_reduce_strs,
                         output_type=output_type,
                         create_graph_copy=create_graph_copy,
                         assert_graph_shapes=assert_graph_shapes,
                         device=device,
                         agent_node_type=agent_node_type
                         )

        use_global_features = in_global_features is not None

        self.input_embeddings = HomogeneousInputEmbedding(in_node_features=in_node_features,
                                                          in_edge_features=in_edge_features,
                                                          in_global_features=in_global_features,
                                                          latent_dimension=latent_dimension,
                                                          embedding_config=embedding_config,
                                                          device=device)

        # create message passing stack
        self.message_passing_stack = HomogeneousStack(stack_config=stack_config,
                                                      latent_dimension=latent_dimension,
                                                      scatter_reducers=self._scatter_reducers,
                                                      use_global_features=use_global_features)

    def _get_assertions(self): # removed annotation  -> Type[HomogeneousGraphAssertions]
        return HomogeneousGraphAssertions

    @staticmethod
    def _get_input_embeddings(): # removed annotation -> Type[HomogeneousInputEmbedding]
        return HomogeneousInputEmbedding

    @staticmethod
    def _get_message_passing_stack(): # removed annotation -> Type[HomogeneousStack]
        return HomogeneousStack

    def transform_to_features(self, graph: Batch) -> Batch:
        # todo needs cleanup
        return unpack_homogeneous_features(graph, agent_node_type=self._agent_node_type)
