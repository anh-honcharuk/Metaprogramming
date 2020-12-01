from token_ import MyToken
from type_token import TypeToken


class Formatter:
    TYPES = list(TypeToken.INT, TypeToken.FLOAT, TypeToken.DOUBLE, TypeToken.LONG,
                 TypeToken.HEX, TypeToken.BIN, TypeToken.CHAR, TypeToken.STRING)
    KEYWORD_WITH_PARENTHESES = list("if", "while", "when", "catch", "for")

    def __init__(self):
        pass
