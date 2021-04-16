from args_ import ArgsParser


if __name__ == '__main__':
    a = ArgsParser()
    k = a.parse_args()
    ArgsParser.define_item(k)