import itertools
from multiprocessing import Pool, Process, cpu_count


# Multiprocessing settings
NUM_PROCESSES = cpu_count()


def get_sum(term: str, substitution: dict) -> int:
    """ Return the numerical sum of a word given a substitution dictionary for each letter """
    s: int = 0
    factor: int = 1
    letter: str
    for letter in reversed(term):
        s += factor * substitution[letter]
        factor *= 10
    return s


def split(input: list, n: int) -> list:
    """ Yields successive n-sized chunks of input """
    for i in range(0, len(input), n):
        yield input[i:i + n]


def constraints_valid(solution: dict, constraints: dict) -> bool:
    """ Check if the constraints are valid """
    for key, value in constraints.items():
            if solution[key] == value: return False
    return True


def check_solutions(permutations: list, variables: set, lhs_terms: list, rhs: str, constraints: dict) -> dict:
    """ Check for solutions in permutations """
    permutations_left: bool = True
    while permutations_left:
        for permutation in permutations:
            solution: dict = dict(zip(variables, permutation))
            if not constraints_valid(solution, constraints): continue

            # Check if sum of left side equals right side
            if sum(get_sum(term, solution) for term in lhs_terms) == get_sum(rhs, solution):
                return {v: k for k, v in solution.items()}
        permutations_left = False        


def terminate(solution):
    """ Terminate all processes running in the pool """
    print(f"Exiting with solution: {solution}")
    pool.terminate()


def bf_solver(variables: set, lhs_terms: list, rhs: str, constraints: dict, multiprocess: bool = False) -> dict:
    """ Solve verbal arithmetic CSP by shear bruteforce """

    # Domain
    digits: list = [*range(10)]

    # Solution space
    permutations = list(itertools.permutations(digits, len(variables)))

    if multiprocess:
        print(f"Running multiprocessing with {NUM_PROCESSES} cores...")

        split_permutations = list(split(permutations, int(len(permutations) / NUM_PROCESSES) + 1))

        global pool
        pool = Pool(NUM_PROCESSES)
        for i in range(NUM_PROCESSES):
            pool.apply_async(check_solutions, args=(split_permutations[i], variables, lhs_terms, rhs, constraints), callback=terminate)
        pool.close()
        pool.join()

    else:
        return check_solutions(permutations, variables, lhs_terms, rhs, constraints)