import os
import typing
import uuid

import streamlit.components.v1 as components

from .base_node import BaseNode
from .edge import Edge
from .handle import Handle
from .layouts import Layout, ManualLayout
from .markdown_node import MarkdownNode
from .marker import Marker
from .state import State

_RELEASE = False

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
    state: State,
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
    component_value = _st_flow_func(
        nodes=[node.as_dict() for node in state.nodes],
        edges=[edge.as_dict() for edge in state.edges],
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
        timestamp=state.timestamp,
        component="streamlit_flow",
    )

    if component_value is None:
        return state

    import json

    print(json.dumps(component_value["nodes"], indent=2))

    #
    # Collect and create the handles at the basic level. Valid handles will be added next
    #
    handle_ids: set[str] = set()
    handle_by_id: dict[str, Handle] = {}
    handle_dict_by_id: dict[str, dict[str, typing.Any]] = {}
    for node_dict in component_value["nodes"]:
        data = node_dict["data"]

        for handle_dict in data["handles"]:
            id = handle_dict["id"]

            handle_dict_by_id[id] = handle_dict
            handle_by_id[id] = Handle.from_dict(handle_dict)

    #
    # Iterate through to add the valid handles
    #
    for id in handle_ids:
        handle = handle_by_id[id]
        handle_dict = handle_dict_by_id[id]

        handle.valid_targets.add(*[handle_by_id[valid_id] for valid_id in handle_dict["validTargetIds"]])

    #
    # Build nodes now that the handles are available
    #
    node_by_id: dict[str, BaseNode] = {}
    for node_dict in component_value["nodes"]:
        data = node_dict["data"]

        node_dict["data"]["handles"] = [handle_by_id[handle_dict["id"]] for handle_dict in data["handles"]]

        node_by_id[node_dict["id"]] = BaseNode.subclass_registry[node_dict["type"]].from_dict(node_dict)

    #
    # Build Markers
    #
    marker_by_id: dict[str, Marker] = {}
    for edge_dict in component_value["edges"]:
        marker_start_dict = edge_dict["markerStart"]
        if "id" in marker_start_dict:
            marker_by_id[marker_start_dict["id"]] = Marker.from_dict(marker_start_dict)

        marker_end_dict = edge_dict["markerEnd"]
        if "id" in marker_end_dict:
            marker_by_id[marker_end_dict["id"]] = Marker.from_dict(marker_end_dict)

    #
    # Build edges now that we have everything built.
    #
    edge_by_id: dict[str, Edge] = {}
    for edge_dict in component_value["edges"]:
        edge_dict["source_node"] = node_by_id[edge_dict["source"]]
        edge_dict["source_handle"] = handle_by_id[edge_dict["sourceHandle"]]

        edge_dict["target_node"] = node_by_id[edge_dict["target"]]
        edge_dict["target_handle"] = handle_by_id[edge_dict["targetHandle"]]

        try:
            edge_dict["marker_start"] = marker_by_id[edge_dict["markerStart"]["id"]]
        except KeyError:
            edge_dict["marker_start"] = None

        try:
            edge_dict["marker_end"] = marker_by_id[edge_dict["markerEnd"]["id"]]
        except KeyError:
            edge_dict["marker_end"] = None

        edge_by_id[edge_dict["id"]] = Edge.from_dict(edge_dict)

    if component_value["selectedId"] is None:
        selected = None
    else:
        selected = {**node_by_id, **edge_by_id}[component_value["selectedId"]]

    return State(
        nodes=list(node_by_id.values()),
        edges=list(edge_by_id.values()),
        selected=selected,
        timestamp=component_value["timestamp"],
    )
