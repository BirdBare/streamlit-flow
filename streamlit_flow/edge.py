from __future__ import annotations

import contextlib
import typing
import uuid


class Edge:
    def __init__(
        self,
        source_node_id: uuid.UUID,
        source_handle_id: uuid.UUID,
        target_node_id: uuid.UUID,
        target_handle_id: uuid.UUID,
        label: str = "",
        *,
        type: typing.Literal["default", "straight", "step", "smoothstep", "simplebezier"] = "default",
        source_marker_id: uuid.UUID | None = None,  # TODO
        target_marker_id: uuid.UUID | None = None,  # TODO
        hidden: bool = False,
        animated: bool = False,
        deletable: bool = True,
        focusable: bool = True,
        z_index: float = 0,
        style: dict[str, typing.Any] = {},
        label_style: dict[str, typing.Any] = {},
    ) -> None:

        self.id = uuid.uuid4()
        self.source_node_id = source_node_id
        self.source_handle_id = source_handle_id
        self.target_node_id = target_node_id
        self.target_handle_id = target_handle_id
        self.label = label
        self.type = type
        self.source_marker_id = source_marker_id
        self.target_marker_id = target_marker_id
        self.hidden = hidden
        self.animated = animated
        self.deletable = deletable
        self.focusable = focusable
        self.z_index = z_index

        if style == {}:
            self.style = {}
        else:
            self.style = style

        if label_style == {}:
            self.label_style = {}
        else:
            self.label_style = label_style

    def __eq__(self, value) -> bool:
        try:
            return self.id == value.id
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": str(self.id),
            "source": str(self.source_node_id),
            "sourceHandle": str(self.source_handle_id),
            "target": str(self.target_node_id),
            "targetHandle": str(self.target_handle_id),
            "label": self.label,
            "type": self.type,
            "markerStartId": str(self.source_marker_id) if self.source_marker_id is not None else None,
            "markerEndId": str(self.target_marker_id) if self.target_marker_id is not None else None,
            "hidden": self.hidden,
            "animated": self.animated,
            "deletable": self.deletable,
            "focusable": self.focusable,
            "zIndex": self.z_index,
            "style": self.style,
            "labelStyle": self.label_style,
        }

        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:
        instance = cls(
            source_node_id=uuid.UUID(input_dict["source"]),
            source_handle_id=uuid.UUID(input_dict["sourceHandle"]),
            target_node_id=uuid.UUID(input_dict["target"]),
            target_handle_id=uuid.UUID(input_dict["targetHandle"]),
            label=input_dict.get("label", ""),
            type=input_dict.get("type", "default"),
            source_marker_id=uuid.UUID(input_dict.get("markerStartId"))
            if input_dict.get("markerStartId") is not None
            else None,
            target_marker_id=uuid.UUID(input_dict.get("markerEndId"))
            if input_dict.get("markerEndId") is not None
            else None,
            hidden=input_dict.get("hidden", False),
            animated=input_dict.get("animated", False),
            deletable=input_dict.get("deletable", True),
            focusable=input_dict.get("focusable", True),
            z_index=input_dict.get("zIndex", 0),
            style=input_dict.get("style", {}),
            label_style=input_dict.get("labelStyle", {}),
        )

        if "id" in input_dict:
            instance.id = uuid.UUID(input_dict["id"])

        return instance

    def update_from_dict(self, input_dict: dict[str, typing.Any]):
        with contextlib.suppress(KeyError):
            self.source_node_id = uuid.UUID(input_dict["source"])
        with contextlib.suppress(KeyError):
            self.source_handle_id = uuid.UUID(input_dict["sourceHandle"])
        with contextlib.suppress(KeyError):
            self.target_node_id = uuid.UUID(input_dict["target"])
        with contextlib.suppress(KeyError):
            self.target_handle_id = uuid.UUID(input_dict["targetHandle"])
        with contextlib.suppress(KeyError):
            self.label = input_dict["label"]
        with contextlib.suppress(KeyError):
            self.type = input_dict["type"]
        with contextlib.suppress(KeyError):
            self.source_marker_id = (
                uuid.UUID(input_dict["markerStartId"]) if input_dict["markerStartId"] is not None else None
            )
        with contextlib.suppress(KeyError):
            self.target_marker_id = (
                uuid.UUID(input_dict["markerEndId"]) if input_dict["markerEndId"] is not None else None
            )
        with contextlib.suppress(KeyError):
            self.hidden = input_dict["hidden"]
        with contextlib.suppress(KeyError):
            self.animated = input_dict["animated"]
        with contextlib.suppress(KeyError):
            self.deletable = input_dict["deletable"]
        with contextlib.suppress(KeyError):
            self.focusable = input_dict["focusable"]
        with contextlib.suppress(KeyError):
            self.z_index = input_dict["zIndex"]
        with contextlib.suppress(KeyError):
            self.style = input_dict["style"]
        with contextlib.suppress(KeyError):
            self.label_style = input_dict["labelStyle"]

    def __repr__(self):
        return f"StreamlitFlowEdge({self.id}, {self.source_node_id}:{self.source_handle_id}->{self.target_node_id}:{self.target_handle_id}, '{self.label}')"
