#!/usr/bin/env python

import os

MAX_LINE_LEN = 79

ERRORS_DICT = {'Long Line': 'S001',
               'Indentation': 'S002',
               'Semicolon': 'S003',
               'Inline Comments': 'S004',
               'TODO': 'S005',
               'Blank lines': 'S006'}
indent_pattern = r'^ +'
file = input()

valid_file = os.path.exists(file)


class Analyser:
    """ A simple static code analyser. """
    def __init__(self, file_to_analyse: str = file):
        self.file = file_to_analyse
        self.invalid_file = os.path.exists(self.file)
        self.all_errors = {}

    def check_inline_comment(self):
        pass

    def check_for_semicolon(self):
        """ Checks for the presence of unnecessary
        semicolons in statements """
        current_line = self.file_reader()
        if current_line:
            try:
                while True:
                    c_line, c_line_num = next(current_line)
                    line_str = f'Line {c_line_num}'
                    line_without_comment = self.remove_comment_in_a_string(c_line)
                    if line_without_comment.endswith(';'):
                        if line_str in self.all_errors:
                            self.all_errors[line_str].append([ERRORS_DICT.get('Semicolon'),
                                                             c_line_num])
                        else:
                            self.all_errors[line_str] = []
                            self.all_errors[line_str].append([ERRORS_DICT.get('Semicolon'),
                                                             c_line_num])
            except StopIteration:
                pass

    @staticmethod
    def remove_comment_in_a_string(string):
        if '#' in string:
            return string[:string.index('#')].strip()
        else:
            return string

    def check_indent_error(self):
        current_line = self.file_reader()
        if current_line:
            try:
                while True:
                    c_line, c_line_num = next(current_line)
                    line_str = f'Line {c_line_num}'
                    indent_num = len(c_line) - len(c_line.lstrip())
                    if indent_num % 4 > 0 and len(c_line) > 1:
                        if line_str in self.all_errors:
                            self.all_errors[line_str].append([ERRORS_DICT.get('Indentation'),
                                                              c_line_num])
                        else:
                            self.all_errors[line_str] = []
                            self.all_errors[line_str].append([ERRORS_DICT.get('Indentation'),
                                                              c_line_num])
            except StopIteration:
                pass

    def file_reader(self) -> tuple:
        """ Loops through the provided file yielding each line and it's corresponding
        line num of the file.
        one by one.
        :returns an empty tuple if the provided file does not exist.
        """
        c_line = 1
        try:
            with open(self.file) as file_:
                for line in file_:
                    yield line, c_line
                    c_line += 1
        except FileNotFoundError:
            return ()


def main():
    s = Analyser()
    s.check_indent_error()
    s.check_for_semicolon()
    print(s.all_errors)


if __name__ == '__main__':
    main()
