from matchers import *
from token_ import *

MATCHERS = [
    operator_dfa,
    number_dfa,
    special_symbol_dfa,
    punctuation_dfa,
    identifier_keyword_dfa,
    whitespace_dfa,
    string_dfa,
    single_line_comment_dfa,
    doc_comment_dfa,
    multiline_comment_dfa
]


class Lexer:
    def __init__(self):
        self.tokens = []

    def tokenize(self, code):
        self.tokens.clear()
        position = 0
        error = None
        while position < len(code):
            to_add = None

            for i in range(len(MATCHERS)):
                matcher = MATCHERS[i]
                temp = matcher(position, code)
                if to_add is None or (temp is not None and temp.end > to_add.end):
                    to_add = temp

            if to_add is not None:
                if error is not None:
                    self.tokens.append(error)
                    error = None
                self.tokens.append(to_add)
                position = to_add.end
                continue
            if error is None:
                error = Token(TokenType.ERROR, position + 1, code[position])
            else:
                error.value += code[position]
                error.end += 1
            position += 1

    # for token in self.tokens:
    #    print(token.to_string())
        return self.tokens
