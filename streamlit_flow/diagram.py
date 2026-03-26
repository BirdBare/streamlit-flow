import datetime

from .base_edge import BaseEdge
from .base_node import BaseNode


class Diagram:
    def __init__(
        self,
        nodes: set[BaseNode],
        edges: set[BaseEdge],
        *,
        timestamp: int = int(datetime.datetime.now().timestamp() * 1000),
        selected: BaseNode | BaseEdge | None = None,
    ):
        self.nodes = nodes
        self.edges = edges
        self.timestamp = timestamp
        self.selected = selected
