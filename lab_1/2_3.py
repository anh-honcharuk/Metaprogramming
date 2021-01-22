# 3.Метаклас CreationLogger, який керує створенням об’єктiв
# екземплярiв класу PlaneRoute та здiйснює динамiчну фiксацiю
# створення авiарейсiв що виконуються з використанням певної
# моделi лiтака з певного початкового пункту записуючи iнформацiю
# про новостворенi авiарейси у журнальний текстовий файл.
from datetime import datetime


class CreationLogger(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.__model_name = '2'
        cls.__start_point = 'Ukraine'

    def __call__(cls, *args):
        new_obj = super().__call__(*args)
        if 'model' in new_obj.__dict__ and cls.__model_name == new_obj.model and cls.__start_point == new_obj.start_point:
            with open('log_creation.txt', 'a+') as f:
                f.write(str(datetime.now()) + str(new_obj))
        return new_obj


# 2.Клас PlaneRoute, який наступнi атрибути:
# назва, початковий та кінцевий пункти, модель лiтака,
# пілоти, кiлькiсть пасажирських мiсць, тривалiсть польоту,
# класи пасажирських мiсць. Реалiзувати управлiння атрибутами
# об’єктiв екземплярiв класу PlaneRoute за допомогою спецiальних методiв,
# якi реалiзують функцiональнiсть get, set та delete.
class PlaneRoute(metaclass=CreationLogger):
    __attributes = {'name', 'start_point', 'end_point', 'model', 'pilots', 'passenger_count', 'flight_duration',
                    'classes'}

    __attributes = {'name': lambda x: type(x) == str,
                    'start_point': lambda x: type(x) == str,
                    'end_point': lambda x: type(x) == str,
                    'model': lambda x: type(x) == str,
                    'pilots': lambda x: type(x) == int and x > 0,
                    'passenger_count': lambda x: type(x) == int and x > 0,
                    'flight_duration': lambda x: type(x) == float and x > 0,
                    'classes': lambda x: type(x) == int and x > 0}

    def __init__(self, name, start_point, end_point, model, pilots, passenger_count, flight_duration, classes):
        self.name = name
        self.start_point = start_point
        self.end_point = end_point
        self.model = model
        self.pilots = pilots
        self.passenger_count = passenger_count
        self.flight_duration = flight_duration
        self.classes = classes

    def __getattr__(self, item):
        if item not in self.__dict__:
            raise ValueError(str(self.__class__.__name__) + ' has no attribute "' + str(item) + '"')

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        if key not in self.__dict__:
            if key not in PlaneRoute.__attributes:
                raise ValueError(str(self.__class__.__name__) + ' not allowed to have attribute "' + str(key) + '"')

        if key in PlaneRoute.__attributes:
            if PlaneRoute.__attributes[key](value):
                self.__dict__[str(key)] = value
            else:
                raise ValueError(
                    str(self.__class__.__name__) + ' in attribute "' + str(key) + '" not allowed to have type '
                    + str(type(value)))

    def __delattr__(self, item):
        del self.__dict__[item]

    def __str__(self):
        return " name: ".upper() + self.name + \
               " start_point: ".upper() + self.start_point + \
               " end_point: ".upper() + self.end_point + \
               " model: ".upper() + self.model + \
               " pilots:".upper() + str(self.pilots) + \
               " passenger_count: ".upper() + str(self.passenger_count) + \
               " flight_duration: ".upper() + str(self.flight_duration) + \
               " classes: ".upper() + str(self.classes) + '\n'



a = PlaneRoute("An", "ert", "An", "2", 4, 5, 56.0, 5)
b = PlaneRoute("An", "Ukraine", "An", "2", 4, 5, 56.0, 5)
c = PlaneRoute("An", "Ukraine", "An", "34", 4, 5, 56.0, 5)
d = PlaneRoute("An", "qw", "An", "3", 4, 5, 56.0, 5)
del a.name
a.name = 'Ukraine'
a.model = 'dxcfgbhjn'
print(a.name)
