from collections.abc import Awaitable, Callable
from enum import Enum
from inspect import get_annotations
from typing import TypeAlias, TypeGuard, TypeVar, Union


class ReprEnum(Enum):
    def __repr__(self) -> str:
        return f"{type(self).__name__}.{self._name_}"


class Anchor(ReprEnum):
    TOP = "n"
    BOTTOM = "s"
    LEFT = "w"
    RIGHT = "e"
    TOPLEFT = "nw"
    TOPRIGHT = "ne"
    BOTTOMLEFT = "sw"
    BOTTOMRIGHT = "se"
    TOPBOTTOM = "ns"
    LEFTRIGHT = "we"
    TOPLEFTRIGHT = "nwe"
    BOTTOMLEFTRIGHT = "swe"
    TOPLEFTBOTTOM = "nws"
    TOPRIGHTBOTTOM = "nes"
    CENTER = "center"


class Justify(ReprEnum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class Mode(ReprEnum):
    DETERMINATE = "determinate"
    INDETERMINATE = "indeterminate"


class Orientation(ReprEnum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class Sticky(ReprEnum):
    CENTER = ""
    TOP = "n"
    BOTTOM = "s"
    LEFT = "w"
    RIGHT = "e"
    TOPLEFT = "nw"
    TOPRIGHT = "ne"
    BOTTOMLEFT = "sw"
    BOTTOMRIGHT = "se"
    TOPBOTTOM = "ns"
    LEFTRIGHT = "we"
    TOPLEFTRIGHT = "nwe"
    BOTTOMLEFTRIGHT = "swe"
    TOPLEFTBOTTOM = "nws"
    TOPRIGHTBOTTOM = "nes"
    ALL = "nswe"


class WidgetState(ReprEnum):
    NORMAL = "normal"
    DISABLED = "disabled"
    READONLY = "readonly"


class WindowState(ReprEnum):
    NORMAL = "normal"
    MINIMIZED = "iconic"
    MAXIMIZED = "zoomed"
    FULLSCREEN = "fullscreen"
    WITHDRAWN = "withdrawn"


Distance: TypeAlias = int
AxisDistance: TypeAlias = Union[
    Distance,
    tuple[Distance, Distance],
]
CardinalDistance: TypeAlias = Union[
    Distance,
    tuple[Distance, Distance],
    tuple[Distance, Distance, Distance],
    tuple[Distance, Distance, Distance, Distance],
]


CallbackArg = TypeVar("CallbackArg")
Callback: TypeAlias = Callable[[CallbackArg], Awaitable[None] | None]


def horizontal_axis(card_dist: CardinalDistance) -> AxisDistance:
    if isinstance(card_dist, tuple):
        if _is_4_tuple(card_dist):
            return card_dist[0], card_dist[2]
        elif _is_3_tuple(card_dist):
            return card_dist[0], card_dist[2]
        else:
            return card_dist[0]
    else:
        return card_dist


def vertical_axis(card_dist: CardinalDistance) -> AxisDistance:
    if isinstance(card_dist, tuple):
        if _is_4_tuple(card_dist):
            return card_dist[1], card_dist[3]
        elif _is_3_tuple(card_dist):
            return card_dist[1]
        else:
            return card_dist[1]
    else:
        return card_dist


def _is_3_tuple(
    value: tuple[Distance, ...]
) -> TypeGuard[tuple[Distance, Distance, Distance]]:
    return len(value) == 3


def _is_4_tuple(
    value: tuple[Distance, ...]
) -> TypeGuard[tuple[Distance, Distance, Distance, Distance]]:
    return len(value) == 4


def get_option_names(object_: object) -> tuple[str, ...]:
    return tuple(get_annotations(type(object_).__init__).keys())
