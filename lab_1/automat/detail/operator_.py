from automat.automat_match import AutomatMatch

from token_ import MyToken
from type_token import TypeToken


class Operator(AutomatMatch):

    def match(self, text, position):
        cur_position = position
        state = 0
        result = None
        while cur_position < len(text):
            cur_symbol = text[cur_position]
            cur_position += 1

            if state == 0:
                if cur_symbol == '&':
                    state = 1
                elif cur_symbol == '|':
                    state = 2
                elif cur_symbol in "<>*/%":
                    state = 3
                    result = MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                elif cur_symbol == '!' or cur_symbol == '=':
                    state = 4
                    result = MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                elif cur_symbol == '+':
                    state = 5
                    result = MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                elif cur_symbol == '-':
                    state = 6
                    result = MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                else:
                     return None
                continue
            if state == 1:
                if cur_symbol == '&':
                    return MyToken( TypeToken.OPERATOR, text[position: cur_position], position, cur_position )
                else:
                     return None
            if state == 2:
                if cur_symbol =='|':
                    return MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                else:
                    return None

            if state == 3:
                if cur_symbol == '=':
                    return MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                else:
                    return result

            if state == 4:
                if cur_symbol == '=':
                    state = 3
                    result = MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                    continue
                else:
                    return result
            if state == 5:
                if cur_symbol == '+' or cur_symbol == '=':
                    return MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                else:
                    return result
            if state == 6:
                if cur_symbol == '-' or cur_symbol == '=':
                    return MyToken( TypeToken.OPERATOR, text[position:cur_position], position, cur_position )
                else:
                    return result
            else:
                return result

        return result

print(Operator().match('!=', 0).return_token())