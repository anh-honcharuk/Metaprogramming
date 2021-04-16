import re

from formatter.logger import Logger
from lexer_items.type_token import TypeToken
class Style:
    # Tabs and Idents
    use_tab_character = False
    smart_tabs = False

    tab_size = 4
    indent = 4
    continuation_indent = 8

    keep_indents_on_empty_lines = False

    # Spaces
    # Before Parentheses
    if_parentheses = True
    for_parentheses = True
    while_parentheses = True
    catch_parentheses = True
    when_parentheses = True

    # Around Operators
    assignment_operators = True
    logical_operators = True
    equality_operators = True
    relational_operators = True
    additive_operators = True
    multiplicative_operators = True

    unary_operators = False
    range_operators = False

    # Other
    before_comma = False
    after_comma = True
    before_colon = False
    after_colon = True
    # before_colon_in_new_type_definition = True
    # after_colon_in_new_type_definition = True
    # in_simple_one_line_methods = True
    around_arrow = True
    # around_arrow_in_when_clause = False # True
    before_lambda_arrow = True

    # Wrapping and Braced

    # Blank Lines
    # Keep Maximum Blank Lines
    blank_lines = 2
    in_declaration = 2
    in_code = 2
    before_end_brace = 2

    # Minimum Blank Lines
    # after_class_header = 0
    # around_when_branches_with = 0



