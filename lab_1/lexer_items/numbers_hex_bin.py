from lexer_items.automat_match import AutomatMatch
from lexer_items.token_ import MyToken
from lexer_items.type_token import TypeToken
import re


class NumberHexBin(AutomatMatch):
    __MIN_LENGTH = 3

    def match(self, text, position):
        cur_position = position
        res_position = position
        type_ = ''

        if len(text) - position < self.__MIN_LENGTH:
            # print( type_ )
            return None

        if re.match("[-+]?0[xX].?", text[position:position + self.__MIN_LENGTH]):
            type_ = TypeToken.HEX
            # ------------
        elif re.match("[-+]?0[bB].?", text[position:position + self.__MIN_LENGTH]):
            type_ = TypeToken.BIN
            # ------------
        else:
            # print( type_ )
            return None
        # print(type_)
        while cur_position < len(text):
            cur_position += 1
            if type_ == TypeToken.HEX and re.match("[-+]?0[xX][0-9a-fA-F]+([eE]([-+]?[0-9]+)?)?", text[position:cur_position]):
                res_position = cur_position
                # ------------
            if type_ == TypeToken.BIN and re.match("[-+]?0[bB][01]+([eE]([-+]?[0-9]+)?)?", text[position:cur_position]):
                res_position = cur_position
                # ------------
        if res_position != position:
            return MyToken(type_, text[position:res_position], position, res_position)

        return None
