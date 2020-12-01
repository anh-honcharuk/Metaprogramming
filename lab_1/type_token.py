import enum
#import Enum

class TypeToken(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
    INT = enum.auto()
    FLOAT = enum.auto()
    DOUBLE = enum.auto()
    LONG = enum.auto()
    HEX = enum.auto()
    BIN = enum.auto()
    CHAR = enum.auto()
    STRING = enum.auto()
    MODIFIER_KEYWORD = enum.auto()
    OPERATOR = enum.auto()
    SEPARATOR = enum.auto()
    WHITESPACE = enum.auto()
    NEW_LINE = enum.auto()
    DOT = enum.auto()
    IDENTIFIER = enum.auto()
    HARD_KEYWORD = enum.auto()
    SOFT_KEYWORD = enum.auto()
    COMMENT = enum.auto()
    MULTILINE_COMMENT = enum.auto()
    SPECIAL_SYMBOL = enum.auto()
    BRACKET = enum.auto()
    ERROR = enum.auto()
