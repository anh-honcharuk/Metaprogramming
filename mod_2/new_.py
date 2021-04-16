class Meta(type):
    def __new__(cls, *args, **kwargs):
        class_ = type.__new__(cls, *args, **kwargs)
        setattr(class_, 'q2', 0)
        return class_

    def __call__(self, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        setattr( obj, 'q3', 1)
        return obj


class Q(metaclass=Meta):

    def __init__(self, q):
        self.q = q

q = Q(1)
q2 = Q(10)
print(q2.__dict__)
print(q.__dict__)
print(q.q2)
print(Q.__dict__)