import os.path
def _convert_to_html(cls, ins):
    if not os.path.exists('target_object_html_view'):
        os.makedirs('target_object_html_view')
    try:
        file_path = os.path.join('target_object_html_view',
                                 '{}_ins_{}.html'.format(
                                     cls.__name__,
                                     hash(ins)))
        file = open(file_path, 'x')
        file.write('<style>\n.my_table{\n')
        file.write(' border-collapse: collapse;\n}\n\n')

        file.write('.my_table_cell, .my_table_cell_centered {\n')
        file.write(' border: 1px solid black;\n')
        file.write(' border-collapse: collapse;\n')
        file.write(' padding: 5px 5px 5px 5px;\n')
        file.write('}\n')
        file.write('.my_table_cell_centered{\n')
        file.write(' text-align: center;\n')
        file.write('}\n')
        file.write('</style>\n')
        file.write('<h1>' + cls.__name__ + '_ins_' +
            str(hash(ins)) + '</h1>\n')
        file.write('<table border="1" class="my_table">\n')

        file.write(' <tr>\n')
        file.write(' <td class="my_table_cell"> <strong>Attribute name</strong></td>\n')
        file.write(' <td class="my_table_cell"> <strong>Attribute value</strong></td>\n')
        file.write(' <td class="my_table_cell"> <strong>Attribute type</strong></td>\n')
        file.write(' </tr>\n')

        for attribute in ins.__dict__:
            file.write(' <tr>\n')
            file.write(' <td class="my_table_cell">' + attribute + '</td>\n')
            file.write(' <td class="my_table_cell_centered">' +
                       str(ins.__dict__[attribute]) +
                       '</td>\n')
            file.write(' <td class="my_table_cell_centered">' +
                       str(ins.__dict__[attribute].__class__.__name__) +
                       '</td>\n')

            file.write(' </tr>\n')
        for i in cls.__dict__:
            if not i.startswith('__'):
                file.write(' <tr>\n')
                file.write(' <td class="my_table_cell">' +
                           str(cls.__name__ + '_' + i) +
                           '</td>\n')
                file.write(' <td class="my_table_cell_centered">' +
                       str(cls.__dict__[i]) +
                       '</td>\n')
                file.write(' <td class="my_table_cell_centered">'
                           + str(eval(cls.__name__ + '.' +
                                      i + '.__class__.__name__')) +
                           '</td>\n')
                file.write(' </tr>\n')
        file.write('</table>\n')
        file.close()
    except FileExistsError:
        print('HTML view for this ins has already been created.')



class FixNumCreator(type):
    def __init__(cls, name, bases, attrs, ins_num):
        type.__init__(cls, name, bases, attrs)

    def __new__(metacls, name, bases, attrs, ins_num):
        cls = type.__new__(metacls, name, bases, attrs)

        cls.N = ins_num
        #cls.log_file = f'FixNumCreator_{name}.log'
        return cls

    def __call__(cls, *args, **kwargs):
        if cls.N:
            ins = super().__call__(*args, **kwargs)
            _convert_to_html(cls, ins)
            cls.N -= 1
            return ins
        else:
            raise AttributeError(f'Max limit of items for {cls.__name__} excedeed')

def attr_change_logger(key_set):
    def wrapper(cls):
        def _setattr(self, name, value):
            pre_val = getattr(self, name, None)
            result = super(cls, self).__setattr__(name, value)
            if name in key_set and getattr(self, name, None) != pre_val:
                with open(f'{cls.__name__}.{name}_attr.log', 'a') as f:
                    f.write('Set value({}) on .{} for {}\n'.format(value, name, self))
            return result
        cls.__setattr__ = _setattr
        return cls
    return wrapper

class A(metaclass=FixNumCreator, ins_num = 5):
    def __init__(self, a, b):
        self.a = a
        self.b = b

print(A.__name__)
a = A(1, 2)
b = A(2, 3)
c = A(3, 4)
#d = A(4, 5)

class TypeDescriptor:
    pass
class City:
    def __init__(self, name, region, population, parts):
        pass

