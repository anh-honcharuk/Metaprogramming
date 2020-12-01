from automat.automat_match import AutomatMatch
from token_ import MyToken
from type_token import TypeToken


class MultiLineComment(AutomatMatch):

    def match(self, text, position):
        cur_position = position
        state = 0
        while cur_position < len(text):
            cur_symbol = text[cur_position]
            cur_position += 1
            print(cur_symbol)
            print(len(text))
            if state == 0:
                if cur_symbol == '/':
                    state = 1
                    print('/')
                else:
                    return None
                continue
            if state == 1:
                if cur_symbol == '*':
                    state = 2
                else:
                    return None
                continue
            if state == 2:
                if cur_symbol == '*':
                    state = 3
                continue
            if state == 3:
                if cur_symbol == '/':
                    return MyToken( TypeToken.MULTILINE_COMMENT, text[position:cur_position], position, cur_position );
            else:
                state = 2

        return None

print(MultiLineComment().match("/*fdvdfv*/", 0).return_token())
