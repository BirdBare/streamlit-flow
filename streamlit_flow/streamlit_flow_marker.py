from __future__ import annotations

import typing
import uuid


class StreamlitFlowMarker:
    def __init__(
        self,
        type: typing.Literal["arrow", "arrowclosed"],
        *,
        color: str | None = None,
        stroke_width: int | None = None,
    ):
        self.id = str(uuid.uuid4())
        self.type = type
        self.color = color
        self.stroke_width = stroke_width

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": self.id,
            "type": self.type,
            "color": self.color,
            "strokeWidth": self.stroke_width,
        }

        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:

        instance = cls(
            type=input_dict["type"],
            color=input_dict["color"],
            stroke_width=input_dict["strokeWidth"],
        )

        if "id" in input_dict:
            instance.id = input_dict["id"]

        return instance

    def __repr__(self):
        return f"StreamlitFlowMarker({self.type}, {self.color}, {self.stroke_width})"
