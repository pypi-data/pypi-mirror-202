from src.HGNM.util.Types import *
from src.HGNM.modules.abstract.AbstractBlock import AbstractBlock
from src.HGNM.modules.homogeneous.HomogeneousModules import HomogeneousEdgeModule, \
    HomogeneousNodeModule, HomogeneousGlobalModule
from src.HGNM.modules.common.hmpn_util import noop


class HomogeneousBlock(AbstractBlock):
    """
         Defines a single MessagePassingLayer that takes a homogeneous observation graph and updates its node and edge
         features using different modules (Edge, Node, Global).
         It first updates the edge-features. The node-features are updated next using the new edge-features. Finally,
         it updates the global features using the new edge- & node-features. The updates are done through MLPs.
    """

    def __init__(self,
                 stack_config: ConfigDict,
                 latent_dimension: int,
                 scatter_reducers,
                 use_global_features: bool = False):
        """
        Initializes the HomogeneousBlock, which realizes a single iteration of message passing for a homogeneous graph.
        This message passing layer consists of three modules: Edge, Node, Global, each of which updates the respective
        part of the graph.
        Initializes the HomogeneousBlock.
        Args:
            stack_config:
                Configuration of the stack of GNN blocks. Should contain keys
                "num_blocks" (int),
                "use_residual_connections" (bool),
                "mlp" (ConfigDict). "mlp" is a dictionary for the general configuration of the MLP.
                    which should contain keys
                    "num_layers" (int),
                    "add_output_layer" (bool),
                    "activation_function" (str: "relu", "leakyrelu", "tanh", "silu"), and
                    "regularization" (ConfigDict),
                        which should contain keys
                        "spectral_norm" (bool),
                        "dropout" (float),
                        "latent_normalization" (str: "batch_norm", "layer_norm" or None)
            latent_dimension:
                Dimension of the latent space.
            scatter_reducers:
                reduce operators from torch_scatter. Can be e.g. [scatter_mean]
            use_global_features:
                Whether to use global features or not.
        """

        super().__init__(latent_dimension=latent_dimension)

        n_scatter_ops = len(scatter_reducers)

        edge_in_features = 3 * latent_dimension  # edge features, and the two participating nodes
        node_in_features = latent_dimension * (1 + n_scatter_ops) # node features and the aggregated incoming edge features

        if use_global_features:
            edge_in_features += latent_dimension
            node_in_features += latent_dimension
            self.global_module = HomogeneousGlobalModule(
                in_features=latent_dimension * (2 * n_scatter_ops + 1),  # global features, reduced edge features and reduced node features
                latent_dimension=latent_dimension,
                stack_config=stack_config,
                scatter_reducers=scatter_reducers
            )
            self._maybe_global = self.global_module
        else:
            self.global_module = None
            self._maybe_global = noop

        # edge module
        self.edge_module = HomogeneousEdgeModule(in_features=edge_in_features,
                                                 latent_dimension=latent_dimension,
                                                 stack_config=stack_config,
                                                 scatter_reducers=scatter_reducers,
                                                 use_global_features=use_global_features)

        # node module
        self.node_module = HomogeneousNodeModule(in_features=node_in_features,
                                                 latent_dimension=latent_dimension,
                                                 stack_config=stack_config,
                                                 scatter_reducers=scatter_reducers,
                                                 use_global_features=use_global_features)

        self.reset_parameters()
