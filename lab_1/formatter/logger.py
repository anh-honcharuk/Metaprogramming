class Logger:
    def __init__(self, name):
        self.logger = list()
        self.file_name = name

    def write_error(self, line, message):
        self.logger.append( '[' + self.file_name + "] ERROR: " + message + ", line: " + str(line) + '\n' )
        # print( '[' + self.file_name + "] ERROR: " + message + ", line: " + str(line))
