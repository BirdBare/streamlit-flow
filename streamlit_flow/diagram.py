from .base_edge import BaseEdge
from .base_node import BaseNode


class Diagram:
    def __init__(
        self,
        nodes: set[BaseNode],
        edges: set[BaseEdge],
        *,
        selected: BaseNode | BaseEdge | None = None,
    ):
        self.nodes = nodes
        self.edges = edges
        self.selected = selected
