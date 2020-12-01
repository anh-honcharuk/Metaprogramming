from automat.automat_match import AutomatMatch
from automat.utils import Utils
from token_ import MyToken
from type_token import TypeToken


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
print(Punctuation().match(";{{{",0).return_token())