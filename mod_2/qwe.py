import os

class CreationLogger(type):

    def __call__(self, *args):
        print(args)
        filename = '\' + str(hash(args)) + '.html'
        file = open(filename, 'w')
        file.write('<html><head>\n')
        file.write('<style>\ntable, th, td {\n  border: 1px solid black;\n}\n</style>\n')
        file.write('</head><body>\n')
        file.write('<table><tbody>\n')
        file.write('<tr><td>name</td><td>' + args[0] +
                   '</td></tr>\n')
        file.write('<tr><td>country</td><td>' + args[1] + '</td></tr>\n')
        file.write('<tr><td>days</td><td>' + str(args[2]) + '</td></tr>\n')
        file.write('<tr><td>people</td><td>' + str(args[3]) + '</td></tr>\n')
        file.write('<tr><td>price</td><td>' + str(args[4]) + '</td></tr>\n')
        file.write('</tbody></table>\n')
        file.write('</body></html>')
        file.close()
        return super().__call__(*args)



def country_tours_logger(func):
    def _decorator(self, *args, **kwargs):
        func(self, *args, **kwargs)
        filename = 'C:/Users\\Alina\\Desktop\\exam_preparation\\' + self.country + '.txt'
        append_write = 'a' if os.path.exists(filename) else 'w'
        file = open(filename, append_write)
        file.write(str(self) + '\n')
        file.close()
    return _decorator


class TouristTour(metaclass=CreationLogger):
    __attributes = {'name': lambda x: type(x) == str,
                    'country': lambda x: type(x) == str,
                    'days': lambda x: type(x) == int and x > 0,
                    'people': lambda x: type(x) == int and x > 0,
                    'price': lambda x: type(x) == float and x > 0}

    @country_tours_logger
    def __init__(self, name=str(), country=str(), days=int(),
                 people=int(), price=float()):
        self.name = name
        self.country = country
        self.days = days
        self.people = people
        self.price = price

    def __getattr__(self, item):
        """Attribute error get action."""

        if item not in self.__dict__:
            return str(self.__class__.__name__) + \
                   ' object  "' \
                   + str(item) + '"!'

    def __getattribute__(self, item):

        """Get action."""

        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        """Set action."""
        if key not in self.__dict__:
            if key in TouristTour.__attributes:
                if TouristTour.__attributes[key](value):
                    self.__dict__[str(key)] = value
                    print('Update ' + key)
                else:
                    raise TypeError("Wrong value for attribute " + key)

            else:
                self.__dict__[key] = value
                print('Update ' + key)

        else:
            self.__dict__[key] = value
            print('Створено ' + key)

    def __delattr__(self, item):
        """Delete action."""

        del self.__dict__[item]
        print('Del attr' + item)

    def __str__(self):
        return "Країна: " + self.country + " Назва: " + self.name + " Кількість людей: " + str(self.people) + " Кількість днів: " + str(self.days) + " Ціна: " + str(self.price)


a = TouristTour("An", "qw", 4, 5, 56.0)
del a.name
a.name = 'Ukraine'
print(a.name)

# a = TouristTour("An", 3, 4, 5, 56)
