from abc import ABC


class Skeleton(ABC):
    """Base class for skeleton used by different datasets.

    Each skeleton is defined as a graph with nodes and edges, and a unique
    name to identify it.
    """

    def __init__(self, name, nodes, edges) -> None:
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.num_keypoints = len(self.nodes)

    def __str__(self) -> str:
        return self.name
