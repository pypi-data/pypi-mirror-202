from torch import nn
from typing import Optional, Tuple
import torch

from src.HGNM.util.Types import *
from src.HGNM.modules.common.Embedding import Embedding
from src.HGNM.modules.common.hmpn_util import tuple_to_string
from src.HGNM.modules.abstract.AbstractInputEmbedding import AbstractInputEmbedding


class HeterogeneousInputEmbedding(AbstractInputEmbedding):
    """
    Input feature embedding for Heterogeneous Graphs.
    """

    def __init__(self,
                 *,
                 in_node_features: Dict[str, int],
                 in_edge_features: Dict[Tuple[str, str, str], int],
                 in_global_features: Optional[int],
                 embedding_config: Optional[ConfigDict],
                 latent_dimension: int,
                 device: Optional[torch.device]):
        """
        Initializes the heterogeneous input embedding

        Args:
            in_node_features: Keys are node types and values are the number of input features for that node type
            in_edge_features: Keys are edge types and values are the number of input features for that edge type
            in_global_features: Number of input features for the global features
            embedding_config: Embedding configuration dictionary
            latent_dimension: Dimension of the latent space
            device: Device to use for the embeddings
        """
        super().__init__(in_global_features=in_global_features, latent_dimension=latent_dimension,
                         embedding_config=embedding_config, device=device)
        self.node_input_embeddings = nn.ModuleDict({node_name: Embedding(in_features=num_node_features,
                                                                         latent_dimension=latent_dimension,
                                                                         embedding_config=embedding_config,
                                                                         device=device)
                                                    for node_name, num_node_features in in_node_features.items()})

        self.edge_input_embeddings = nn.ModuleDict(
            {tuple_to_string(edge_name): Embedding(in_features=num_edge_features,
                                                   latent_dimension=latent_dimension,
                                                   embedding_config=embedding_config,
                                                   device=device)
             for edge_name, num_edge_features in in_edge_features.items()})

    def forward(self, graph: Batch):
        """
        Computes the forward pass for this heterogeneous input embedding
        Args:
            graph: Batch object of pytorch geometric. Represents a batch of heterogeneous graphs

        Returns: None. In-place modification of the graph object.
        """
        for position, node_type in enumerate(graph.node_types):
            graph.node_stores[position]["x"] = self.node_input_embeddings[node_type](
                graph.node_stores[position]["x"])

        for position, edge_type in enumerate(graph.edge_types):
            graph.edge_stores[position]["edge_attr"] = self.edge_input_embeddings[tuple_to_string(edge_type)](
                graph.edge_stores[position]["edge_attr"])

        super().forward(graph=graph)
