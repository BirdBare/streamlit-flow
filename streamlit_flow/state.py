from dataclasses import dataclass, field
from datetime import datetime

from .elements import StreamlitFlowEdge, StreamlitFlowNode


@dataclass
class StreamlitFlowState:
    """
    Container to maintain the state of the flowchart component.

    Arguments:
    - **nodes** : List[StreamlitFlowNode] : The list of nodes in the flowchart.
    - **edges** : List[StreamlitFlowEdge] : The list of edges in the flowchart.
    - **selected_id** : str? : The id of the selected node.
    - **timestamp** : float? : The timestamp of the state.

    """

    nodes: list[StreamlitFlowNode]
    edges: list[StreamlitFlowEdge]
    selected_id: str | None = None
    timestamp: int = field(default_factory=lambda: int(datetime.now().timestamp() * 1000))

    def asdict(self):
        return {
            "nodes": [node.asdict() for node in self.nodes],
            "edges": [edge.asdict() for edge in self.edges],
            "selected_id": self.selected_id,
            "timestamp": self.timestamp,
        }
