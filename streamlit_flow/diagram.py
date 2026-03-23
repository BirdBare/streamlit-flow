import datetime
import uuid

from .base_node import BaseNode
from .edge import Edge


class Diagram:
    def __init__(
        self,
        nodes: list[BaseNode],
        edges: list[Edge],
        *,
        timestamp: int = int(datetime.datetime.now().timestamp() * 1000),
        selected_id: uuid.UUID | None = None,
    ):
        self.nodes = nodes
        self.edges = edges
        self.timestamp = timestamp
        self.selected_id = selected_id
