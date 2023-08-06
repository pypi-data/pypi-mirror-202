from torch import nn
from typing import Callable

from src.HGNM.util.Types import *
from src.HGNM.modules.abstract.AbstractBlock import AbstractBlock
from src.HGNM.modules.heterogeneous.HeterogeneousModules import HeterogeneousEdgeModule, \
    HeterogeneousNodeModule, HeterogeneousGlobalModule
from src.HGNM.modules.common.hmpn_util import noop
from src.HGNM.modules.common.LatentMLP import LatentMLP


class HeterogeneousBlock(AbstractBlock):
    """
         Defines a single Message Passing Block that takes a heterogeneous observation graph and updates its node and edge
         features using different modules (Edge, Node, Global).
         It first updates the edge-features. The node-features are updated next using the new edge-features. Finally,
         it updates the global features using the new edge- & node-features. The updates are done through MLPs.
    """

    def __init__(self,
                 node_mlps: nn.ModuleDict,
                 num_edge_types: Dict[str, int],
                 edge_mlps: nn.ModuleDict,
                 latent_dimension: int,
                 scatter_reducers: Union[Callable, List[Callable]],
                 stack_config: ConfigDict,
                 use_global_features: bool,
                 global_mlp: LatentMLP):
        """
        Initializes the HeterogeneousBlock.

        Args:
            node_mlps: Dictionary of node MLPs. The keys are the node types and the values are the MLPs.
            num_edge_types: Dictionary of edge types and the number of edge types.
            edge_mlps: Dictionary of edge MLPs. The keys are the edge types and the values are the MLPs.
            latent_dimension: Dimension of the latent space.
            scatter_reducers: list of functions from torch_scatter to use for scatter operations.
            stack_config: Dictionary of stack configuration.
            use_global_features: Whether to use global features or not.
            global_mlp: MLP for global features.
        """
        super().__init__(latent_dimension=latent_dimension)

        self._outer_aggregation: str = stack_config.get("outer_aggregation")

        # edge module
        self.edge_module = HeterogeneousEdgeModule(mlps=edge_mlps,
                                                   scatter_reducers=scatter_reducers,
                                                   use_global_features=use_global_features,
                                                   latent_dimension=latent_dimension,
                                                   outer_aggregation=self._outer_aggregation)

        # node module

        self.node_module = HeterogeneousNodeModule(mlps=node_mlps,
                                                   num_edge_types=num_edge_types,
                                                   latent_dimension=latent_dimension,
                                                   outer_aggregation=self._outer_aggregation,
                                                   scatter_reducers=scatter_reducers,
                                                   use_global_features=use_global_features)

        if use_global_features:
            self.global_module = HeterogeneousGlobalModule(
                mlps=nn.ModuleDict({"u": global_mlp}),
                scatter_reducers=scatter_reducers,
                use_global_features=use_global_features,
                latent_dimension=latent_dimension,
                outer_aggregation=self._outer_aggregation
            )
            self._maybe_global = self.global_module
        else:
            self.global_module = None
            self._maybe_global = noop

        self.reset_parameters()

    def __repr__(self):
        return super().__repr__() + f"outer_aggregation_type={self._outer_aggregation}"
