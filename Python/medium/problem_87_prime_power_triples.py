"""
https://projecteuler.net/problem=87
Prime Power Triples

Medium: HackerRank optimization
"""

import bisect
import time
import math

from project_euler.proj_euler import get_primes


def solve_base(limit):
    """
    Return the solution of the problem.

    """
    primes = get_primes(math.ceil(math.sqrt(limit)))

    solutions = set()
    for i in primes:
        for j in primes:
            current_j = i * i + j**3
            if current_j >= limit:
                break
            for k in primes:
                # print(i,j,k)
                current_k = current_j + k**4
                if current_k >= limit:
                    break
                solutions.add(current_k)
    return solutions


def parse_input():
    """
    read input and solve the problem as defined on HackerRank

    Computing the solutions is expensive, so we do it only once. Inspired
    by discussions on forum.
    Otherwise: 3/8 tests successful, 5/8 timeouts.
    """
    solutions = sorted(list(solve_base(10**7)))

    count = int(input().strip())
    for _ in range(count):
        limit = int(input().strip())
        result = bisect.bisect_right(solutions, limit)
        print(result)


def solve(limit):
    """
    Returns the number of solutions.
    """
    return len(solve_base(limit))


def problem():
    """
    Solve the problem as formulated on the original site.
    """
    start = time.time()

    result = solve(50_000_000)

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
    assert solve(50) == 4
    assert solve(100) == 10
    assert solve(1000) == 98


if __name__ == "__main__":
    debug_validations()

    # original problem
    # problem()

    # harden/generalized HackerRank problem
    parse_input()
