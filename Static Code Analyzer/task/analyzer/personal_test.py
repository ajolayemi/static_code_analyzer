print('What\'s your name?')  # reading an input
name = input()
print(f'Hello, {name}')  # here is an obvious comment: this prints greeting with a name

very_big_number = 11_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000
print(very_big_number)


def some_fun():
    print('NO TODO HERE;;')
    pass  # Todo something


class InvalidClass:
    @staticmethod
    def __init__(self):
        pass


class ValidClass:
    pass


class  wrongname:
    pass


def WrongFunctionName():
    pass


class InheritingClass(FatherParent):
    pass

class CorrectOne:
    pass


class spaces:
    pass


class snake_case:
    pass


class Inheritance(CorrectOne):
    pass

