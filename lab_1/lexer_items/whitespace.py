from lexer_items.automat_match import AutomatMatch
from lexer_items.token_ import MyToken
from lexer_items.type_token import TypeToken


class Whitespace (AutomatMatch):

    def match(self, text, position):
        cur_position = position
        state = 0
        result = None
        while cur_position < len(text):
            cur_symbol = text[cur_position]
            cur_position += 1
            if state == 0:
                if cur_symbol in " \t\r":
                    state = 1
                    continue
                elif cur_symbol in "\n":
                    return MyToken(TypeToken.NEW_LINE, text[position:cur_position], position, cur_position)
                else:
                    return None
            if state == 1:
                if cur_symbol in "\n":
                    return MyToken(TypeToken.NEW_LINE, text[position:cur_position], position, cur_position)

                elif not cur_symbol in " \t\r":
                    return MyToken(TypeToken.WHITESPACE, text[position:(cur_position - 1)], position, cur_position - 1)

        if state == 1:
            return MyToken(TypeToken.WHITESPACE, text[position:cur_position], position, cur_position)

        return result

