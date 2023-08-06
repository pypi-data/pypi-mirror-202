from dataclasses import dataclass, field
from enum import Flag, auto
from typing import List, Tuple


class DiffMode(Flag):
    ABSOLUTE = auto()
    RELATIVE = auto()


class Units(Flag):
    MM = auto()
    INCH = auto()


@dataclass
class ToolJobSegment:
    diff_mode: DiffMode
    units: Units
    holes: List[Tuple[float, float]] = field(default_factory=list)


@dataclass
class ToolJob:
    diameter: float
    segments: List[ToolJobSegment] = field(default_factory=list)


__all__ = ['DiffMode', 'Units', 'ToolJobSegment', 'ToolJob']
