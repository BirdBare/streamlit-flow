from __future__ import annotations

import typing


class StreamlitFlowNode:
    """
    Represents a node in streamlit_flow

    Arguments:
    - **id** : str : Unique identifier for the node
    - **pos** : tuple[float, float] : Position of the node in the canvas
    - **data** : dict[str, typing.Any] : Arbitrary data to save in the node. Use {'content': 'Node content'} to set the content of the node
    - **node_type** : str : Type of the node. One of ['default', 'input', 'output']
    - **source_position** : str : Position of the source anchor. One of ['top', 'bottom', 'left', 'right']
    - **target_position** : str : Position of the target anchor. One of ['top', 'bottom', 'left', 'right']
    - **hidden** : bool : Whether the node is hidden
    - **selected** : bool : Whether the node is selected
    - **dragging** : bool : Whether the node is being dragged (?)
    - **draggable** : bool : Whether the node is draggable
    - **selectable** : bool : Whether the node is selectable
    - **connectable** : bool : Whether the node is connectable
    - **resizing** : bool : Whether the node is resizable
    - **deletable** : bool : Whether the node is deletable
    - **z_index** : float : Z-index of the node
    - **focusable** : bool : Whether the node is focusable
    - **style** : dict[str, typing.Any] : CSS style of the node

    """

    def __init__(
        self,
        id: str,
        pos: tuple[float, float],
        data: dict[str, typing.Any],
        node_type: typing.Literal["default", "input", "output"] = "default",
        source_position: typing.Literal["bottom", "top", "left", "right"] = "bottom",
        target_position: typing.Literal["bottom", "top", "left", "right"] = "top",
        hidden: bool = False,
        selected: bool = False,
        dragging: bool = False,
        draggable: bool = True,
        selectable: bool = False,
        connectable: bool = False,
        resizing: bool = False,
        deletable: bool = False,
        z_index: float = 0,
        focusable: bool = True,
        style: dict[str, typing.Any] = {},
        **kwargs,
    ) -> None:

        if "width" not in style:
            style["width"] = "auto"
        if "height" not in style:
            style["height"] = "auto"

        self.id = id
        self.position = {"x": pos[0], "y": pos[1]}
        self.data = data
        self.type = node_type
        self.source_position = source_position
        self.target_position = target_position
        self.hidden = hidden
        self.selected = selected
        self.dragging = dragging
        self.draggable = draggable
        self.selectable = selectable
        self.connectable = connectable
        self.resizing = resizing
        self.deletable = deletable
        self.z_index = z_index
        self.focusable = focusable
        self.style = style
        self.kwargs = kwargs

        # Remove post V1.3.0
        if "label" in self.data:
            content = self.data.pop("label")
            self.data["content"] = content

        self.__validate__()

    @classmethod
    def from_dict(cls, node_dict: dict[str, typing.Any]) -> StreamlitFlowNode:

        # other_attributes_dict = {key: value for key, value in node_dict.items() if key not in ['id', 'position', 'data', 'type', 'sourcePosition', 'targetPosition', 'hidden', 'selected', 'dragging', 'draggable', 'selectable', 'connectable', 'resizing', 'deletable', 'width', 'height', 'zIndex', 'focusable', 'style']}

        return cls(
            id=node_dict.get("id", ""),
            pos=(node_dict["position"].get("x", 0), node_dict["position"].get("y", 0)),
            data=node_dict.get("data", {}),
            node_type=node_dict.get("type", "default"),
            source_position=node_dict.get("sourcePosition", "bottom"),
            target_position=node_dict.get("targetPosition", "top"),
            hidden=node_dict.get("hidden", False),
            selected=node_dict.get("selected", False),
            dragging=node_dict.get("dragging", False),
            draggable=node_dict.get("draggable", True),
            selectable=node_dict.get("selectable", False),
            connectable=node_dict.get("connectable", True),
            resizing=node_dict.get("resizing", False),
            deletable=node_dict.get("deletable", False),
            z_index=node_dict.get("zIndex", 0),
            focusable=node_dict.get("focusable", True),
            style=node_dict.get("style", {}),
        )

    def __validate__(self):
        assert self.type in ["default", "input", "output"], (
            f"Node type must be one of ['default', 'input', 'output']. Got {self.type}"
        )
        assert self.source_position in ["top", "bottom", "left", "right"], (
            f"Source position must be one of ['top', 'bottom', 'left', 'right']. Got {self.source_position}"
        )
        assert self.target_position in ["top", "bottom", "left", "right"], (
            f"Target position must be one of ['top', 'bottom', 'left', 'right']. Got {self.target_position}"
        )

    def asdict(self) -> dict[str, typing.Any]:
        node_dict = {
            "id": self.id,
            "position": self.position,
            "data": self.data,
            "type": self.type,
            "sourcePosition": self.source_position,
            "targetPosition": self.target_position,
            "hidden": self.hidden,
            "selected": self.selected,
            "dragging": self.dragging,
            "draggable": self.draggable,
            "selectable": self.selectable,
            "connectable": self.connectable,
            "resizing": self.resizing,
            "deletable": self.deletable,
            "zIndex": self.z_index,
            "focusable": self.focusable,
            "style": self.style,
        }
        node_dict.update(self.kwargs)
        return node_dict

    def __repr__(self):
        return f"StreamlitFlowNode({self.id}, ({round(self.position['x'], 2)}, {round(self.position['y'], 2)}), '{self.data.get('content', '')}')"
