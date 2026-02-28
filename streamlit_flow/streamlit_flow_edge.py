from __future__ import annotations

import typing


class StreamlitFlowEdge:
    """
    Represents an edge in streamlit_flow

    Arguments:
    - **id** : str : Unique identifier for the edge
    - **source** : str : ID of the source node
    - **target** : str : ID of the target node
    - **edge_type** : str : Type of the edge. One of ['default', 'straight', 'step', "smoothstep", "simplebezier"]
    - **marker_start** : dict : Marker at the start of the edge. Eg: {'type': 'arrow'/'arrowclosed'}
    - **marker_end** : dict : Marker at the end of the edge. Eg: {'type': 'arrow'/'arrowclosed'}
    - **hidden** : bool : Whether the edge is hidden
    - **animated** : bool : Whether the edge is animated
    - **selected** : bool : Whether the edge is selected
    - **deletable** : bool : Whether the edge is deletable
    - **focusable** : bool : Whether the edge is focusable
    - **z_index** : float : Z-index of the edge
    - **label** : str : Label of the edge
    - **label_style** : dict[str, typing.Any] : CSS style of the label
    - **label_show_bg** : bool : Whether to show background for the label
    - **label_bg_style** : dict[str, typing.Any] : CSS style of the label background
    - **style** : dict[str, typing.Any] : CSS style of the edge

    """

    def __init__(
        self,
        id: str,
        source: str,
        target: str,
        edge_type: typing.Literal["default", "straight", "step", "smoothstep", "simplebezier"] = "default",
        marker_start: dict = {},
        marker_end: dict = {},
        hidden: bool = False,
        animated: bool = False,
        selected: bool = False,
        deletable: bool = False,
        focusable: bool = False,
        z_index: float = 0,
        label: str = "",
        label_style: dict[str, typing.Any] = {},
        label_show_bg: bool = False,
        label_bg_style: dict[str, typing.Any] = {},
        style: dict[str, typing.Any] = {},
        **kwargs,
    ) -> None:

        self.id = id
        self.source = source
        self.target = target
        self.type = edge_type
        self.marker_start = marker_start
        self.marker_end = marker_end
        self.hidden = hidden
        self.animated = animated
        self.selected = selected
        self.deletable = deletable
        self.focusable = focusable
        self.z_index = z_index
        self.label = label
        self.label_style = label_style
        self.label_show_bg = label_show_bg
        self.label_bg_style = label_bg_style
        self.style = style
        self.kwargs = kwargs

        self.__validate__()

    @classmethod
    def from_dict(cls, edge_dict: dict[str, typing.Any]) -> StreamlitFlowEdge:

        # other_attributes_dict = {key: value for key, value in edge_dict.items() if key not in ['id', 'source', 'target', 'type', 'hidden', 'animated', 'selected', 'deletable', 'focusable', 'zIndex', 'label', 'labelStyle', 'labelShowBg', 'labelBgStyle', 'style']}
        return cls(
            id=edge_dict.get("id", ""),
            source=edge_dict.get("source", ""),
            target=edge_dict.get("target", ""),
            edge_type=edge_dict.get("type", "default"),
            marker_start=edge_dict.get("markerStart", {}),
            marker_end=edge_dict.get("markerEnd", {}),
            hidden=edge_dict.get("hidden", False),
            animated=edge_dict.get("animated", False),
            selected=edge_dict.get("selected", False),
            deletable=edge_dict.get("deletable", False),
            focusable=edge_dict.get("focusable", False),
            z_index=edge_dict.get("zIndex", 0),
            label=edge_dict.get("label", ""),
            label_style=edge_dict.get("labelStyle", {}),
            label_show_bg=edge_dict.get("labelShowBg", False),
            label_bg_style=edge_dict.get("labelBgStyle", {}),
            style=edge_dict.get("style", {}),
        )

    def __validate__(self) -> None:
        assert self.type in ["default", "straight", "step", "smoothstep", "simplebezier"], (
            f"Edge type must be one of ['default', 'straight', 'step', 'smoothstep', 'simplebezier']. Got {self.type}"
        )

    def asdict(self) -> dict[str, typing.Any]:
        edge_dict = {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "type": self.type,
            "markerStart": self.marker_start,
            "markerEnd": self.marker_end,
            "hidden": self.hidden,
            "animated": self.animated,
            "selected": self.selected,
            "deletable": self.deletable,
            "focusable": self.focusable,
            "zIndex": self.z_index,
            "label": self.label,
            "labelStyle": self.label_style,
            "labelShowBg": self.label_show_bg,
            "labelBgStyle": self.label_bg_style,
            "style": self.style,
        }

        edge_dict.update(self.kwargs)
        return edge_dict

    def __repr__(self):
        return f"StreamlitFlowEdge({self.id}, {self.source}->{self.target}, '{self.label}')"
