import os
import typing
import uuid

import streamlit.components.v1 as components

from .base_edge import BaseEdge
from .base_node import BaseNode
from .diagram import Diagram
from .handle import Handle
from .layouts import Layout, ManualLayout
from .markdown_edge import MarkdownEdge
from .markdown_node import MarkdownNode
from .marker import Marker

_RELEASE = True

if not _RELEASE:
    _st_flow_func = components.declare_component(
        "streamlit_flow",
        url="http://localhost:3333/",
    )

else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _st_flow_func = components.declare_component("streamlit_flow", path=build_dir)


def render(
    key: str,
    diagram: Diagram,
    *,
    height: int = 500,
    fit_view: bool = False,
    show_controls: bool = True,
    show_minimap: bool = False,
    allow_new_edges: bool = False,
    animate_new_edges: bool = False,
    new_edge_line_type: typing.Literal["straight", "smoothstep", "simplebezier", "bezier"] = "simplebezier",
    style: dict = {},
    layout: Layout = ManualLayout(),
    get_node_on_click: bool = False,
    get_edge_on_click: bool = False,
    pan_on_drag: bool = True,
    allow_zoom: bool = True,
    min_zoom: float = 0.5,
    hide_watermark: bool = False,
):
    """
    The main function to render the flowchart component in Streamlit.

    Arguments:
    - **key** : str : A unique identifier for the component.
    - **state** : StreamlitFlowState : The current state of the flowchart component.
    - **height** : int : The height of the component in pixels.
    - **fit_view** : bool : Whether to fit the view of the component.
    - **show_controls** : bool : Whether to show the controls of the component.
    - **show_minimap** : bool : Whether to show the minimap of the component.
    - **allow_new_edges** : bool : Whether to allow new edges to be created.
    - **animate_new_edges** : bool : Whether to animate new edges created on the canvas.
    - **style** : dict : CSS style of the component.
    - **layout** : Layout : The layout of the nodes in the component.
    - **get_node_on_click** : bool : Whether to get the node on click.
    - **get_edge_on_click** : bool : Whether to get the edge on click.
    - **pan_on_drag** : bool : Whether to pan on drag.
    - **allow_zoom** : bool : Whether to allow zoom.
    - **min_zoom** : float : The minimum zoom level.
    - **hide_watermark** : bool : Whether to hide the watermark.

    """
    component_value = _st_flow_func(
        nodes=[node.as_dict() for node in diagram.nodes],
        edges=[edge.as_dict() for edge in diagram.edges],
        height=height,
        showControls=show_controls,
        fitView=fit_view,
        showMiniMap=show_minimap,
        style=style,
        allowNewEdges=allow_new_edges,
        animateNewEdges=animate_new_edges,
        typeOfNewEdges=new_edge_line_type,
        layoutOptions=layout.__to_dict__(),
        getNodeOnClick=get_node_on_click,
        getEdgeOnClick=get_edge_on_click,
        panOnDrag=pan_on_drag,
        allowZoom=allow_zoom,
        minZoom=min_zoom,
        hideWatermark=hide_watermark,
        key=key,
        timestamp=diagram.timestamp,
        component="streamlit_flow",
    )

    if component_value is None:
        return diagram

    node_by_id: dict[str, BaseNode] = {str(node.id): node for node in diagram.nodes}
    handle_by_id: dict[str, Handle] = {str(handle.id): handle for node in diagram.nodes for handle in node.handles}
    edge_by_id: dict[str, BaseEdge] = {str(edge.id): edge for edge in diagram.edges}
    marker_by_id: dict[str, Marker] = {
        str(marker.id): marker
        for edge in diagram.edges
        for marker in (edge.source_marker, edge.target_marker)
        if marker is not None
    }

    for node_dict in component_value["nodes"]:
        node_id = node_dict["id"]

        assert node_id in node_by_id

        node = node_by_id[node_id]
        node_dict["data"]["handles"] = node.handles
        node.update_from_dict(node_dict)

    for edge_dict in component_value["edges"]:
        edge_id = edge_dict["id"]

        if edge_id not in edge_by_id:
            edge_dict["source"] = node_by_id[edge_dict["source"]]
            edge_dict["sourceHandle"] = handle_by_id[edge_dict["sourceHandle"]]
            edge_dict["target"] = node_by_id[edge_dict["target"]]
            edge_dict["targetHandle"] = handle_by_id[edge_dict["targetHandle"]]

            edge = BaseEdge.subclass_registry[edge_dict["type"]].from_dict(edge_dict)

            edge_by_id[str(edge.id)] = edge

    selected_id = component_value["selectedId"]
    selected = None

    if selected_id is not None:
        if selected_id in node_by_id:
            selected = node_by_id[selected_id]
        elif selected_id in edge_by_id:
            selected = edge_by_id[selected_id]

    return Diagram(
        nodes=set(node_by_id.values()),
        edges=set(edge_by_id.values()),
        selected=selected,
        timestamp=component_value["timestamp"],
    )
