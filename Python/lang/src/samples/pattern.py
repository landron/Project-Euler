"""
pylint, flake8

Knowledge base
    1.  "Files using ASCII (in Python 2) or UTF-8 (in Python 3) should
    not have an encoding declaration."
        https://www.python.org/dev/peps/pep-0008/
"""

import time


USE_LIB = False

if USE_LIB:
    # from project_euler.proj_euler import get_primes
    pass
else:
    # import math
    pass


def solve(limit):
    """
    Return the solution of the problem.
    """
    return limit


def parse_input():
    """
    read input and solve the problem as defined on HackerRank
    """
    limit, _ = (int(i) for i in input().strip().split())
    solution = solve(limit)
    solution.sort()
    for i in solution:
        print(i, end="")
    print()


def problem():
    """
    Solve the problem as formulated on the original site.
    """
    start = time.time()

    result = solve(666)

    duration = time.time() - start
    if duration >= 1:
        print(f"Result {result} in {duration:.2f} seconds")
    else:
        print(result)


def debug_validations():
    """
    unit tests

    pass -O to ignore assertions and gain some time:
        python -O ./prob.py
    """


if __name__ == "__main__":
    debug_validations()

    # original problem
    problem()

    # harden/generalized HackerRank problem
    # parse_input()
