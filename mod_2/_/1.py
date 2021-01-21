class Money:

    def __init__(self, money):

        self.money = money

    def __get__(self, instance, owner):

        if self.money in instance.__dict__.keys():
            return str(instance.__dict__[self.money]) + \
                " " + str(self.money).upper()
        else:
            return str(instance.__class__.__name__) + \
            ' object currently has no attribute ' \
            + str(self.money) + '.'

    def __set__(self, instance, value):

        if self.money not in instance.__dict__.keys():
            instance.__dict__[self.money] = value
        else:
            if value > 0:
                instance.__dict__[self.money] += value
                print(str(value) + ' ' + str(self.money).upper() + \
                ' was putted into your wallet.')

        def __delete__(self, instance):
            del instance.__dict__[self.money]
            print('Your ' + str(self.money).upper() + ' money account was closed.')


class PlaneRoute:

    __attributes = {'usd', 'eur', 'uah', 'gbp', 'chf', 'ownerName', 'ownerSurname'}

    def __init__(self, usd=float(), eur=float(), uah=float(), name=str(), surname=str()):
        self.ownerName = name
        self.ownerSurname = surname
        self.usd = usd
        self.eur = eur
        self.uah = uah

    usd = Money('usd')
    eur = Money('eur')
    uah = Money('uah')

    def __getattr__(self, item):


        if item not in self.__dict__:
            return str(self.__class__.__name__) + \
            ' object currently has no attribute "' \
            + str(item) + '"!'

    def __getattribute__(self, item):

        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):

        if key not in self.__dict__:
            if key in Wallet.__attributes:
                self.__dict__[str(key)] = value

                print('Attribute "' + str(key) + \
                '" was added to the object structure.')
                print('Attribute "' + str(key) + \
                '" was assigned with value ' + \
                str(value) + '!')
            else:
                print('Attribute "' + str(key) + \
                        '" cannot be added to the object structure.')
        else:
            if value > 0:
                self.__dict__[key] += value
                print('Attribute "' + str(key) + \
                '" was assigned with value ' \
                    + str(value) + '!')

            def __delattr__(self, item):

                del self.__dict__[item]
                print('Attribute "' + str(item) + \
                      '" was removed form object structure.')

class CreationLogger(type):
    def __new__(mcs, *args, **kwargs):
        return type.__new__(mcs, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        obj = super.__call__(*args, **kwargs)
        cls.__