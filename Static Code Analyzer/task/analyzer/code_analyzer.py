#!/usr/bin/env python

import os
import sys
import re

MAX_LINE_LEN = 79

ERRORS_DICT = {'Long Line': 'S001',
               'Indentation': 'S002',
               'Semicolon': 'S003',
               'Inline Comments': 'S004',
               'TODO': 'S005',
               'Blank lines': 'S006',
               'Construction space': 'S007',
               'Class name': 'S008',
               'Function name': 'S009'
               }

class_name_ptn = re.compile(r'^class[\s]+[A-Z][a-z]+[A-Z]?[a-z]+?$')
function_name_ptn = re.compile(r'^def[\s]+[a-z_]+_?[a-z_]+$')
def_constructor_ptn = re.compile(r'^\s?def\s\w+')
class_constructor_ptn = re.compile(r'^\s?class\s\w+')

sys.argv.append(r'..\test')
if len(sys.argv) > 2:
    file_or_dir = sys.argv[1]

else:
    file_or_dir = ''

is_dir = os.path.isdir(file_or_dir)
is_file = os.path.isfile(file_or_dir)


class Analyser:
    """ A simple static code analyser. """
    previous_blanks = 0

    def __init__(self, file_to_analyse: str = file_or_dir):
        self.file = file_to_analyse
        self.check_all()

    def check_all(self):
        current_line = self.file_reader()
        while True:
            try:
                c_line = next(current_line)
                self.check_long_line(c_line)
                self.check_indent_error(c_line)
                self.check_for_semicolon(c_line)
                self.check_inline_comment(c_line)
                self.check_to_do(c_line)
                self.check_blank_lines(c_line)
                self.check_constructor_space(c_line)
                self.check_naming_convention(c_line)
            except StopIteration:
                break

    @staticmethod
    def check_naming_convention(current_line):
        if current_line:
            c_line, c_line_num, file_path = current_line
            if c_line.lstrip().startswith('class'):
                if c_line.strip().find('(') > 0:
                    class_name = c_line[:c_line.strip().find('(')]
                else:
                    class_name = c_line[:c_line.strip().find(':')]

                if not re.search(class_name_ptn, class_name):
                    print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("Class name")} '
                          f'ClassName follows the CamelCase convention.')

            elif c_line.lstrip().startswith('def') and \
                    not re.search(function_name_ptn, c_line.strip()[:c_line.strip().index('(')]):
                print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("Function name")} '
                      f'function_name follows the snake_case convention.')

    @staticmethod
    def check_constructor_space(current_line):
        if current_line:
            c_line, c_line_num, file_path = current_line
            if c_line.lstrip().startswith('class') and not re.search(class_constructor_ptn,
                                                                     c_line.lstrip()):
                print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("Construction space")} '
                      f'Too many spaces after class constructor ')
            elif c_line.lstrip().startswith('def') and not re.search(def_constructor_ptn,
                                                                     c_line.lstrip()):
                print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("Construction space")} '
                      f'Too many spaces after def constructor ')

    @staticmethod
    def check_long_line(current_line):
        if current_line:
            c_line, c_line_num, file_path = current_line
            if len(c_line) > MAX_LINE_LEN:
                print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("Long Line")} '
                      f'The line is {len(c_line) - MAX_LINE_LEN} chars too long')

    @staticmethod
    def check_blank_lines(current_line):
        if current_line:
            c_line, c_line_num, file_path = current_line
            if len(c_line) == 1:
                Analyser.previous_blanks += 1
            else:
                if Analyser.previous_blanks > 2:
                    print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("Blank lines")} More than two blank'
                          f' lines preceding a code line')
                    Analyser.previous_blanks = 0
                else:
                    Analyser.previous_blanks = 0

    @staticmethod
    def check_to_do(current_line):
        if current_line:
            c_line, c_line_num, file_path = current_line
            comment = c_line[c_line.find('#'):].lower()
            if 'todo' in comment:
                print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("TODO")} TODO found')

    @staticmethod
    def check_inline_comment(current_line):
        if current_line:
            c_line, c_line_num, file_path = current_line
            line_str = f'Line {c_line_num}'
            if '#' in c_line and not c_line.startswith('#'):
                if not c_line.split('#')[0].endswith('  '):
                    print(f'{file_path}: {line_str}: {ERRORS_DICT.get("Inline Comments")} At least two spaces required'
                          f' before inline comments')

    def check_for_semicolon(self, current_line):
        """ Checks for the presence of unnecessary
        semicolons in statements """
        if current_line:
            c_line, c_line_num, file_path = current_line
            line_without_comment = self.remove_comment_in_a_string(c_line)
            if line_without_comment.strip().endswith(';'):
                print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("Semicolon")} Unnecessary semicolon')

    @staticmethod
    def remove_comment_in_a_string(string):
        if '#' in string:
            return string[:string.index('#')].strip()
        else:
            return string

    @staticmethod
    def check_indent_error(current_line):
        if current_line:
            c_line, c_line_num, file_path = current_line
            indent_num = len(c_line) - len(c_line.lstrip())
            if indent_num % 4 > 0 and len(c_line) > 1:
                print(f'{file_path}: Line {c_line_num}: {ERRORS_DICT.get("Indentation")} '
                      f'Line indent not a multiple of four')

    def file_reader(self) -> tuple:
        """ Loops through the provided file_or_dir yielding each line and it's corresponding
        line num of the file_or_dir.
        one by one.
        :returns an empty tuple if the provided file_or_dir does not exist.
        """
        c_line = 1
        try:
            if is_file:
                with open(self.file) as file_:
                    for line in file_:
                        yield line, c_line, self.file
                        c_line += 1
            elif is_dir:
                for dir_path, dir_names, file_names in os.walk(self.file):
                    for name in file_names:
                        file_path = os.path.join(dir_path, name)
                        with open(file_path) as file_:
                            for line in file_:
                                yield line, c_line, file_path
                                c_line += 1
                        c_line = 1
        except FileNotFoundError:
            return ()


if __name__ == '__main__':
    Analyser()
