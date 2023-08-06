from torch import nn
from typing import Callable

from src.HGNM.util.Types import *
from src.HGNM.modules.abstract.AbstractStack import AbstractStack
from src.HGNM.modules.homogeneous.HomogeneousBlock import HomogeneousBlock


class HomogeneousStack(AbstractStack):
    """
    Message Passing module that acts on both node and edge features.
    Internally stacks multiple instances of MessagePassingBlocks.
    This implementation is used for homogeneous observation graphs.
    """

    def __init__(self,
                 stack_config: ConfigDict,
                 latent_dimension: int,
                 scatter_reducers: List[Callable],
                 use_global_features: bool = False):
        """
        Args:
            stack_config: Dictionary specifying the way that the message passing network base should look like.
                num_blocks: how many blocks this stack should have
                use_residual_connections: if the blocks should use residual connections. If True,
              the original inputs will be added to the outputs.
            latent_dimension: the latent dimension of all vectors used in this stack
            scatter_reducers: functions of torch_scatter: min,max,mean,std,etc, as a list of functions
            use_global_features: whether to use global features
        """
        super().__init__(latent_dimension=latent_dimension, 
                         stack_config=stack_config,
                         use_global_features=use_global_features)
        # todo need to initialize (shared) MLPs here and give to the blocks
        self._message_passing_blocks = nn.ModuleList([HomogeneousBlock(stack_config=stack_config,
                                                                       latent_dimension=latent_dimension,
                                                                       scatter_reducers=scatter_reducers,
                                                                       use_global_features=use_global_features)
                                                      for _ in range(self._num_blocks)])

        if stack_config.get("use_layer_norm"):
            self._node_layer_norms = nn.ModuleList([nn.LayerNorm(normalized_shape=latent_dimension)
                                                    for _ in range(self._num_blocks)])
            self._edge_layer_norms = nn.ModuleList([nn.LayerNorm(normalized_shape=latent_dimension)
                                                    for _ in range(self._num_blocks)])

        else:
            self._node_layer_norms = None
            self._edge_layer_norms = None

    def _store_old_graph(self, graph: Batch):
        self._old_graph = {"x": graph.x,
                           "edge_attr": graph.edge_attr}
        self._maybe_store_global(graph)

    def _add_residual(self, graph: Batch):
        graph.__setattr__("x", graph.x + self._old_graph["x"])
        graph.__setattr__("edge_attr", graph.edge_attr + self._old_graph["edge_attr"])
        self._maybe_add_global_residual(graph)

    def _layer_norm(self, graph: Batch, layer_position: int) -> None:
        graph.__setattr__("x", self._node_layer_norms[layer_position](graph.x))
        graph.__setattr__("edge_attr", self._edge_layer_norms[layer_position](graph.edge_attr))
        self._maybe_global_layer_norm(graph=graph, layer_position=layer_position)
