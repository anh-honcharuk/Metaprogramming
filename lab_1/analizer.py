import os

from formatter.formatter import Formatter
from lexer_ import Lexer

class Analizer:
    saved = list()
    def __init__(self, path):
        self.way_list = list()
        self.res_list = list()
        self.file_list = list()
        self.path = path
        self.find_path(path)
        self.logs = list()


    def open_(self, file_path):
        f = open(file_path, "r")
        lines = f.readlines()
        return ''.join(lines)

    def find_path(self, dir_way):
        for root, dirs, files in os.walk(dir_way, topdown=False):

            for file in files:

                if file.endswith(".kt") and 'FORMATTED' not in os.path.join(root, file):

                    self.way_list.append(os.path.join(root, file))

                    self.res_list.append(self.new_file(os.path.join(root, file)))
                    self.file_list.append(file)

    def new_file(self, path):

        path = path[0:-3] + 'FORMATTED.kt'
        f = open(path, 'w+')
        return path

    def analize_all(self):
        analized = Analizer(self.path)

        for i in range(len(analized.way_list)):
            # print(analized.way_list[i])
            str_ = analized.open_(analized.way_list[i])
            cl = Formatter()
            formatted = cl.format_tokens(Lexer().tokenize(str_), str(self.res_list[i]) )#file_list
            self.saved.append([analized.way_list[i], formatted])
            self.logs.append(cl.logger)
            f = open(analized.res_list[i], 'w+')
            f.write(formatted)
            f.close()

    # @staticmethod
    # def analize_one(self, way):
    #     analized = Analizer(way)
    #     str_ = analized.open_(way)
    #     cl = Formatter()
    #     formatted = cl.format_tokens(Lexer().tokenize(str_), str(way))
    #
    #     f = open(way[0:-3] + 'FORMATTED.kt', 'w+')
    #     f.write(formatted)
    #     f.close()

    def logging_(self):
        analized = Analizer(self.path)

        for i in range(len(analized.way_list)):
            # print(analized.way_list[i])
            str_ = analized.open_(analized.way_list[i])
            cl = Formatter()
            formatted = cl.format_tokens(Lexer().tokenize(str_), str(self.res_list[i]) )
            self.saved.append([analized.way_list[i], formatted])
            self.logs.append(cl.logger)

    def analize_file(self, path):
        analized = Analizer(path)
        str_ = analized.open_(path)
        cl = Formatter()
        formatted = cl.format_tokens(Lexer().tokenize(str_), str(path[0:-3] + 'FORMATTED.kt'))

        self.logs.append(cl.logger)
        f = open(path[0:-3] + 'FORMATTED.kt', 'w+')
        f.write(formatted)
        f.close()


