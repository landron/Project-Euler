"""
This is private code.

"Counting rectangles"
https://projecteuler.net/problem=85
https://www.hackerrank.com/contests/projecteuler/challenges/euler085

pylint, flake8
"""

import math
import time


USE_LIB = True

if USE_LIB:
    # from lib.proj_euler import get_primes
    pass
else:
    # import math
    pass


def count_rectangles_calculate(height, width):
    """the number of rectangles contained in the given one
    by formula
    """
    count_by_width = width * (width + 1) // 2
    count = height * (height + 1) * count_by_width // 2
    return count


def count_rectangles_brute(height, width):
    """the number of rectangles contained in the given one
    by brute force
    """
    count = 0
    for i in range(height):
        for j in range(width):
            count += (height - i) * (width - j)
    return count


def count_rectangles(height, width):
    """the number of rectangles contained in the given one"""
    return count_rectangles_calculate(height, width)


def solve_try_around_square(limit, debug=False):
    """
    Return the solution of the problem:
        * find the closest square to the limit
        * try find a better solution around it

    Fails miserably on hackerrank.
    """
    i = 1
    count = count_rectangles(i, i)
    while count < limit:
        i += 1
        count = count_rectangles(i, i)
        if debug:
            print(i, count)

    best = (count, i, i)
    count = count_rectangles(i - 1, i - 1)
    if abs(count - limit) < abs(best[0] - limit):
        best = (count, i - 1, i - 1)

    pivot = best[1]
    to_try = max(pivot // 2, 10)
    for i in range(to_try):
        for j in range(to_try):
            count = count_rectangles(pivot - i, pivot + j)
            if abs(count - limit) < abs(best[0] - limit):
                best = (count, pivot - i, pivot + j)
                if debug:
                    print("new best", pivot - i, pivot + j, count)
            elif abs(count - limit) == abs(best[0] - limit):
                if best[1] * best[2] < (pivot - i) * (pivot + j):
                    best = (count, pivot - i, pivot + j)

    return best[1] * best[2]


def solve_calculate(limit, debug=False):
    """
    Try them all, but smartly: calculate the other factor:
        Number = height*(height+1)*width*(width+1)/4
    """
    best = (0, 0, 0)

    def eval_best(best, attempt, limit, debug):
        if abs(attempt[0] - limit) > abs(best[0] - limit):
            return best
        if abs(attempt[0] - limit) == abs(best[0] - limit):
            # get bigger surface
            if attempt[1] * attempt[2] <= best[1] * best[2]:
                return best
        if debug:
            print("new best:", attempt)
        return attempt

    height = 1
    width = round(math.sqrt(limit * 4 / (height * (height + 1))))
    while height <= width:
        for i in range(2):
            count = count_rectangles_calculate(height, width - 1 + i)
            best = eval_best(best, (count, height, width - 1 + i), limit, debug)
        height += 1
        width = round(math.sqrt(limit * 4 / (height * (height + 1))))

    return best[1] * best[2]


def solve(limit, debug=False):
    """
    Return the solution of the problem.
    """
    return solve_calculate(limit, debug)
    # return solve_try_around_square(limit, debug)


def parse_input():
    """
    read input and solve the problem as defined on HackerRank
    """
    test_cases = int(input().strip())
    for _ in range(test_cases):
        limit = int(input().strip())
        solution = solve(limit)
        print(solution)


def problem():
    """
    Solve the problem as formulated on the original site.
    """
    start = time.time()

    value = 2000000
    result = solve(value)
    print(f"solve({value}): {result} in {time.time() - start:.2f}s")


def debug_validations():
    """all the assertions"""
    assert count_rectangles_brute(2, 3) == 18
    assert count_rectangles_brute(3, 2) == 18
    assert count_rectangles_brute(2, 2) == 9
    assert count_rectangles_brute(3, 3) == 36
    assert count_rectangles_calculate(2, 3) == 18
    assert count_rectangles_calculate(3, 2) == 18
    assert count_rectangles_calculate(2, 2) == 9
    assert count_rectangles_calculate(3, 3) == 36
    assert count_rectangles_calculate(3, 4) == count_rectangles_brute(3, 4)
    assert count_rectangles_calculate(3, 5) == count_rectangles_brute(3, 5)
    assert count_rectangles_calculate(5, 5) == count_rectangles_brute(5, 5)
    assert count_rectangles_calculate(1, 6) == count_rectangles_brute(1, 6)

    assert solve_try_around_square(18) == 6  # 2,3
    assert solve_try_around_square(21) == 6  # 1,6
    assert solve_try_around_square(2) == 2
    assert solve_calculate(18) == 6  # 2,3
    assert solve_calculate(21) == 6  # 1,6
    assert solve_calculate(2) == 2

    assert solve_calculate(100) == 16
    assert solve_calculate(101) == 16
    assert solve_calculate(103) == 14


if __name__ == "__main__":
    debug_validations()

    # original problem
    # problem()
    print(solve_calculate(105, True))

    # harden/generalized HackerRank problem
    # parse_input()
