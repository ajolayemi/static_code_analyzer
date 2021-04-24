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


def analyze_file(file_to_analyse: str = file) -> list[list]:
    """ :param file_to_analyse: a file path pointing to a valid
    python file.
    Reads through each line in the file and checks to see if each line len <= 79
    Returns a nested list containing the numbers of lines with len > 79 and there len"""
    c_line = 1
    invalid_lines = []
    try:
        with open(file_to_analyse) as file_:
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
    check = analyze_file()
    if all((check[0], check[1])):
        for long_line in check[0]:
            line, line_len = long_line
            print(f'Line {line}: S001 The line was {line_len - MAX_LINE_LEN} chars too long')

    elif not check[0] and check[1]:
        pass

    else:
        print(f'The provided file - {file} does not exist!')


if __name__ == '__main__':
    main()
