import type_token


class MyToken:

    def __init__(self, type, value, begin, end):
        self.type = type
        self.value = value
        self.begin = begin
        self.end = end

    #
    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_begin(self):
        return self.begin

    def set_start(self, begin):
        self.begin = begin

    def get_end(self):
        return self.end

    def set_end(self, end):
        self.end = end

    def return_token(self):
        return "MyToken: " + "type=" + str(self.type) + ", value='" + str(self.value) + '\'' + ", begin=" + str(
            self.begin) + ", end=" + str( self.end)
