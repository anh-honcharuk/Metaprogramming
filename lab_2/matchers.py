from utils import *
from token_ import *


def get_type(text):
    if text in HARD_KEYWORDS:
        return TokenType.HARD_KEYWORD
    elif text in SOFT_KEYWORDS:
        return TokenType.SOFT_KEYWORD
    elif text in MODIFIER_KEYWORDS:
        return TokenType.MODIFIER_KEYWORD
    else:
        return TokenType.IDENTIFIER


def identifier_keyword_dfa(position, text):
    cur_position = position
    state = 0
    while cur_position < len(text):
        cur_char = text[cur_position]
        cur_position += 1
        if state == 0:
            if cur_char == '_' or cur_char.isalpha():
                state = 1
            else:
                return None
        elif state == 1:
            if not (cur_char.isalpha() or cur_char.isnumeric() or cur_char == '_' or cur_char == '$'):
                return Token(get_type(text[position:cur_position - 1]), cur_position - 1,
                             text[position:cur_position - 1])

    if state == 1:
        return Token(get_type(text[position:cur_position]), cur_position, text[position:cur_position])


def multiline_comment_dfa(position, text):
    cur_position = position
    state = 0
    while cur_position < len(text):
        cur_char = text[cur_position]
        cur_position += 1
        if state == 0:
            if cur_char == '/':
                state = 1
            else:
                return None
        elif state == 1:
            if cur_char == '*':
                state = 2
            else:
                return None
        elif state == 2:
            if cur_char == '*':
                state = 3
        elif state == 3:
            if cur_char == '/':
                return Token(TokenType.MULTILINE_COMMENT, cur_position, text[position:cur_position])
            else:
                state = 2
    return None


def doc_comment_dfa(position, text):
    cur_position = position
    state = 0
    while cur_position < len(text):
        cur_char = text[cur_position]
        cur_position += 1
        if state == 0:
            if cur_char == '/':
                state = 1
            else:
                return None
        elif state == 1:
            if cur_char == '*':
                state = 2
            else:
                return None
        elif state == 2:
            if cur_char == '*':
                state = 3
            else:
                return None
        elif state == 3:
            if cur_char == '*':
                state = 4
        elif state == 4:
            if cur_char == '/':
                return Token(TokenType.DOC_COMMENT, cur_position, text[position:cur_position])
            else:
                state = 3
    return None


def single_line_comment_dfa(position, text):
    cur_position = position
    state = 0
    while cur_position < len(text):
        cur_char = text[cur_position]
        cur_position += 1
        if state == 0:
            if cur_char == '/':
                state = 1
            else:
                return None
        elif state == 1:
            if cur_char == '/':
                state = 2
            else:
                return None
        elif state == 2:
            if cur_char == '\n':
                return Token(TokenType.COMMENT, cur_position, text[position:cur_position])

    return Token(TokenType.COMMENT, cur_position, text[position:cur_position]) if state == 2 else None


def string_dfa(position, text):
    cur_position = position
    state = 0
    while cur_position < len(text):
        cur_char = text[cur_position]
        cur_position += 1
        if state == 0:
            if cur_char == '"':
                state = 1
            elif cur_char == "'":
                state = 2
            else:
                return None
        elif state == 1:
            if cur_char == '"':
                return Token(TokenType.STRING, cur_position, text[position:cur_position])
        elif state == 2:
            if cur_char != "'":
                state = 3
            else:
                return None
        elif state == 3:
            if cur_char == "'":
                return Token(TokenType.CHAR, cur_position, text[position:cur_position])
            else:
                return None
    return Token(TokenType.COMMENT, cur_position, text[position:cur_position]) if state == 2 else None


def whitespace_dfa(position, text):
    cur_position = position
    state = 0
    while cur_position < len(text):
        cur_char = text[cur_position]
        cur_position += 1
        if state == 0:
            if " \t\r".find(cur_char) != -1:
                state = 1
            elif cur_char == '\n':
                return Token(TokenType.NEW_LINE, cur_position, text[position:cur_position])
            else:
                return None
        elif state == 1:
            if cur_char == '\n':
                return Token(TokenType.NEW_LINE, cur_position, text[position:cur_position])
            elif " \t\r".find(cur_char) == -1:
                return Token(TokenType.WHITESPACE, cur_position - 1, text[position:cur_position - 1])
    if state == 1:
        return Token(TokenType.WHITESPACE, cur_position, text[position:cur_position])
    return None


