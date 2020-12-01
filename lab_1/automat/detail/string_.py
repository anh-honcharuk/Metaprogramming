from automat.automat_match import AutomatMatch
from automat.utils import Utils
from token_ import MyToken
from type_token import TypeToken


class String(AutomatMatch):

    def match(self, text, position):
        cur_position = position
        state = 0
        while cur_position < len(text):
            cur_symbol = text[cur_position]
            cur_position += 1
            print(state)
            # -----------
            if state == 0:
                if cur_symbol == '"':
                    state = 1
                    continue
                elif cur_symbol == "'":
                    state = 2
                    continue
                else:
                    return None

            if state == 1:
                if cur_symbol == '"':
                    return MyToken(TypeToken.STRING, text[position:cur_position], position, cur_position)
                continue
            if state == 2:
                if not cur_symbol == "'":
                    state = 3
                    continue
                else:
                    return None

            if state == 3:
                if cur_symbol == "'":
                    return MyToken(TypeToken.CHAR, text[position:cur_position], position, cur_position)
                    continue
                else:
                    return None
            # -----------
        if state == 2:
            return MyToken(TypeToken.COMMENT, text[position:cur_position], position, cur_position)

        return None

print(String().match("'g'",0).return_token())