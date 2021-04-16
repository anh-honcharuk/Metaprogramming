from lexer_items.automat_match import AutomatMatch
from lexer_items.token_ import MyToken
from lexer_items.type_token import TypeToken
import re

class SpecialSymbol(AutomatMatch):
    __MAX_LENGTH = 2

    def match(self, text, position):
        result = None
        special_symbols = ("?.", "?:", "..", ":", "::", "->", "!!", "$", "@")
        for i in range(1, min(self.__MAX_LENGTH + 1, len(text) - position + 1)):
            substring = text[position:position + i]
            # print(substring)
            if substring in special_symbols:
                return MyToken(TypeToken.SPECIAL_SYMBOL, substring, position, position + i)
            # if re.match("(\?[.:]?)|\.\.|(:){1,2}|->|!!|\$|@", substring):
            #
            #     result = MyToken(TypeToken.SPECIAL_SYMBOL, substring, position, position + i)

        return result
