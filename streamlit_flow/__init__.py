import os
import typing
import uuid

import streamlit.components.v1 as components

from .base_node import BaseNode
from .diagram import Diagram
from .edge import Edge
from .handle import Handle
from .layouts import Layout, ManualLayout
from .markdown_node import MarkdownNode
from .marker import Marker

_RELEASE = True

if not _RELEASE:
    _st_flow_func = components.declare_component(
        "streamlit_flow",
        url="http://localhost:3001/",
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
    type_of_new_edges: typing.Literal["default", "straight", "step", "smoothstep", "simplebezier"] = "default",
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
    node_by_id: dict[str, BaseNode] = {str(node.id): node for node in diagram.nodes}
    handle_by_id: dict[str, Handle] = {str(handle.id): handle for handle in diagram.handles}
    edge_by_id: dict[str, Edge] = {str(edge.id): edge for edge in diagram.edges}
    marker_by_id: dict[str, Marker] = {str(marker.id): marker for marker in diagram.markers}

    node_dicts = [node.as_dict() for node in diagram.nodes]
    for node_dict in node_dicts:
        node_dict["data"]["handles"] = [
            handle_by_id[handle_id].as_dict() for handle_id in node_dict["data"]["handleIds"]
        ]

    edge_dicts = [edge.as_dict() for edge in diagram.edges]
    for edge_dict in edge_dicts:
        marker_id = edge_dict["markerStartId"]
        if marker_id is not None:
            edge_dict["markerStart"] = marker_by_id[marker_id].as_dict()

        marker_id = edge_dict["markerEndId"]

        if marker_id is not None:
            edge_dict["markerEnd"] = marker_by_id[marker_id].as_dict()

    component_value = _st_flow_func(
        nodes=node_dicts,
        edges=edge_dicts,
        height=height,
        showControls=show_controls,
        fitView=fit_view,
        showMiniMap=show_minimap,
        style=style,
        allowNewEdges=allow_new_edges,
        animateNewEdges=animate_new_edges,
        typeOfNewEdges=type_of_new_edges,
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

    output_nodes: set[BaseNode] = set()
    output_handles: set[Handle] = set()
    for node_dict in component_value["nodes"]:
        node_id = node_dict["id"]
        try:
            node = node_by_id[node_id]
            node.update_from_dict(node_dict)
        except KeyError:
            node = BaseNode.subclass_registry[node_dict["type"]].from_dict(node_dict)

        output_nodes.add(node)

    output_edges: set[Edge] = set()
    output_markers: set[Marker] = set()
    for edge_dict in component_value["edges"]:
        edge_id = edge_dict["id"]
        try:
            edge = edge_by_id[edge_id]
            edge.update_from_dict(edge_dict)
        except KeyError:
            edge = Edge.from_dict(edge_dict)

        output_edges.add(edge)

    selected_id = component_value["selectedId"]
    if selected_id is not None:
        selected_id = uuid.UUID(selected_id)

    return Diagram(
        nodes=list(output_nodes),
        edges=list(output_edges),
        handles=diagram.handles,
        markers=diagram.markers,
        selected_id=selected_id,
        timestamp=component_value["timestamp"],
    )
