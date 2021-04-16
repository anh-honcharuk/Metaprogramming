from lexer_items.automat_match import AutomatMatch

from lexer_items.token_ import MyToken
from lexer_items.type_token import TypeToken


class Keyword(AutomatMatch):
    HARD_KEYWORDS = [
        "as", "break", "catch", "class", "continue", "do", "else", "false", "for", "fun", "if", "in", "interface", "is",
        "null", "object", "package", "return", "super", "this", "throw", "true", "try", "typealias", "typeof",
        "val", "var", "when", "while"
    ]

    SOFT_KEYWORDS = [
        "by", "constructor", "delegate", "dynamic", "field", "file", "finally", "get", "import", "init",
        "it", "param", "property", "receiver", "set", "setparam", "where"
    ]

    MODIFIER_KEYWORDS = [
        "actual", "abstract", "annotation", "companion", "const", "crossinline", "data", "enum", "expect",
        "external", "final", "infix", "inline", "inner", "internal", "lateinit", "noinline", "open", "operator",
        "out", "override", "private", "protected", "public", "reified", "sealed", "suspend", "tailrec", "vararg"
    ]
    def match(self, text, position):

        cur_position = position
        state = 0
        result = None
        while cur_position < len(text):
            cur_symbol = text[cur_position]
            cur_position += 1
            if state == 0:
                if cur_symbol == '_' or cur_symbol.isalpha():
                    state = 1
                else:
                    return None
                continue
            if state == 1:
                if not cur_symbol.isalpha() or cur_symbol.isdigit() or cur_symbol == '_' or cur_symbol == '$':
                    return MyToken( self.get_type(text[position:cur_position - 1]), text[position:cur_position - 1], position, cur_position - 1 )
        if state == 1:
            return MyToken(self.get_type( text[position:cur_position]), text[position:cur_position], position, cur_position )

        return None


    def get_type(self, text):
        if text in self.HARD_KEYWORDS:
            return TypeToken.HARD_KEYWORD
        if text in self.SOFT_KEYWORDS:
            return TypeToken.SOFT_KEYWORD
        if text in self.MODIFIER_KEYWORDS:
            return TypeToken.MODIFIER_KEYWORD
        return TypeToken.IDENTIFIER