def number_dfa(position, text):
    cur_position = position
    state = 0
    result = None
    while cur_position < len(text):
        cur_char = text[cur_position]
        cur_position += 1
        if state == 0 or state == 1:
            if cur_char == '0':
                state = 2
                result = Token(TokenType.INT, cur_position, text[position:cur_position])
            elif cur_char.isnumeric():
                state = 4
                result = Token(TokenType.INT, cur_position, text[position:cur_position])
            elif cur_char == '.':
                state = 6
            else:
                return None
        elif state == 2:
            if cur_char.isnumeric() or cur_char == '_':
                state = 3
            elif cur_char == "L":
                return Token(TokenType.LONG, cur_position, text[position:cur_position])
            elif cur_char == '.':
                state = 6
            elif cur_char == "F" or cur_char == "f":
                return Token(TokenType.FLOAT, cur_position, text[position:cur_position])
            else:
                return result
        elif state == 3:
            if cur_char == "F" or cur_char == "f":
                return Token(TokenType.FLOAT, cur_position, text[position:cur_position])
            elif cur_char.isnumeric() or cur_char == '_':
                pass
            else:
                return result
        elif state == 4:
            if cur_char.isnumeric() or cur_char == '_':
                result = Token(TokenType.INT, cur_position, text[position:cur_position])
            elif cur_char == "L":
                return Token(TokenType.LONG, cur_position, text[position:cur_position])
            elif cur_char == "F" or cur_char == "f":
                return Token(TokenType.FLOAT, cur_position, text[position:cur_position])
            elif cur_char == '.':
                state = 6
            else:
                return result
        elif state == 6:
            if cur_char.isnumeric():
                result = Token(TokenType.DOUBLE, cur_position, text[position:cur_position])
                state = 7
            else:
                return result
        elif state == 7:
            if cur_char.isnumeric() or cur_char == '_':
                result = Token(TokenType.DOUBLE, cur_position, text[position:cur_position])
            elif cur_char == "F" or cur_char == "f":
                return Token(TokenType.FLOAT, cur_position, text[position:cur_position])
            else:
                return result
    return result


def operator_dfa(position, text):
    cur_position = position
    state = 0
    result = None
    while cur_position < len(text):
        cur_char = text[cur_position]
        cur_position += 1
        if state == 0:
            if cur_char == '&':
                state = 1
            elif cur_char == '|':
                state = 2
            elif "<>*/%".find(cur_char) != -1:
                state = 3
                result = Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            elif cur_char == '!' or cur_char == '=':
                state = 4
                result = Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            elif cur_char == '+':
                state = 5
                result = Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            elif cur_char == '-':
                state = 6
                result = Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            else:
                return None
        elif state == 1:
            if cur_char == '&':
                return Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            else:
                return None
        elif state == 2:
            if cur_char == '|':
                return Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            else:
                return None
        elif state == 3:
            if cur_char == '=':
                return Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            else:
                return result
        elif state == 4:
            if cur_char == '=':
                state = 3
                result = Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            else:
                return result
        elif state == 5:
            if cur_char == '+' or cur_char == '=':
                return Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            else:
                return result
        elif state == 6:
            if cur_char == '-' or cur_char == '=':
                result = Token(TokenType.OPERATOR, cur_position, text[position:cur_position])
            else:
                return result
        else:
            return result
    return result


def punctuation_dfa(position, text):
    cur_char = text[position]

    if "{}[]()".find(cur_char) != -1:
        return Token(TokenType.BRACKET, position + 1, text[position:position + 1])
    if ",;".find(cur_char) != -1:
        return Token(TokenType.SEPARATOR, position + 1, text[position:position + 1])
    if cur_char == '.':
        return Token(TokenType.DOT, position + 1, text[position:position + 1])
    return None


def special_symbol_dfa(position, text):
    special_symbols = ("?.", "?:", "..", ":", "::", "->", "!!", "$", "@")
    result = None
    if text[position] in special_symbols:
        result = Token(TokenType.SPECIAL_SYMBOL, position + 1, text[position])
    if position + 1 < len(text) and text[position:position + 2] in special_symbols:
        result = Token(TokenType.SPECIAL_SYMBOL, position + 2, text[position:position + 2])
    return result
