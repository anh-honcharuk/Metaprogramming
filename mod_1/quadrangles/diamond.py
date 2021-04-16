from quadrangles.parallelogram import Parallelogram
from quadrangles.quadrangle_type import QuadrangleType


class Diamond(Parallelogram):
    def __init__(self, vert1, vert2,
                 vert3, vert4):
        super().__init__( vert1, vert2, vert3, vert4 )
        self.figure_type = QuadrangleType.PARALLELOGRAM.name
        self.__figure_id = self.__set_figure_id()

