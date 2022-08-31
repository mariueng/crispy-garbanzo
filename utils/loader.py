from typing import Tuple


def load_puzzle(puzzle: str) -> Tuple[set, list, str]:
    """ Load verbal aritmetic puzzles from a string and converts it into a list of chars. """
    lhs, rhs = puzzle.replace(' ', '').split('=')
    lhs_terms: list[str] = lhs.split('+')
    variables = set(rhs)
    variables.update([l for l in ''.join(lhs_terms)])

    return (variables, lhs_terms, rhs)
