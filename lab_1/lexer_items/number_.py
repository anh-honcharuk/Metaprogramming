from lexer_items.automat_match import AutomatMatch
from lexer_items.token_ import MyToken
from lexer_items.type_token import TypeToken


class Number (AutomatMatch):

    def match(self, text, position):
        cur_position = position
        state = 0
        result = None
        while cur_position < len(text):
            cur_symbol = text[cur_position]
            cur_position += 1
            # print(cur_position, 'pos')
            if state == 0:
                # print(state)
                # print(cur_symbol.isdigit())
                # print(cur_symbol)
                if cur_symbol == '0':
                    state = 2
                    result = MyToken( TypeToken.INT, text[position:cur_position], position, cur_position )
                elif cur_symbol.isdigit():
                    state = 4
                    # print( cur_symbol.isdigit() )

                    result = MyToken( TypeToken.INT, text[position:cur_position], position, cur_position )
                elif cur_symbol == '.':
                    state = 6
                else:
                    return None
                # print(state , "njsndjlf")
                continue
            if state == 1:
                if cur_symbol == '0':
                    state = 2
                    result = MyToken( TypeToken.INT, text[position:cur_position], position, cur_position )
                elif cur_symbol.isdigit():
                    state = 4
                    result = MyToken( TypeToken.INT, text[position:cur_position], position, cur_position )
                elif cur_symbol == '.':
                    state = 6
                else:
                    return None

                continue
            #-------------------
            if state == 2:
                # print( state, "2" )
                if cur_symbol.isdigit() or cur_symbol == '_':
                    state = 3
                elif cur_symbol == 'L':
                    state = 4
                    return MyToken( TypeToken.LONG, text[position:cur_position], position, cur_position )
                elif cur_symbol == '.':
                    state = 6
                elif cur_symbol == 'F' or cur_symbol == 'f':
                    return MyToken( TypeToken.FLOAT, text[position:cur_position], position, cur_position )
                else:
                    return result
                # print(state, "2")
                continue
            if state == 3:
                # print(state, "3", cur_symbol.isdigit(), cur_symbol)
                if cur_symbol == 'F' or cur_symbol == 'f':
                    state = 2
                    result = MyToken(TypeToken.FLOAT, text[position:cur_position], position, cur_position)

                elif cur_symbol.isdigit() or cur_symbol == '_':
                    continue
                    # print('pass')
                else:
                    return result
                # print( state, "3" )
            if state == 4:
                if cur_symbol.isdigit() or cur_symbol == '_':
                    result = MyToken( TypeToken.INT, text[position:cur_position], position, cur_position )
                    continue
                elif cur_symbol == 'L':
                    return MyToken( TypeToken.LONG, text[position:cur_position], position, cur_position )
                elif cur_symbol == 'F' or cur_symbol == 'f':
                    return MyToken( TypeToken.FLOAT, text[position:cur_position], position, cur_position )
                elif cur_symbol == '.':
                    state = 6
                    continue
                else:
                    return result

            if state == 6:
                if cur_symbol.isdigit():
                    state = 7
                    result = MyToken( TypeToken.DOUBLE, text[position:cur_position], position, cur_position )
                    continue
                else:
                    return result

            if state == 7:
                if cur_symbol.isdigit() or cur_symbol == '_':
                    result = MyToken( TypeToken.DOUBLE, text[position:cur_position], position, cur_position )
                elif cur_symbol == 'F' or cur_symbol == 'f':
                    return MyToken( TypeToken.FLOAT, text[position:cur_position], position, cur_position )
                else:
                    return result

        return result
