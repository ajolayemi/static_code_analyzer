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
    previous_blanks = 0

    def __init__(self, file_to_analyse: str = file):
        self.file = file_to_analyse
        self.invalid_file = os.path.exists(self.file)
        self.all_errors = {}

        current_line = self.file_reader()
        while True:
            try:
                c_line = next(current_line)
                self.check_indent_error(c_line)
                self.check_for_semicolon(c_line)
                self.check_inline_comment(c_line)
                self.check_to_do(c_line)
                self.check_blank_lines(c_line)
            except StopIteration:
                break

    @staticmethod
    def check_blank_lines(current_line):
        if current_line:
            c_line, c_line_num = current_line
            if len(c_line) == 1:
                Analyser.previous_blanks += 1
            else:
                if Analyser.previous_blanks > 2:
                    print(f'Line: {c_line_num}: {ERRORS_DICT.get("Blank lines")} More than two blank'
                          f' lines preceding a code line')
                    Analyser.previous_blanks = 0

    @staticmethod
    def check_to_do(current_line):
        if current_line:
            c_line, c_line_num = current_line
            comment = c_line[c_line.find('#'):].lower()
            if 'todo' in comment:
                print(f'Line {c_line_num}: {ERRORS_DICT.get("TODO")} TODO found')

    @staticmethod
    def check_inline_comment(current_line):
        if current_line:
            c_line, c_line_num = current_line
            line_str = f'Line {c_line_num}'
            if '#' in c_line and not c_line.startswith('#'):
                if not c_line.split('#')[0].endswith('  '):
                    print(f'{line_str}: {ERRORS_DICT.get("Inline Comments")} At least two spaces required'
                          f' before inline comments')

    def check_for_semicolon(self, current_line):
        """ Checks for the presence of unnecessary
        semicolons in statements """
        if current_line:
            c_line, c_line_num = current_line
            line_without_comment = self.remove_comment_in_a_string(c_line)
            if line_without_comment.endswith(';'):
                print(f'Line {c_line_num}: {ERRORS_DICT.get("Semicolon")} Unnecessary semicolon')

    @staticmethod
    def remove_comment_in_a_string(string):
        if '#' in string:
            return string[:string.index('#')].strip()
        else:
            return string

    @staticmethod
    def check_indent_error(current_line):
        if current_line:
            c_line, c_line_num = current_line
            indent_num = len(c_line) - len(c_line.lstrip())
            if indent_num % 4 > 0 and len(c_line) > 1:
                print(f'Line {c_line_num}: {ERRORS_DICT.get("Indentation")} '
                      f'Line indent not a multiple of four')

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


if __name__ == '__main__':
    Analyser()
