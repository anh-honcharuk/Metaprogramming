from enum import *


class QuadrangleType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
    RECTANGLE = auto()
    SQUARE = auto()
    PARALLELOGRAM = auto()
    DIAMOND = auto()
    TRAPEZOID = auto()
    RECTANGULAR_TRAPEZOID = auto()
    EQUILATERAL_TRAPEZOID = auto()
