def sum_dec(func):
    def wrapper(*args):
        wrapper.money += args[1]

        return func(*args)

    wrapper.money = 0
    return wrapper

class Wallet:

    def __init__(self, money=float()):
        self._money = money
    @property
    def money(self):
        return self._money

    @money.setter
    @sum_dec
    def money(self, money=float()):
        if type(money) == float:
            self._money += money
