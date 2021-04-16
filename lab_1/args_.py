import argparse
import os
from analizer import Analizer

class ArgsParser:

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description='kotlin code analyzer', add_help=True)
        # parser.add_argument('-v', '--verify', help='')
        parser.add_argument('-ft', '--format', help='format files')
        parser.add_argument('--file', help='format file')
        parser.add_argument('-l', '--log', help='logs')

        args = parser.parse_args()
        args_dictionary = vars(args)
        return args_dictionary

    @staticmethod
    def define_item(my_dict):

        if my_dict['format'] is not None:
            Analizer(my_dict['format']).analize_all()

        if my_dict['log'] is not None:
            print(my_dict['log'])
            cl = Analizer(my_dict['log'])
            cl.logging_()
            log_ = cl.logs
            for l in log_:
                ls = l.logger
                for i in ls:
                    print(i, end="")

        if my_dict['file'] is not None:

            cl = Analizer(my_dict['file'])
            cl.analize_file(my_dict['file'])
            cl.logging_()
            log_ = cl.logs
            for l in log_:
                ls = l.logger
                for i in ls:
                    print( i, end="" )