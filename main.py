import logging
from logging.config import fileConfig
from typing import TextIO, Iterator, Match
import re

fileConfig("log.ini")

logger = logging.getLogger('dev')

BRACKET_PATTERN = r"\(([0-9+*]+)\)"

ADDITTION_PATTERN = r"(\d+)\+(\d+)"

MULTIPLICATION_PATTERN = r"(\d+)\*(\d+)"


def get_input_data(file_name: str) -> Iterator[str]:
    f: TextIO = open(file_name)
    processed_line_iterator = map(lambda s: s.replace(" ", ""), map(lambda s: s.strip(), f.readlines()))
    f.close()
    return processed_line_iterator


def solve_line(line: str) -> int:
    match: Match
    while re.search(BRACKET_PATTERN, line):
        match = re.search(BRACKET_PATTERN, line)
        line = line.replace(match.group(0), str(solve_line(match.group(1))))
    current_operator: str = "+"
    current_value: int = 0
    for symb in map(lambda m: m.group(0), re.finditer(r"\d+|[*+]", line)):
        if symb in ["+", "*"]:
            current_operator = symb
        else:
            if current_operator == "+":
                current_value += int(symb)
            else:
                current_value *= int(symb)
    return current_value


def solve_line_prec(line: str) -> int:
    match: Match
    while re.search(BRACKET_PATTERN, line):
        match = re.search(BRACKET_PATTERN, line)
        line = line.replace(match.group(0), str(solve_line_prec(match.group(1))))
    logger.debug(line)
    while re.search(ADDITTION_PATTERN, line):
        match = re.search(ADDITTION_PATTERN, line)
        logger.debug(match)
        line = re.sub(ADDITTION_PATTERN, str(int(match.group(1))+int(match.group(2))), line, 1)
        logger.debug(line)
    while re.search(MULTIPLICATION_PATTERN, line):
        match = re.search(MULTIPLICATION_PATTERN, line)
        logger.debug(match)
        line = re.sub(MULTIPLICATION_PATTERN, str(int(match.group(1))*int(match.group(2))), line, 1)
        logger.debug(line)
    return int(line)


def solution_part_1(file_name: str) -> int:
    sum_value: int = 0
    for line in get_input_data(file_name):
        sum_value += solve_line(line)
        logger.debug(solve_line(line))
    return sum_value


def solution_part_2(file_name: str) -> int:
    sum_value: int = 0
    for line in get_input_data(file_name):
        sum_value += solve_line_prec(line)
        logger.debug(solve_line_prec(line))
    return sum_value


if __name__ == '__main__':
    logger.info(f"Summe: {solution_part_1('inputData.txt')}")
    logger.info(f"Summe: {solution_part_2('inputData.txt')}")
