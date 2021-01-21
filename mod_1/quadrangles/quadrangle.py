from abc import ABC, abstractmethod


class Quadrangle(ABC):
    def __init__(self, vert1, vert2,
                 vert3, vert4):

        self.__vert1 = self.error_catcher_vert(vert1)
        self.__vert2 = self.error_catcher_vert(vert2)
        self.__vert3 = self.error_catcher_vert(vert3)
        self.__vert4 = self.error_catcher_vert(vert4)
        # порахувати, додати ф-ї
        self.__len12 = None
        self.__len23 = None
        self.__len34 = None
        self.__len41 = None
        self.__perimeter = None
        self.__area = None
        self.__len_diagonal1 = None
        self.__len_diagonal2 = None
        self.__angle412 = None
        self.__angle123 = None
        self.__angle234 = None
        self.__angle341 = None

    def get_figure_type(self):
        return self.figure_type
    """
    ---------------
    """

    @staticmethod
    def error_catcher_vert(atr):
        if type(atr) == list:
            if len(atr) == 2:
                return atr
            else:
                raise ValueError( 'Incorect type(2)' )
        else:
            raise ValueError( 'Incorect type(1)' )

    @staticmethod
    def get_subclasses():
        return list(Quadrangle.__subclasses__())

    @staticmethod
    def get_superclasses():
        return list(Quadrangle.mro())

    @abstractmethod
    def generate_collection(self):
        pass

    def is_equal_sides(self):
        self.is_equal_sides = None
        if self.__len12 == self.__len23 == self.__len34 == self.__len41:
            self.is_equal_sides = True
            return True
        else:
            self.is_equal_sides = False
            return False
    @abstractmethod
    def is_type(self, type_):
        pass
''' self.i
— Динамiчнi атрибути якi перевiряють виконання основних якiсних властивостей фiгури (наприклад рiвнiсть сторiн, паралельнiсть сторiн, рiвнiсть кутiв, тощо).
— Метод iнiцiалiзацiї об’єктiв екземплярiв.
— Метод отримання типу фiгури.
— Методи отримання унiкального незмiнного iдентифiкатора фiгури.
— Методи отримання координат вершин фiгури.
— Методи отримання довжини сторiн фiгури.
— Методи отримання периметру та площi фiгури.
— Методи отримання довжини дiагоналей фiгури.
— Методи отримання градусних мiр кутiв фiгури.
— Метод отримання перелiку пiдтипiв фiгури.
— Метод отримання перелiку супертипiв фiгури.
— Метод перевiрки належностi фiгури до певного типу фiгур в рамках iєрархiї.
— Усi можливi методи порiвняння за площею та периметром фiгури iз будь-якої iншою фiгурою
iєрархiї. Реалiзацiя має враховувати усi можливi варiанти порiвняння.
— Метод перевiрки перетину фiгури iз будь-якою iншою фiгурою iєрархiї.
— Методи генерацiї колекцiй чотирикутникiв за заданою площею та периметром.
Реалiзувати окремий модуль demo в рамках якого повинна вiдбуватися демонстрацiя створення
об’єктiв усiх класiв чотирикутникiв реалiзованих в рамках пакету qsuadrangles та виклики усiх
“публiчних” методiв реалiзованих в рамках кожного з класiв пакету. (10 балiв)
    '''