class Formatter:
    TYPES = [TypeToken.INT, TypeToken.FLOAT,
            TypeToken.DOUBLE, TypeToken.LONG, TypeToken.HEX, TypeToken.BIN, TypeToken.CHAR, TypeToken.STRING]
    KEYWORD_WITH_PARENTHESES = ["if", "while", "when", "catch", "for"]

    def __init__(self):
        self.code_style = Style()
        self.logger = None

    def format_tokens(self, origin_tokens, file_name):
        result = ''#------------
        need_space = False
        line = 1
        blank_line = 0
        indent_level = 0
        self.logger = Logger(file_name)


        for i in range(len(origin_tokens)):
            # print(i, 88888888888888888)
            cur_token = origin_tokens[i]

            if cur_token.type == TypeToken.HARD_KEYWORD:
                if (need_space):
                    result += ' '
                result += cur_token.value
                if cur_token.value in self.KEYWORD_WITH_PARENTHESES:
                    if self.keyword_parentheses(cur_token.value, self.code_style):
                        result += ' '
                    need_space = False
                else:
                    result += ' '
                    need_space = False

            elif cur_token.type == TypeToken.SOFT_KEYWORD or cur_token.type == TypeToken.MODIFIER_KEYWORD:
                result += cur_token.value + ' '
                need_space = False


            elif cur_token.type.name == TypeToken.BRACKET.name:

                if cur_token.value == "{":
                    indent_level += 1

                    if i + 1 >= len(origin_tokens) or not origin_tokens[i + 1].get_type() == TypeToken.NEW_LINE:
                        if need_space:
                            result += " " + cur_token.get_value() + '\n'
                        else:
                            result += cur_token.get_value() + '\n'
                    else:
                        result += cur_token.get_value()
                elif cur_token.value == "}":
                    indent_level -= 1
                    # print( 3 )
                    if indent_level < 0:
                        # print(1)
                        indent_level = 0
                    if not (i - 1 > -1 and origin_tokens[i - 1].get_type() == TypeToken.NEW_LINE) and not (i - 2 > -1 and origin_tokens[i - 2].get_type() == TypeToken.NEW_LINE):
                        result += '\n'
                        # print( 2)
                        self.logger.write_error(line, "need new line before closing braces")

                    result += cur_token.get_value()
                    if (i + 1 < len(origin_tokens) and re.match("else|catch|finally|\\)", origin_tokens[i + 1].get_value())) or (i + 2 < len(origin_tokens) and re.match("else|catch|finally|\\)", origin_tokens[i + 2].get_value())):
                        result += ' '
                    elif not (i + 1 < len(origin_tokens) and origin_tokens[i + 1].get_type() == TypeToken.NEW_LINE) and not (i + 2 < len(origin_tokens) and origin_tokens[i + 2].get_type() == TypeToken.NEW_LINE):
                        result += '\n'

                    need_space = False


                elif cur_token.value == "(":
                    # print('55555555555555555555555555')
                    if need_space:
                        result += " " + "("
                    else:
                        result += "("

                    need_space = False

                elif cur_token.value == ")":
                    if result[len(result) - 1] == " ":
                        result = result[0:-1] + cur_token.get_value()

                    else:
                        result += cur_token.get_value()

                    need_space = True

                elif cur_token.value == "[":

                    result += cur_token.get_value()
                    need_space = False

                elif cur_token.value == "]":

                    result += cur_token.get_value()
                    need_space = True

            # -------------------------

            elif cur_token.get_type() == TypeToken.IDENTIFIER:

                if need_space:
                    result += " " + cur_token.get_value()

                else:
                    result += cur_token.get_value()
                need_space = True


            elif cur_token.get_type() == TypeToken.OPERATOR:

                if self.operator_spaces(cur_token.get_value(), self.code_style):
                    if need_space:
                        result += " " + cur_token.get_value() + " "
                    else:
                        result += cur_token.get_value() + " "
                else:
                    result += cur_token.get_value()
                need_space = False


            elif cur_token.get_type().name == TypeToken.SEPARATOR.name:
                if cur_token.get_value() == ",":

                    if need_space and self.code_style.before_comma:
                        result += " "
                    result += cur_token.get_value()
                    if self.code_style.after_comma:
                        result += " "

                    need_space = False
                else:
                    result += cur_token.get_value()
                    need_space = False

            elif cur_token.get_type() == TypeToken.DOT:
                result += cur_token.get_value()
                need_space = False


            elif cur_token.get_type() == TypeToken.SPECIAL_SYMBOL:
                if cur_token.get_value() == "->":

                    if self.code_style.around_arrow:

                        if not result[len(result) - 1] == " ":
                            result += " " + cur_token.get_value() + " "
                        else:
                            result += cur_token.get_value() + " "
                        need_space = False
                    else:
                        result += cur_token.get_value()



                elif cur_token.get_value() == ":":
                    if self.code_style.before_colon and need_space:
                        result += " "
                    result += cur_token.get_value()
                    if self.code_style.after_colon:
                        result += " "
                    need_space = False


                elif cur_token.get_value() == ".." :
                    if self.code_style.range_operators:
                        if need_space:
                            result += " " + cur_token.get_value() + " "
                        else:
                            result += cur_token.get_value() + " "
                        need_space = False
                    else:
                        result += cur_token.get_value()
                else:
                    result += cur_token.get_value()
            elif cur_token.get_type() in self.TYPES:
                result += cur_token.get_value()
                need_space = True
            elif cur_token.get_type() == TypeToken.MULTILINE_COMMENT:
                result += cur_token.get_value()
            elif cur_token.get_type() == TypeToken.NEW_LINE:
                if i + 1 < len(origin_tokens) and origin_tokens[i + 1].get_value() == "{" or i + 2 < len(origin_tokens) and origin_tokens[i + 2].get_value() == "{":
                    result += ' '
                    self.logger.write_error(line, "redundant new line before bracket {" )
                elif i + 1 < len(origin_tokens) and origin_tokens[i + 1].get_value() == "}" or i + 2 < len(origin_tokens) and origin_tokens[i + 2].get_value() == "}":
                    result += cur_token.get_value()

                else:
                    if i - 1 > -1 and origin_tokens[i - 1].get_type() == TypeToken.NEW_LINE:

                        blank_line += 1
                    else:

                        blank_line = 0
                    if blank_line < self.code_style.blank_lines:
                        result += cur_token.get_value()
                    self.logger.write_error(line, "max number of blank lines " + str(self.code_style.blank_lines))
                    line += 1

                need_space = False
            elif cur_token.get_type().name == TypeToken.WHITESPACE.name:
                if result[-1] == '\n':
                    result += cur_token.get_value()
                    need_space = False
                elif not need_space:

                    self.logger.write_error(line, "redundant whitespace");
                    need_space = False

                else:
                    result += cur_token.get_value()
                    need_space = False
            elif not cur_token.get_type().name == TypeToken.WHITESPACE.name:
                result += cur_token.get_value()
                need_space = False
            else:
                result += cur_token.get_value()
            # print(result)

        return result



    def keyword_parentheses(self, val, format_settings):
        if val == "if":
            return self.code_style.if_parentheses
        if val == "for":
            return self.code_style.for_parentheses
        if val == "when":
            return self.code_style.while_parentheses
        if val == "catch":
            return self.code_style.catch_parentheses
        if val == "while":
            return self.code_style.when_parentheses

        return False


    def operator_spaces(self, val, code_style):
        if re.match("=|\\+=|-=|\\*=|/=", val):
            return self.code_style.assignment_operators
        if re.match("&&|\\|\\|", val):
            return self.code_style.logical_operators
        if re.match("==|!=", val):
            return self.code_style.equality_operators
        if re.match("<|>|<=|>=", val):
            return self.code_style.relational_operators
        if re.match("[+\\-]", val):
            return self.code_style.additive_operators
        if re.match("[*/%]", val):
            return self.code_style.multiplicative_operators
        if re.match("!|-|\\+\\+|--", val):
            return self.code_style.unary_operators
        return False
