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
        self.invalid_file = os.path.exists(self.file)

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
                    yield line.strip(), c_line
                    c_line += 1
        except FileNotFoundError:
            return ()


def main():
    pass


if __name__ == '__main__':
    main()
