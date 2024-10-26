from collections.abc import Iterable, Iterator, Sequence
from itertools import chain
from typing import TYPE_CHECKING, TypeVar, overload

if TYPE_CHECKING:
    from typing import Self

T = TypeVar("T", covariant=True)


class sequence(Sequence[T]):
    def __init__(self, values: Iterable[T] = tuple(), /):
        self.__values = tuple(values)

    def __add__(self, values: T | Iterable[T], /) -> "Self":
        if not isinstance(values, Iterable) or isinstance(values, str):
            values = (values,)  # type: ignore[assignment]

        return type(self)(chain(self, values))  # type: ignore[arg-type]

    def __sub__(self, values: T | Iterable[T], /) -> "Self":
        if not isinstance(values, Iterable) or isinstance(values, str):
            values = (values,)  # type: ignore[assignment]

        values = set(values)  # type: ignore[arg-type]
        return type(self)(value for value in self if value not in values)

    def __contains__(self, value: object, /) -> bool:
        return value in self.__values

    @overload
    def __getitem__(eslf, key: int, /) -> T: ...

    @overload
    def __getitem__(self, key: slice, /) -> "Self": ...

    def __getitem__(self, key: int | slice, /) -> object:
        return self.__values[key]

    def __iter__(self) -> Iterator[T]:
        return iter(self.__values)

    def __len__(self) -> int:
        return len(self.__values)

    def __repr__(self) -> str:
        return type(self).__name__ + "(" + ", ".join(map(repr, self.__values)) + ")"


class setsequence(sequence[T]):
    def __init__(self, values: Iterable[T] = tuple(), /):
        super().__init__(dict.fromkeys(values).keys())
