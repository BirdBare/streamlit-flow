from __future__ import annotations

import typing
import uuid


class Marker:
    def __init__(
        self,
        type: typing.Literal["arrow", "arrowclosed"],
        *,
        color: str | None = None,
        stroke_width: int | None = None,
    ):
        self.id = uuid.uuid4()
        self.type = type
        self.color = color
        self.stroke_width = stroke_width

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": str(self.id),
            "type": self.type,
            "color": self.color,
            "strokeWidth": self.stroke_width,
        }

        return output_dict

    def __eq__(self, value) -> bool:
        try:
            return self.id == value.id
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self):
        return f"StreamlitFlowMarker({self.type}, {self.color}, {self.stroke_width})"
