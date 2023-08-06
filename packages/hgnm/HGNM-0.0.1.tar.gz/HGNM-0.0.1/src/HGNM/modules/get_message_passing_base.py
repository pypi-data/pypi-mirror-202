import torch
from typing import Optional, Tuple
from util.Types import *
from modules.heterogeneous.HeterogeneousMessagePassingBase import HeterogeneousMessagePassingBase
from modules.heterogeneous.mock.MockHeteroBase import MockHeteroBase
from modules.homogeneous.HomogeneousMessagePassingBase import HomogeneousMessagePassingBase
from modules.abstract.AbstractMessagePassingBase import AbstractMessagePassingBase


def get_message_passing_base(*,
                             in_node_features: Union[int, Dict[str, int]],
                             in_edge_features: Union[int, Dict[Tuple[str, str, str], int]],
                             in_global_features: Optional[int],
                             latent_dimension: int,
                             base_config: ConfigDict,
                             agent_node_type: str,
                             device: Optional[torch.device] = None) -> AbstractMessagePassingBase:
    """
    Build and return a Message Passing Base specified in the config. The base may be either suited for message
    passing on homogeneous or heterogeneous graphs, depending on whether the input feature dimensions for nodes and
    edges are given as dictionaries Dict[str, int], or as simple integers.

    Args:
        in_node_features: Either a single integer, or a dictionary of node types to integers
        in_edge_features: Either a single integer, or a dictionary of (source_node_type, edge_type, target_node_type)
            to integers
        in_global_features: Either None, or an integer
        latent_dimension: The dimension of the latent space
        base_config: The config for the base
        agent_node_type: The node type of the agent
        device: The device to put the base on

    Returns:
        A Message Passing Base operating on either homogeneous or heterogeneous graphs.

    """
    assert type(in_node_features) == type(in_edge_features), f"May either provide feature dimensions as int or Dict, " \
                                                             f"but not both. " \
                                                             f"Given '{in_node_features}', '{in_edge_features}'"

    create_graph_copy = base_config.get("create_graph_copy")
    assert_graph_shapes = base_config.get("assert_graph_shapes")
    use_homogeneous_graph = base_config.get("use_homogeneous_graph")
    stack_config = base_config.get("stack")
    embedding_config = base_config.get("embedding")
    scatter_reduce_strs = base_config.get("scatter_reduce")
    if isinstance(scatter_reduce_strs, str):
        scatter_reduce_strs = [scatter_reduce_strs]

    if isinstance(in_node_features, Dict):
        # heterogeneous graph. Can either convert to homogeneous graph or keep as heterogeneous graph.
        if use_homogeneous_graph:
            base = MockHeteroBase
        else:
            base = HeterogeneousMessagePassingBase
    elif isinstance(in_node_features, int):
        base = HomogeneousMessagePassingBase
    else:
        raise ValueError(f"Invalid type '{type(in_node_features)}' for in_node_features '{in_node_features}'. "
                         f"May use either a dictionary Dict[str, int], or a simple int")
    return base(in_node_features=in_node_features,
                in_edge_features=in_edge_features,
                in_global_features=in_global_features,
                latent_dimension=latent_dimension,
                scatter_reduce_strs=scatter_reduce_strs,
                stack_config=stack_config,
                embedding_config=embedding_config,
                create_graph_copy=create_graph_copy,
                assert_graph_shapes=assert_graph_shapes,
                device=device,
                agent_node_type=agent_node_type)
