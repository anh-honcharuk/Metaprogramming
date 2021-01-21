from enum import Enum


class TokenType(Enum):
    INT = 0,
    FLOAT = 1,
    DOUBLE = 2,
    LONG = 3,
    HEX = 4,
    BIN = 5,
    IDENTIFIER = 6,
    HARD_KEYWORD = 7,
    SOFT_KEYWORD = 8,
    MODIFIER_KEYWORD = 9,
    OPERATOR = 10,
    SEPARATOR = 11,
    DOT = 12,
    BRACKET = 13,
    CHAR = 14,
    STRING = 15,
    COMMENT = 16,
    MULTILINE_COMMENT = 17,
    WHITESPACE = 18,
    NEW_LINE = 19,
    SPECIAL_SYMBOL = 20,
    ERROR = 21,
    DOC_COMMENT = 22


class Token:
    def __init__(self, token_type, end, value=None):
        self.token_type = token_type
        self.end = end
        self.value = value

    def to_string(self):
        if self.value is not None:
            return "{" + self.token_type.name + " | " + self.value + "}"
