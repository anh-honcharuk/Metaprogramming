from lexer_ import Lexer, TokenType
from enum import Enum
import os
import logging
import re


class CCFType(Enum):
    FIX = 0,
    VERIFY = 1

class FileWalkType(Enum):
    FILE = 0,
    PROJECT = 1,
    DIRECTORY = 2

class CodeConventionsFixer:
    def __init__(self):
        self.verify_log_file_name = "verification.log"
        self.fix_log_file_name = "fixing.log"
        self.file_walk_type = FileWalkType.FILE
        self.ccf_type = CCFType.VERIFY
        self.log_file = self.verify_log_file_name
        self.reformat_classes_names = {}
        self.reformat_classes_packages = {}

    def set_file_walk_type(self, file_walk_type):
        self.file_walk_type = file_walk_type

    def set_type(self, ccf_type):
        self.ccf_type = ccf_type
        if ccf_type == CCFType.FIX:
            self.log_file = self.fix_log_file_name

        logger = logging.getLogger()
        fhandler = logging.FileHandler(filename=self.log_file, mode='w')
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        logger.setLevel(logging.DEBUG)

    def to_string(self):
        return self.file_walk_type.name + " " + self.ccf_type.name

    def run(self, path):
        if self.ccf_type == CCFType.VERIFY:
            logging.basicConfig(filename=self.verify_log_file_name)
        else:
            logging.basicConfig(filename=self.fix_log_file_name)

        if self.file_walk_type == FileWalkType.FILE:
            self.format_file(path)
        elif self.file_walk_type == FileWalkType.PROJECT:
            self.format_project(path)
        else:
            self.format_dir(path)

    def format_tokens(self, path):
        output = ""
        lexer = Lexer()
        indent_level = 0
        line = 1
        last_bracket_index = 0
        package_name = ""
        refactor_names = {}
        refactor_indents = {}
        val_types = [TokenType.INT, TokenType.DOUBLE, TokenType.FLOAT, TokenType.LONG, TokenType.STRING, TokenType.CHAR]
        with open(path, 'r', encoding="utf-8") as file:
            orig_tokens = lexer.tokenize(file.read())
            self.refactor_docs(orig_tokens)
            tokens = list(filter(lambda x: x.token_type != TokenType.WHITESPACE, orig_tokens))
            for i in range(0, len(tokens)):
                token = tokens[i]
                if token.value == "{":
                    indent_level += 1
                    last_bracket_index = i
                elif token.value == "}":
                    indent_level -= 1
                    for name in refactor_indents.keys():
                        level = refactor_indents[name]
                        if level is not None and indent_level < level:
                            refactor_indents[name] = None
                            refactor_names[name] = None
                elif token.token_type == TokenType.HARD_KEYWORD and token.value == "package":
                    for j in range(i + 1, len(tokens)):
                        if tokens[j].token_type == TokenType.DOT or tokens[j].token_type == TokenType.IDENTIFIER or \
                                tokens[j].value == "*":
                            package_name += tokens[j].value
                        else:
                            break
                elif token.token_type == TokenType.HARD_KEYWORD:
                    if token.value == "val":
                        if tokens[i + 1].token_type == TokenType.IDENTIFIER and tokens[i + 2].value == "=" and \
                                tokens[i + 3].token_type in val_types:
                            if not self.is_upper_snake_case(tokens[i + 1].value):
                                refactor_names[tokens[i + 1].value] = self.to_upper_snake_case(tokens[i + 1].value)
                                refactor_indents[tokens[i + 1].value] = indent_level
                                self.refactor_prev(tokens[last_bracket_index + 1: i], tokens[i + 1].value,
                                                   self.to_upper_snake_case(tokens[i + 1].value))
                                self.write_log(path, line, "VAL_NAMING_ERROR", tokens[i + 1].value,
                                               self.to_upper_snake_case(tokens[i + 1].value))
                        else:
                            if not self.is_camel_case(tokens[i + 1].value):
                                refactor_names[tokens[i + 1].value] = self.to_camel_case(tokens[i + 1].value)
                                refactor_indents[tokens[i + 1].value] = indent_level
                                self.refactor_prev(tokens[last_bracket_index + 1: i], tokens[i + 1].value,
                                                   self.to_camel_case(tokens[i + 1].value))
                                self.write_log(path, line, "VAL_NAMING_ERROR", tokens[i + 1].value,
                                               self.to_camel_case(tokens[i + 1].value))
                    elif token.value == "var":
                        if tokens[i + 1].token_type == TokenType.IDENTIFIER and tokens[i + 2].value == "=":
                            if not self.is_camel_case(tokens[i + 1].value):
                                refactor_names[tokens[i + 1].value] = self.to_camel_case(tokens[i + 1].value)
                                refactor_indents[tokens[i + 1].value] = indent_level
                                self.refactor_prev(tokens[last_bracket_index + 1: i], tokens[i + 1].value,
                                                   self.to_camel_case(tokens[i + 1].value))
                                self.write_log(path, line, "VAR_NAMING_ERROR", tokens[i + 1].value,
                                               self.to_camel_case(tokens[i + 1].value))
                    elif token.value == "fun":
                        if tokens[i + 1].token_type == TokenType.IDENTIFIER and tokens[i + 2].value == "(" and \
                                tokens[i - 1].value != "Test":
                            if tokens[i + 3].value == ")" and tokens[i + 1].value == tokens[i + 5].value:
                                pass
                            elif not self.is_camel_case(tokens[i + 1].value):
                                refactor_names[tokens[i + 1].value] = self.to_camel_case(tokens[i + 1].value)
                                refactor_indents[tokens[i + 1].value] = indent_level
                                self.refactor_prev(tokens[last_bracket_index + 1: i], tokens[i + 1].value,
                                                   self.to_camel_case(tokens[i + 1].value))
                                self.write_log(path, line, "FUN_NAMING_ERROR", tokens[i + 1].value,
                                               self.to_camel_case(tokens[i + 1].value))
                    elif token.value == "object":
                        if tokens[i + 1].token_type == TokenType.IDENTIFIER:
                            if not self.is_pascal_case(tokens[i + 1].value):
                                refactor_names[tokens[i + 1].value] = self.to_pascal_case(tokens[i + 1].value)
                                refactor_indents[tokens[i + 1].value] = indent_level
                                self.refactor_prev(tokens[last_bracket_index + 1: i], tokens[i + 1].value,
                                                   self.to_pascal_case(tokens[i + 1].value))
                                self.write_log(path, line, "OBJECT_NAMING_ERROR", tokens[i + 1].value,
                                               self.to_camel_case(tokens[i + 1].value))
                    elif token.value == "class" or token.value == "interface":
                        if not self.is_pascal_case(tokens[i + 1].value):
                            refactor_names[tokens[i + 1].value] = self.to_pascal_case(tokens[i + 1].value)
                            refactor_indents[tokens[i + 1].value] = indent_level
                            self.refactor_prev(tokens[last_bracket_index + 1: i], tokens[i + 1].value,
                                               self.to_pascal_case(tokens[i + 1].value))
                            self.reformat_classes_names[tokens[i + 1].value] = self.to_pascal_case(tokens[i + 1].value)
                            self.reformat_classes_packages[tokens[i + 1].value] = package_name
                            self.write_log(path, line, token.value.upper() + "_NAMING_ERROR", tokens[i + 1].value,
                                           self.to_pascal_case(tokens[i + 1].value))

                elif token.token_type == TokenType.IDENTIFIER:
                    if token.value in refactor_names.keys() is not None:
                        token.value = refactor_names[token.value]
                elif token.token_type == TokenType.NEW_LINE:
                    line += 1
        k = 0
        for t in orig_tokens:
            if t.token_type == TokenType.WHITESPACE:
                output += t.value
            elif k < len(tokens):
                output += tokens[k].value
                k += 1
        return output

    def refactor_docs(self, orig_tokens):
        tokens = list(filter(lambda x: x.token_type == TokenType.DOC_COMMENT, orig_tokens))
        for token in tokens:
            i = orig_tokens.index(token)
            indent = orig_tokens[i - 1].value if i > 0 and orig_tokens[i - 1].token_type == TokenType.WHITESPACE else ""
            lines = token.value.split("\n")
            if len(lines) != 1:
                if lines[0] != "/**":
                    token.value = lines[0][0:3] + "\n" + indent + " * " + lines[0][3:len(lines[0])].lstrip() + "\n"
                else:
                    token.value = lines[0] + "\n"
                for line in lines[1:len(lines) - 1]:
                    token.value += indent + " * " + line.lstrip(" *") + "\n"
                if lines[len(lines) - 1].lstrip() != "*/":
                    # lines[len(lines) - 1]
                    token.value += indent + " * " + lines[len(lines) - 1].lstrip()[
                                                    0:len(lines) - 2] + "\n" + indent + " */"
                else:
                    token.value += indent + " */"

    def write_log(self, file_path, line_number, error_type, error_val, correct_val):
        # Id. File Path: Line Number - Error Code: Error Message
        if self.ccf_type == CCFType.FIX:
            logging.error(file_path + ": " + str(line_number) + "-" + error_type + ": "
                          + error_val + " renamed to " + correct_val)
        else:
            logging.warning(file_path + ": " + str(line_number) + "-" + error_type + ": "
                            + error_val + " should be " + correct_val)

    def refactor_prev(self, tokens, old, new):
        for token in tokens:
            if token.token_type == TokenType.IDENTIFIER:
                if token.value == old:
                    token.value = new

    def refactor_classes(self, files):
        lexer = Lexer()
        for f in files:
            output = ""
            reformat_classes = {}
            with open(f, 'r', encoding="utf-8") as file:
                orig_tokens = lexer.tokenize(file.read())
                tokens = list(
                    filter(lambda x: x.token_type != TokenType.WHITESPACE and x.token_type != TokenType.NEW_LINE,
                           orig_tokens))
                for i in range(0, len(tokens)):
                    token = tokens[i]
                    if token.token_type == TokenType.SOFT_KEYWORD and token.value == "import":
                        imp = ""
                        for j in range(i + 1, len(tokens)):
                            if tokens[j].token_type == TokenType.DOT or \
                                    tokens[j].token_type == TokenType.IDENTIFIER or tokens[j].value == "*":
                                imp += tokens[j].value
                            else:
                                break
                        for p in self.reformat_classes_packages.keys():
                            if self.is_imported(imp, self.reformat_classes_packages[p], p):
                                reformat_classes[p] = self.reformat_classes_names[p]
                                break
                    elif token.token_type == TokenType.IDENTIFIER:
                        if token.value in reformat_classes.keys() is not None:
                            token.value = reformat_classes[token.value]

            k = 0
            for t in orig_tokens:
                if t.token_type in (TokenType.NEW_LINE, TokenType.WHITESPACE):
                    output += t.value
                elif k < len(tokens):
                    output += tokens[k].value
                    k += 1
            if self.ccf_type == CCFType.FIX:
                self.save_formatted_file(output, f)

    def is_imported(self, imp, package, class_name):
        i = 0
        while True:
            if i == len(imp) or i == len(package) or package[i] != imp[i]:
                break
            else:
                i += 1
        if i == len(package) and i < len(imp) and imp[i: len(imp)] == "." + class_name:
            return True
        elif i < len(imp) and imp[i - 1] == "." and imp[i] == "*":
            return True
        return False

    def format_project(self, path):
        files = []
        tree = os.walk(path)
        for d in tree:
            cur_dir_name = d[0]
            cur_dir_files = d[2]
            for file in cur_dir_files:
                if file.endswith(".kt"):
                    files.append(cur_dir_name + '/' + file)
        for file in files:
            formatted_code = self.format_tokens(file)
            if self.ccf_type == CCFType.FIX:
                self.save_formatted_file(formatted_code, file)
        self.refactor_classes(files)

    def format_dir(self, path):
        files = []
        tree = os.walk(path)
        for d in tree:
            cur_dir_name = d[0]
            cur_dir_files = d[2]
            for file in cur_dir_files:
                if file.endswith(".kt"):
                    files.append(cur_dir_name + '/' + file)
            break
        for file in files:
            formatted_code = self.format_tokens(file)
            if self.ccf_type == CCFType.FIX:
                self.save_formatted_file(formatted_code, file)
        self.refactor_classes(files)

    def format_file(self, path):
        formatted_code = self.format_tokens(path)
        if self.ccf_type == CCFType.FIX:
            self.save_formatted_file(formatted_code, path)

    def save_formatted_file(self, formatted_code, path):
        with open(path, 'w') as file:
            file.write(formatted_code)

    def is_upper_snake_case(self, value: str):
        result = re.match(r'[A-Z]+(_(([A-Z]+)|([0-9]+)))*', value)
        return True if result is not None and result.start() == 0 and result.end() == len(value) else False

    def is_camel_case(self, value: str):
        result = re.match(r'[a-z]+((\d)|([A-Z0-9][a-z0-9]+))*([A-Z])?', value)
        return True if result is not None and result.start() == 0 and result.end() == len(value) else False

    def is_pascal_case(self, value: str):
        result = re.match(r'([A-Z][a-z0-9]+)((\d)|([A-Z0-9][a-z0-9]+))*([A-Z])?', value)
        return True if result is not None and result.start() == 0 and result.end() == len(value) else False

    def to_upper_snake_case(self, value: str):
        new_name = ""
        last_case = -1  # symb = 0, digit = 1, lower = 2, upper = 3
        for letter in value:
            if letter.isalpha():
                if letter.isupper():
                    if last_case == -1 or last_case == 3 or last_case == 0:
                        new_name += letter
                    else:
                        new_name += "_" + letter
                    last_case = 3
                elif letter.islower():
                    if last_case == 1:
                        new_name += "_" + letter.upper()
                    else:
                        new_name += letter.upper()
                    last_case = 2
            elif letter.isnumeric():
                if last_case == -1 or last_case == 1 or last_case == 0:
                    new_name += letter
                else:
                    new_name += "_" + letter
                last_case = 1
            else:
                if last_case != -1 and last_case != 0:
                    new_name += "_"
                last_case = 0
        if last_case == 0:
            new_name = new_name[0:len(new_name) - 1]
        return new_name

    def to_camel_case(self, value: str):
        new_name = ""
        last_case = -1  # symb = 0, digit = 1, lower = 2, upper = 3
        for letter in value:
            if letter.isalpha():
                if letter.isupper():
                    if last_case == 3 or last_case == -1:
                        new_name += letter.lower()
                    else:
                        new_name += letter
                    last_case = 3
                elif letter.lower():
                    if last_case == 0 or last_case == 1:
                        new_name += letter.upper()
                    else:
                        new_name += letter
                    last_case = 2
            elif letter.isnumeric():
                new_name += letter
                last_case = 1
            else:
                last_case = 0
        return new_name

    def to_pascal_case(self, value: str):
        new_name = ""
        last_case = -1  # symb = 0, digit = 1, lower = 2, upper = 3
        for letter in value:
            if letter.isalpha():
                if letter.isupper():
                    if last_case == 3:
                        new_name += letter.lower()
                    else:
                        new_name += letter
                    last_case = 3
                elif letter.lower():
                    if last_case == 0 or last_case == 1:
                        new_name += letter.upper()
                        last_case = 2
                    elif last_case == -1:
                        new_name += letter.upper()
                        last_case = 3
                    else:
                        new_name += letter
                        last_case = 2

            elif letter.isnumeric():
                new_name += letter
                last_case = 1
            else:
                last_case = 0
        return new_name
