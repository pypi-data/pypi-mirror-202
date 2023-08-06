import functools
import typing as t

import pyqtgraph as pg
from pkg_resources import parse_version
from pyqtgraph.parametertree import registerParameterType
from pyqtgraph.parametertree.parameterTypes import actiongroup as ag

parsed = parse_version(pg.__version__)
T = t.TypeVar("T")

__all__ = ["ActionGroupParameter", "pd", "requires_pandas"]

if parsed < parse_version("0.13.1"):
    raise ImportError("pyqtgraph >= 0.13.1 is required")

try:
    import pandas as pd

    def requires_pandas(obj: T) -> T:
        return obj

except ImportError:
    pd = None

    def requires_pandas(obj: T) -> T:
        @functools.wraps(obj)
        def wrapper(*args, **kwargs):
            raise ImportError(f"The `pandas` dependency must be installed to use {obj}")

        return wrapper


if not hasattr(ag, "ActionGroupParameter"):
    # Make compatible with 0.13.2 definition
    class ActionGroupParameter(ag.ActionGroup):
        sigActivated = pg.QtCore.Signal(object)

        def activate(self):
            self.sigActivated.emit(self)
            self.emitStateChanged("activated", None)

    registerParameterType("_actiongroup", ActionGroupParameter, override=True)

else:
    ActionGroupParameter = ag.ActionGroupParameter
