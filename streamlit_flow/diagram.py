import datetime
import uuid

from .base_node import BaseNode
from .edge import Edge
from .handle import Handle
from .marker import Marker


class Diagram:
    def __init__(
        self,
        nodes: list[BaseNode],
        handles: list[Handle],
        edges: list[Edge],
        markers: list[Marker],
        *,
        timestamp: int = int(datetime.datetime.now().timestamp() * 1000),
        selected_id: uuid.UUID | None = None,
    ):
        self.nodes = nodes
        self.handles = handles
        self.edges = edges
        self.markers = markers
        self.timestamp = timestamp
        self.selected_id = selected_id
