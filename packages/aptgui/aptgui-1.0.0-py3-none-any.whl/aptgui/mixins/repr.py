from inspect import isclass, isfunction, ismethod
from itertools import chain

from ..collections import sequence
from ..options import get_option_names


class Repr:
    def __repr__(self) -> str:
        widgets = (
            repr(widget)
            for value in vars(self).values()
            if isinstance(value, sequence)
            for widget in value
        )

        def callable_name_repr(value: object) -> str:
            if ismethod(value):
                return value.__qualname__
            elif isfunction(value) and value.__name__ == "<lambda>":
                return "lambda: '<lambda>'"
            elif isfunction(value) or isclass(value):
                return value.__name__
            else:
                return repr(value)

        options = (
            f"{name}={callable_name_repr(getattr(self, name))}"
            for name in get_option_names(self)
            if hasattr(self, name) and not isinstance(getattr(self, name), sequence)
        )

        return f"{type(self).__name__}({', '.join(chain(widgets, options))})"
