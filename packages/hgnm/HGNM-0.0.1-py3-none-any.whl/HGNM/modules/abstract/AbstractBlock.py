import abc
from typing import Optional
from torch import nn
from src.HGNM.util.Types import *
from src.HGNM.modules.common.hmpn_util import noop


class AbstractBlock(nn.Module, abc.ABC):
    """
     Defines a single Message Passing Block that takes an observation graph and updates its node and edge
     features using different modules described in implementations of this abstract class.
     It first updates the edge-features. The node-features are updated next using the new edge-features. Finally,
     it updates the global features using the new edge- & node-features. The updates are done through MLPs.
    """

    def __init__(self,
                 latent_dimension: int):
        """
        Args:
            latent_dimension:
                Dimension of the latent space.
        """
        super().__init__()
        self._latent_dimension = latent_dimension

        self.edge_module: Optional[nn.Module] = None
        self.node_module: Optional[nn.Module] = None
        self.global_module: Optional[nn.Module] = None
        self._maybe_global = noop

    def reset_parameters(self):
        """
        This resets all the parameters for all modules
        """
        for item in [self.node_module, self.edge_module, self.global_module]:
            if hasattr(item, 'reset_parameters'):
                item.reset_parameters()

    def forward(self, graph: Data):
        """
        Computes the forward pass for this heterogeneous block/meta layer inplace

        Args:
            graph: Data object of pytorch geometric. Represents a (batch of) of homogeneous graph(s)

        Returns:
            None
        """
        self.edge_module(graph)
        self.node_module(graph)
        self._maybe_global(graph)

    def __repr__(self):
        return f"{self.__class__.__name__}(\n " \
               f"edge_module={self.edge_module},\n" \
               f"node_module={self.node_module},\n " \
               f"global_module={self.global_module}\n)"
