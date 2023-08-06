from typing import Optional
import torch

from src.HGNM.util.Types import *
from src.HGNM.modules.common.Embedding import Embedding
from src.HGNM.modules.abstract.AbstractInputEmbedding import AbstractInputEmbedding


class HomogeneousInputEmbedding(AbstractInputEmbedding):
    def __init__(self,
                 *,
                 in_node_features: int,
                 in_edge_features: int,
                 in_global_features: Optional[int],
                 latent_dimension: int,
                 embedding_config: Optional[ConfigDict],
                 device: Optional[torch.device]):
        """
        Builds and returns an input embedding for a homogeneous graph.
        Args:
            in_node_features:
                number of input node features
            in_edge_features:
                number of input edge features
            in_global_features:
                number of input global features. None if no global features are used.
            latent_dimension:
                dimension of the latent space.
            device:
                torch.device to use
        """
        super().__init__(in_global_features=in_global_features, 
                         latent_dimension=latent_dimension,
                         embedding_config=embedding_config,
                         device=device)

        self.node_input_embedding = Embedding(in_features=in_node_features, 
                                              latent_dimension=latent_dimension,
                                              embedding_config=embedding_config, 
                                              device=device)

        self.edge_input_embedding = Embedding(in_features=in_edge_features, 
                                              latent_dimension=latent_dimension,
                                              embedding_config=embedding_config, 
                                              device=device)

        if in_global_features is not None:
            self.global_input_embedding = Embedding(in_features=in_global_features,
                                                    latent_dimension=latent_dimension,
                                                    embedding_config=embedding_config, device=device)

    def forward(self, graph: Data):
        """
        Computes the forward pass for this homogeneous input embedding inplace
        Args:
            graph: torch_geometric.data.Batch, represents a batch of homogeneous graphs
        Returns:
            None
        """
        graph.__setattr__("x", self.node_input_embedding(graph.x))
        graph.__setattr__("edge_attr", self.edge_input_embedding(graph.edge_attr))

        super().forward(graph=graph)
