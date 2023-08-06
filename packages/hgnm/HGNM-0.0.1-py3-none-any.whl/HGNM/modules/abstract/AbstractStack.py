import abc
import copy
import torch.nn as nn
from typing import Optional

from src.HGNM.util.Types import *
from src.HGNM.modules.common.hmpn_util import noop


class AbstractStack(nn.Module, abc.ABC):
    """
    Message Passing module that acts on both node and edge features used for observation graphs.
    Internally stacks multiple instances of MessagePassingBlock.
    """

    def __init__(self,
                 latent_dimension: int,
                 stack_config: ConfigDict, 
                 use_global_features: bool):
        """
        Args:
            latent_dimension: Dimensionality of the latent space
            stack_config: Dictionary specifying the way that the gnn base should look like.
                num_blocks: how many blocks this stack should have
                use_residual_connections: if the blocks should use residual connections
            use_global_features: Whether the stack should use global features
        """
        super().__init__()
        self._num_blocks: int = stack_config.get("num_blocks")
        self._use_residual_connections: bool = stack_config.get("use_residual_connections")
        self._latent_dimension: int = latent_dimension

        self._old_graph: Optional[Batch] = None

        if self._use_residual_connections:
            self.maybe_store_old_graph = self._store_old_graph
            self.maybe_add_residual = self._add_residual
        else:
            self.maybe_store_old_graph = noop
            self.maybe_add_residual = noop
        self._message_passing_blocks: nn.ModuleList = None

        if use_global_features:
            self._maybe_add_global_residual = self._add_global_residual
            self._maybe_store_global = self._store_global
        else:
            self._maybe_add_global_residual = lambda *args, **kwargs: None
            self._maybe_store_global = lambda *args, **kwargs: None

        if stack_config.get("use_layer_norm"):
            self._maybe_layer_norm = self._layer_norm
        else:
            self._maybe_layer_norm = lambda *args, **kwargs: None

        if stack_config.get("use_layer_norm") and use_global_features:
            self._maybe_global_layer_norm = self._global_layer_norm
            self._global_layer_norms = nn.ModuleList([nn.LayerNorm(normalized_shape=latent_dimension)
                                                      for _ in range(self._num_blocks)])
        else:
            self._maybe_global_layer_norm = lambda *args, **kwargs: None
            self._global_layer_norms = None

    def _store_old_graph(self, graph: Batch):
        raise NotImplementedError("'_store_old_graph' not implemented for AbstractStack")

    def _add_residual(self, graph: Batch):
        raise NotImplementedError("'_add_residual' not implemented for AbstractStack")

    def _add_global_residual(self, graph):
        """
        Since the global features are the same for homogeneous and heterogeneous graphs, we can
        implement the residual connection here.
        Args:
            graph:

        Returns:

        """
        graph.__setattr__("u", graph.u + self._old_graph["u"])

    def _store_global(self, graph):
        """
        Since the global features are the same for homogeneous and heterogeneous graphs, we can
        implement storage operation for them here
        Args:
            graph:

        Returns:

        """
        self._old_graph["u"] = graph.u

    def _layer_norm(self, graph: Batch, layer_position: int) -> None:
        """
        Computes the layer norm for the node and edge features of the graph.
        Args:
            graph:
            layer_position: Current layer position, used because we want to use different layer norms for each layer

        Returns:

        """
        raise NotImplementedError("'_layer_norm' not implemented for AbstractStack")

    def _global_layer_norm(self, graph: Batch, layer_position: int) -> None:
        """
        Since the global features are the same for homogeneous and heterogeneous graphs, we can
        implement the layer norm for global features here.
        Args:
            graph:
            layer_position: Current layer position, used because we want to use different layer norms for each layer

        Returns:

        """
        graph.__setattr__("u", self._global_layer_norms[layer_position](graph.u))

    @property
    def num_blocks(self) -> int:
        """
        How many blocks this stack is composed of.
        """
        return self._num_blocks

    @property
    def use_residual_connections(self) -> bool:
        """
        Whether this stack makes use of residual connections or not
        Returns:

        """
        return self._use_residual_connections

    @property
    def latent_dimension(self) -> int:
        """
        Dimensionality of the features that are handled in this stack
        Returns:

        """
        return self._latent_dimension

    def forward(self, graph: Batch) -> None:
        """
        Computes the forward pass for this homogeneous or heterogeneous message passing stack.
        Updates node, edge and global features (new_node_features, new_edge_features, new_global_features)
        for each type as a tuple

        Args: graph of type torch_geometric.data.Batch containing homogeneous or heterogeneous graphs

        Returns: None, in-place operation
        """
        for layer_position, message_passing_block in enumerate(self._message_passing_blocks):
            self.maybe_store_old_graph(graph=graph)
            message_passing_block(graph=graph)
            self.maybe_add_residual(graph=graph)
            self._maybe_layer_norm(graph=graph, layer_position=layer_position)

    def __repr__(self):
        if self._message_passing_blocks:
            return f"{self.__class__.__name__}(\n" \
                   f" use_residual_connections={self.use_residual_connections},\n" \
                   f" num_message_passing_blocks={self.num_blocks},\n" \
                   f" first_block={self._message_passing_blocks[0]}\n"
        else:
            return f"{self.__class__.__name__}(\n" \
                   f" use_residual_connections={self.use_residual_connections},\n" \
                   f" num_message_passing_blocks={self.num_blocks}\n"
