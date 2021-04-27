import ast
import re

class_name_ptn = re.compile(r'^[A-Z][a-z]+[A-Z]?[a-z]+?$')
func_var_arg_ptn = re.compile(r'^[a-z_]+_?[a-z_]+$|^[a-z_]')


ERRORS_DICT = {'Class name': 'S008',
               'Function name': 'S009',
               'Argument name': 'S010',
               'Variable name': 'S011',
               'Default Arg': 'S012'
               }


def file_parser(file_to_parse):
    with open(file_to_parse) as file:
        return ast.parse(file.read())


class ClassAnalyzer(ast.NodeVisitor):
    """ Walks through python file and analyzes functions defined therein. """

    def __init__(self, file_path):
        self.file = file_path


class FuncAnalyzer(ast.NodeVisitor):
    """ Walks through python file and analyzes functions defined therein """

    def __init__(self, file_path):
        self.file_path = file_path

    def visit_FunctionDef(self, node):
        """ This checks to see that function names are written currently.
        Checks to see also that default arguments value aren't mutable ones.
        Checks to see that variables defined in function bodies follow snake_case naming convention. """
        mutable_default_args = [ast.List, ast.Set, ast.Dict]
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            current_line = node.lineno

            # Check that function name is correct
            if not re.search(func_var_arg_ptn, func_name):
                print(f'{self.file_path}: Line {current_line}: {ERRORS_DICT.get("Function name")} '
                      f'Function - {func_name} - name does not follow snake_case convention.')

            # Check that args names are correct
            for arg in node.args.args:
                if not re.search(func_var_arg_ptn, arg.arg):
                    print(f'{self.file_path}: Line {current_line}: {ERRORS_DICT.get("Argument name")} '
                          f'Argument name \'{arg.arg}\' should be snake case. ')

            # Check that variables name defined in function body are correct
            for var in node.body:
                if isinstance(var, ast.Assign):
                    for name in var.targets:
                        if isinstance(name, ast.Attribute):
                            variable_name = name.attr
                        else:
                            variable_name = name.id
                        line_num = var.lineno
                        if not re.search(func_var_arg_ptn, variable_name):
                            print(f'{self.file_path}: Line {line_num}: {ERRORS_DICT.get("Variable name")}'
                                  f' Variable - {variable_name} - name does not follow snake_case convention.')

            # Check to see that default arguments are defined correctly
            if any([isinstance(def_arg, arg) for def_arg in node.args.defaults
                    for arg in mutable_default_args]):
                print(f'{self.file_path}: Line {current_line}: {ERRORS_DICT.get("Default Arg")} '
                      f'Default argument value is mutable.')

        self.generic_visit(node)


if __name__ == '__main__':
    parsed_file = file_parser(r'..\test\this_stage\test_3.py')
    FuncAnalyzer(r'..\test\this_stage\test_3.py').visit_FunctionDef(parsed_file)
