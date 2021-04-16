class Number:
    def draw(self):
        print('Number')

class One(Number):
    pass


class Two(Number):
    def draw(self):
        print('Two')


One().draw()
Two().draw()