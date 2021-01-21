from quadrangles.quadrangle import Quadrangle
from quadrangles.quadrangle_type import QuadrangleType
import hashlib

i = [0]

class Parallelogram(Quadrangle):
    def __init__(self, vert1, vert2,
                 vert3, vert4):
        super().__init__(vert1, vert2, vert3, vert4)
        self.figure_type = QuadrangleType.PARALLELOGRAM.name
        # ?
        self.__figure_id = self.__set_figure_id()

    def __set_figure_id(self):
        i[0] += 1
        return hashlib.md5(self.figure_type.encode('utf-8')).hexdigest() + \
                           hashlib.md5(str(i[0] - 1).encode('utf-8')).hexdigest()
    #id(self)
    def get_figure_id(self):
        return self.__figure_id

    @staticmethod
    def get_subclasses():
        return list(Parallelogram.__subclasses__())

    @staticmethod
    def get_superclasses():
        return list(Parallelogram.mro())

    # Методи генерацiї колекцiй чотирикутникiв за заданою площею та периметром.
    def generate_collection(self):
        return [Parallelogram([i, i], [i, i], [i, i], [i, i]) for i in range(10)]

    def is_type(self, type_):
        if self.figure_type == type_:
            return True
        else:
            return False

    def is_area_eq(self, Object_):
        if Object_.figure_type == self.figure_type:
            return True
        else:
            return False
''''
print(Parallelogram([1,2],[1,2],[1,2],[1,2]).is_equal_sides())
print(Parallelogram([1,2],[1,2],[1,2],[1,2]).get_subclasses())
print(Parallelogram([1,2],[1,2],[1,2],[1,2]).get_superclasses())
print(Parallelogram([1,2],[1,2],[1,2],[1,2]).generate_collection())
print(Parallelogram([1,2],[1,2],[1,2],[1,2]).is_type(QuadrangleType.SQUARE.name))'''
print(Parallelogram([1,2],[1,2],[1,2],[1,2]))
print(Parallelogram([1,2],[1,2],[1,2],[3,2]).is_area_eq(Parallelogram([1,2],[1,5],[1,2],[3,2])))