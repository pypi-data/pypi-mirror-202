from typing import Dict, Optional, Tuple
from torch_geometric.data import Batch

from src.HGNM.modules.abstract.AbstractGraphAssertions import AbstractGraphAssertions


class HeterogeneousGraphAssertions(AbstractGraphAssertions):

    def __init__(self, *,
                 in_node_features: Dict[str, int],
                 in_edge_features: Dict[Tuple[str, str, str], int],
                 in_global_features: Optional[int]
                 ):
        super().__init__(in_node_features=in_node_features,
                         in_edge_features=in_edge_features,
                         in_global_features=in_global_features)

    def __call__(self, graph: Batch):
        """
        Does various shape assertions to make sure that the (batch of) graph(s) is built correctly
        Args:
            graph: batch of heterogeneous graphs

        Returns: None

        """
        super().__call__(graph)

        # general assertions
        for edge_type, edge_store in zip(graph.edge_types, graph.edge_stores):
            assert "edge_attr" in edge_store.keys(), f"Edge store corresponding to type '{edge_type}' must provide " \
                                                     f"key 'edge_attr'. Given key(s) '{edge_store.keys()}' instead."
            assert "edge_index" in edge_store.keys(), f"Edge store corresponding to type '{edge_type}' must provide " \
                                                      f"key 'edge_index'. Given key(s) '{edge_store.keys()}' instead."

            index_shape = edge_store.get("edge_index").shape
            feature_shape = edge_store.get("edge_attr").shape
            assert index_shape[0] == 2, f"Edge index must have shape (2, num_edges), given '{index_shape}' instead."
            assert index_shape[1] == feature_shape[0], f"Must provide one edge index per edge feature vector, " \
                                                       f"given '{index_shape}' and '{feature_shape}' instead."

        for node_type, node_store in zip(graph.node_types, graph.node_stores):
            assert "x" in node_store.keys(), f"Node store corresponding to type '{node_type}' must provide key 'x'. " \
                                             f"Given key(s) '{node_store.keys()}' instead."

        # node assertions
        in_node_features = self._assertion_dict.get("in_node_features")
        assert len(graph.node_types) == len(
            in_node_features.keys()), f"Number of node types does not match. Given '{len(graph.node_types)}'," \
                                      f"expected '{len(in_node_features.keys())}'"
        for node_type, node_store in zip(graph.node_types, graph.node_stores):
            assert node_store["x"].shape[-1] == in_node_features[node_type], f"Feature dimensions of node type " \
                                                                             f"{node_type} do not match. Given " \
                                                                             f"'{node_store['x'].shape[-1]}', " \
                                                                             f"expected '{in_node_features[node_type]}"

        # edge assertions
        in_edge_features = self._assertion_dict.get("in_edge_features")
        assert len(graph.edge_types) == len(in_edge_features.keys()), f"Number of edge types does not match. " \
                                                                       f"Given '{len(graph.edge_types)}', " \
                                                                       f"expected '{len(in_edge_features.keys())}'"
        for edge_type, edge_store in zip(graph.edge_types, graph.edge_stores):
            in_features = edge_store["edge_attr"].shape[-1]
            expected_features = in_edge_features[edge_type]
            assert in_features == expected_features, f"Feature dimensions of edge type {edge_type} do not match. " \
                                               f"Given '{in_features}', expected '{expected_features}"

        if self._assert_global:
            for node_type in graph.node_types:
                assert hasattr(graph[node_type], "batch"), \
                    f"Need batch pointer for graph ids when using batch and global features for node type {node_type}"
                assert graph[node_type].batch is not None, \
                    f"Batch pointer for node type {node_type} is None"