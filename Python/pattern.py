"""
    pylint, flake8
"""
import time


USE_LIB = False

if USE_LIB:
    # from lib.proj_euler import get_primes
    pass
else:
    # import math
    pass


def parse_input():
    '''
        read input and solve the problem as defined on hackerrank
    '''
    limit, terms_no = (int(i) for i in input().strip().split())
    solution = solve(limit, terms_no)
    solution.sort()
    for i in solution:
        print(i, end='')
    print()


def solve(limit, terms_no=0):  # pylint: disable=unused-argument
    '''
        Solve problem and return the solution
    '''
    return limit


def problem():
    """solve the problem, print the needed time"""
    start = time.time()

    result = solve(666)
    assert result == 666
    print("Result {0} in {1:.2f} seconds".format(result, time.time()-start))


def debug_validations():
    """all the assertions"""


if __name__ == "__main__":
    debug_validations()

    # original problem
    print(problem())

    # harden/generalized problem
    # parse_input()
