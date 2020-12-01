from automat.automat_match import AutomatMatch
from token_ import MyToken
from type_token import TypeToken


class Comment(AutomatMatch):

    def match(self, text, position):
        cur_position = position
        state = 0
        result = None
        while cur_position < len(text):
            cur_symbol = text[cur_position]
            cur_position += 1
            if state == 0:
                if cur_symbol == '/':
                    state = 1
                    continue
                else:
                    return None
            if state == 1:
                if cur_symbol == '/':
                    state = 2
                    continue
                else:
                    return None
            if state == 2:
                if cur_symbol == '\n':
                    return MyToken(TypeToken.COMMENT, text[position:cur_position], position, cur_position)
        return None

print(Comment().match("//fj,jvn,\n", 0).return_token())