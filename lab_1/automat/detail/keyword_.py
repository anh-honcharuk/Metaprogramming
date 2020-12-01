from automat.automat_match import AutomatMatch
from automat.utils import Utils
from token_ import MyToken
from type_token import TypeToken

class Keyword (AutomatMatch):

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
            if state == 1:
                if not cur_symbol.isalpha() or cur_symbol.isdigit() or cur_symbol == '_' or cur_symbol == '$':
                    return MyToken( self.get_type( text[position:cur_position - 1] ), text[position:cur_position - 1], position, cur_position - 1 )
        if state == 1:
            return MyToken( self.get_type( text[position:cur_position] ), text[position:cur_position], position, cur_position )

        return None


    def get_type(self, text):
        if text in Utils.HARD_KEYWORDS:
            return Utils.HARD_KEYWORDS
        if text in Utils.SOFT_KEYWORDS:
            return Utils.SOFT_KEYWORDS
        if text in Utils.MODIFIER_KEYWORDS:
            return Utils.MODIFIER_KEYWORDS
        return Utils.IDENTIFIER

print(Keyword().match("as     вы", 0).return_token())
