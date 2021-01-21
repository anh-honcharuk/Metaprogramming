from lexer_items.automat_match import AutomatMatch
from lexer_items.token_ import MyToken
from lexer_items.type_token import TypeToken


class Punctuation(AutomatMatch):

    def match(self, text, position):
        cur_symbol = text[position]

        if cur_symbol in "{}[]()":
            return MyToken(TypeToken.BRACKET, cur_symbol, position, position + 1)

        if cur_symbol in ",;":
            return MyToken(TypeToken.SEPARATOR, cur_symbol, position, position + 1)

        if cur_symbol == ".":
            return MyToken(TypeToken.DOT, cur_symbol, position, position + 1)

        return None
