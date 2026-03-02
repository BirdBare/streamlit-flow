import datetime

from .streamlit_flow_edge import StreamlitFlowEdge
from .streamlit_flow_node import StreamlitFlowNode


class StreamlitFlowState:
    def __init__(
        self,
        nodes: list[StreamlitFlowNode],
        edges: list[StreamlitFlowEdge],
        *,
        timestamp: int = int(datetime.datetime.now().timestamp() * 1000),
        selected: StreamlitFlowNode | StreamlitFlowEdge | None = None,
    ):
        self.nodes = nodes
        self.edges = edges
        self.timestamp = timestamp
        self.selected = selected
