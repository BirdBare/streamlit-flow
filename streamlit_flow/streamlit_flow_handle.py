from __future__ import annotations

import typing
import uuid


class StreamlitFlowHandle:
    def __init__(
        self,
        position: typing.Literal["top", "bottom", "left", "right"],
        *,
        is_source: bool = True,
        valid_targets: list[typing.Self] | None = None,  # If is None then all targets are valid
        is_target: bool = True,
        valid_sources: list[typing.Self] | None = None,  # If is None then all sources are valid
        style: dict[str, typing.Any] = {},
    ):
        self.id = str(uuid.uuid4())
        self.position = position
        self.is_source = is_source
        self.valid_targets = valid_targets
        self.is_target = is_target
        self.valid_sources = valid_sources

        if style == {}:
            self.style = {}
        else:
            self.style = style

    @typing.overload
    def add_valid_sources(self, *sources: typing.Self): ...

    @typing.overload
    def add_valid_sources(self, *sources: None): ...

    def add_valid_sources(self, *sources: typing.Self | None):
        if None in sources:
            self.valid_sources = None

        else:
            if self.valid_sources is None:
                self.valid_sources = []

            self.valid_sources += [source for source in sources if source is not None]

    @typing.overload
    def add_valid_targets(self, *targets: typing.Self): ...

    @typing.overload
    def add_valid_targets(self, *targets: None): ...

    def add_valid_targets(self, *targets: typing.Self | None):
        if None in targets:
            self.valid_targets = None

        else:
            if self.valid_targets is None:
                self.valid_targets = []

            self.valid_targets += [target for target in targets if target is not None]

    def as_dict(self) -> dict[str, typing.Any]:
        output_dict = {
            "id": self.id,
            "position": self.position,
            "isConnectableStart": self.is_source,
            "isConnectableEnd": self.is_target,
            "valid_target_ids": None if self.valid_targets is None else [handle.id for handle in self.valid_targets],
            "valid_source_ids": None if self.valid_sources is None else [handle.id for handle in self.valid_sources],
            "style": self.style,
        }

        return output_dict

    @classmethod
    def from_dict(cls: type[typing.Self], input_dict: dict[str, typing.Any]) -> typing.Self:

        instance = cls(
            position=input_dict["position"],
            is_source=input_dict["isConnectableStart"],
            valid_targets=input_dict["valid_targets"],
            is_target=input_dict["isConnectableEnd"],
            valid_sources=input_dict["valid_sources"],
            style=input_dict["style"],
        )

        if "id" in input_dict:
            instance.id = input_dict["id"]

        return instance

    def __repr__(self):
        return f"StreamlitFlowHandle({self.id}, {self.position}, {self.is_source}, {self.is_target})"
