from enum import Enum, auto


class TypeToken(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    INT = auto()
    FLOAT = auto()
    DOUBLE = auto()
    LONG = auto()
    HEX = auto()
    BIN = auto()
    CHAR = auto()
    STRING = auto()
    MODIFIER_KEYWORD = auto()
    OPERATOR = auto()
    SEPARATOR = auto()
    WHITESPACE = auto()
    NEW_LINE = auto()
    DOT = auto()
    IDENTIFIER = auto()
    HARD_KEYWORD = auto()
    SOFT_KEYWORD = auto()
    COMMENT = auto()
    MULTILINE_COMMENT = auto()
    SPECIAL_SYMBOL = auto()
    BRACKET = auto()
    ERROR = auto()
