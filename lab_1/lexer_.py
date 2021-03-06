from lexer_items.token_ import MyToken
from lexer_items.type_token import TypeToken
from lexer_items.utils_ import Utils


class Lexer:

    def tokenize(self, text):
        tokens = []
        position = 0
        error = None

        while position < len(text):
            to_add = None

            for matcher in Utils.MATCHERS:

                pos = position
                temp = matcher.match(text, pos)

                if to_add == None or (not temp == None and temp.get_end() > to_add.get_end()):
                    to_add = temp


            if not to_add == None:
                if not error == None:
                    tokens.append(error)
                    error = None

                tokens.append(to_add)
                position = to_add.get_end()
                continue

            if error == None:
                error = MyToken(TypeToken.ERROR, text[position], position, position + 1)
            else:
                error.append(text[position])
            position += 1

        return tokens


