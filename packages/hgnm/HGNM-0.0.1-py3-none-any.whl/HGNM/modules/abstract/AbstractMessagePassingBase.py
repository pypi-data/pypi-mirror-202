import abc
import torch
# from torch import nn
from typing import Optional, Tuple, Callable

from src.HGNM.util.Types import *
from src.HGNM.modules.common.hmpn_util import get_scatter_reducers, get_create_copy
from src.HGNM.modules.common.hmpn_util import noop
from src.HGNM.modules.abstract.AbstractGraphAssertions import AbstractGraphAssertions
from src.HGNM.modules.abstract.AbstractInputEmbedding import AbstractInputEmbedding
from src.HGNM.modules.abstract.AbstractStack import AbstractStack
from src.HGNM.util.Keys import AGENT


class AbstractMessagePassingBase(torch.nn.Module, abc.ABC):
    """
    The Message Passing base contains the feature embedding as well as all the message passing blocks.
    Its output is a graph or a tuple of node_features, edge_features, global_features, batch_indices with
    feature dimension of latent_dimension.
    """
    def __init__(self, *,
                 in_node_features: Union[int, Dict[str, int]],
                 in_edge_features: Union[int, Dict[Tuple[str, str, str], int]],
                 in_global_features: Optional[int],
                 latent_dimension: int,
                 scatter_reduce_strs: List[str],
                 output_type: str,
                 create_graph_copy: bool = True,
                 assert_graph_shapes: bool = True,
                 device: Optional[torch.device] = None,
                 agent_node_type: str = AGENT):
        """

        Args:
            in_node_features:
                Either a simple integer for the size of a single node feature, or a
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
                Can be a singular entity or a list of "sum", "mean", "max", "min", "std"
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
        super().__init__()
        self._latent_dimension = latent_dimension
        self._scatter_reducers = get_scatter_reducers(scatter_reduce_strs)
        self._agent_node_type = agent_node_type

        self.maybe_assertions: AbstractGraphAssertions
        if assert_graph_shapes:
            self.maybe_assertions = self._get_assertions()(in_node_features=in_node_features,
                                                           in_edge_features=in_edge_features,
                                                           in_global_features=in_global_features)
        else:
            self.maybe_assertions = noop

        self.maybe_create_copy: Callable = get_create_copy(create_graph_copy=create_graph_copy)

        self.input_embeddings: AbstractInputEmbedding = None
        self.message_passing_stack: AbstractStack = None
        # todo maybe refactor?

        self.maybe_transform_output = self._get_transform_output(output_type=output_type)

    def _get_assertions(self): # removed annotation  -> Type[AbstractGraphAssertions]
        raise NotImplementedError("'get_assertions' not implemented for AbstractMessagePassingBase")

    def _get_transform_output(self, output_type: str):
        """
        Returns a function that transforms the output of the network to the desired output type.
        Args:
            output_type: Either "features" or "graph".

        Returns: Either a function that transforms the output of the network to the desired output type, or a function
        that returns nothing if output_type is "graph"
        """
        if output_type == "features":
            return self.transform_to_features
        elif output_type == "graph":
            return noop
        else:
            raise ValueError(f"Unknown output_type '{output_type}'")

    def transform_to_features(self, graph: Batch) -> Tuple[Union[int, Dict[str, int]],
                                                                 Union[int, Dict[Tuple[str, str, str], int]],
                                                                 Optional[int],
                                                                 Union[int, Dict[str, int]]]:
        raise NotImplementedError("'transform_to_features' not implemented for AbstractMessagePassingBase")

    def forward(self, graph: Batch) -> Batch:
        """
        Performs a forward pass through the Graph Neural Network for the given input
            batch of (potentially heterogeneous) graphs. Note that this forward pass may not be deterministic wrt.
            floating point precision because the used scatter_reduce functions are not.

        Args:
            graph: Batch object of pytorch geometric.
                Represents a (batch of) (potentially heterogeneous) graph(s)

        Returns:
            Either a modified graph or a tuple of (node_features, edge_features, global_features), depending on the
                configuration of the class at initialization.
                All node, edge and potentially global features went through an embedding and multiple rounds of
                message passing.

        """
        self.maybe_assertions(graph)
        graph = self.maybe_create_copy(graph)
        self.input_embeddings(graph)
        self.message_passing_stack(graph)
        return self.maybe_transform_output(graph)

    @property
    def latent_dimension(self) -> int:
        """
        Returns the latent dimension of the network which is used in all feature sizes.
        Returns: int
        """
        return self._latent_dimension
