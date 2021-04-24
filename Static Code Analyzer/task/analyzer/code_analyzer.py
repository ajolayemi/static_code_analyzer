#!/usr/bin/env python

import os

MAX_LINE_LEN = 79

ERRORS_DICT = {'Long Line': 'S001',
               'Indentation': 'S002',
               'Statement Semicolon': 'S003',
               'Inline Comments': 'S004',
               'TODO Found': 'S005',
               'Many blank lines': 'S006'}

file = input()

valid_file = os.path.exists(file)


class Analyser:
    """ A simple static code analyser. """
    def __init__(self, file_to_analyse: str = file):
        self.file = file_to_analyse

    def analyze_file(self) -> list[list]:
        """
        Reads through each line in the file and checks to see if each line len <= 79
        Returns a nested list containing the numbers of lines with len > 79 and there len"""
        c_line = 1
        invalid_lines = []
        try:
            with open(self.file) as file_:
                for line in file_:
                    if len(line.strip()) > 79:
                        invalid_lines.append([c_line, len(line.strip())])
                        c_line += 1
                    else:
                        c_line += 1
                return invalid_lines, True
        except FileNotFoundError:
            return [], False, 0


def main():
    pass


if __name__ == '__main__':
    main()
