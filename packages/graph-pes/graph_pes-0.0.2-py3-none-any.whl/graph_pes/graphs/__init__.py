from __future__ import annotations

from typing import Final

from . import keys
from .graph_typing import (
    AtomicGraph,
    AtomicGraphBatch,
    LabelledBatch,
    LabelledGraph,
)
from .operations import with_nice_repr

__all__ = [
    "AtomicGraph",
    "AtomicGraphBatch",
    "LabelledBatch",
    "LabelledGraph",
    "keys",
    "with_nice_repr",
    "DEFAULT_CUTOFF",
]

DEFAULT_CUTOFF: Final[float] = 5.0
"""The default cutoff radius for models."""
