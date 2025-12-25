#! /usr/bin/python3
"""
https://projecteuler.net/problem=39

https://www.hackerrank.com/contests/projecteuler/challenges/euler039
    todo_hackerrank:    33.33
    WIP:    WIP_solve_problem_2

"Your code has been rated at 9.91/10"
pylint --version
    No config file found, using default configuration
    pylint 1.8.1,
    astroid 1.6.0
    Python 3.6.4
"""


def create_right_triangles():
    """create the structure used as cache"""

    def cache():
        pass

    cache.limit = 0
    cache.squares = {}
    cache.perimeters = None  # solve_problem_2
    return cache


def gen_right_triangles(limit):
    """generate the squares up to the limit"""
    cache = create_right_triangles()
    cache.limit = limit
    for i in range(2, limit):
        cache.squares[i * i] = i
    return cache


def adjust_right_triangles(cache, limit):
    """enlarge the cache up to the new limit"""
    assert cache.limit < limit

    for i in range(cache.limit, limit):
        cache.squares[i * i] = i
    cache.limit = limit


def unused_solve_problem(limit, cache):
    """solve the problem up to the NEW given limit using the old cache
        Score: 0.00
        #1-#2 : wrong answer; #3-#6 : timeouts

    good enough for project Euler
    """

    prev_limit = cache.limit
    if limit > cache.limit:
        adjust_right_triangles(cache, limit)

    perimeters = [0] * (limit - prev_limit + 1)

    # recalculation is unfortunately needed
    # for i in range(prev_limit, limit):
    for i in range(1, limit):
        for j in range(i + 1, limit):
            sum_of_squares = i * i + j * j
            if sum_of_squares in cache.squares:
                k = cache.squares[sum_of_squares]
                perimeter = i + j + k
                if perimeter <= limit and perimeter > prev_limit:
                    perimeters[perimeter - prev_limit] += 1

    # print('Perimeters calculated', perimeters, cache.solution.value)

    max_solutions_index = -1
    max_solutions = cache.solution.value
    for i in range(1, limit - prev_limit + 1):
        if perimeters[i] > max_solutions:
            # print(perimeters[i], max_solutions)
            max_solutions = perimeters[i]
            max_solutions_index = i

    if max_solutions_index != -1:
        cache.solution.index = prev_limit + max_solutions_index
        cache.solution.value = max_solutions

    return cache.solution.index


def solve_problem_1(limit, cache):
    """direct solution

    Score: 33.33    #3-#6 : timeouts
    """

    if limit > cache.limit:
        adjust_right_triangles(cache, limit)

    perimeters = [0] * (limit + 1)
    max_cathetus = limit // 2

    max_solutions_index = 0

    for i in range(1, max_cathetus):
        for j in range(i + 1, max_cathetus):
            sum_of_squares = i * i + j * j
            if sum_of_squares in cache.squares:
                k = cache.squares[sum_of_squares]
                perimeter = i + j + k
                if perimeter <= limit:
                    perimeters[perimeter] += 1
                    if perimeters[perimeter] > perimeters[max_solutions_index]:
                        max_solutions_index = perimeter

    return max_solutions_index


def WIP_solve_problem_2(limit, cache):
    """
    try to not calculate all the perimeters every time
    """

    prev_limit = cache.limit
    if not cache.perimeters:
        prev_limit = 0
        cache.perimeters = [0] * (limit + 1)

    if limit > cache.limit:
        adjust_right_triangles(cache, limit)
        cache.perimeters.extend([0] * (prev_limit - limit))

    perimeters = cache.perimeters
    max_cathetus = limit // 2
    # print(prev_limit, limit, cache.limit, max_cathetus)

    max_solutions_index = 0
    if prev_limit != 0:
        for i in range(1, prev_limit):
            # print(i, max_solutions_index, len(perimeters))
            if perimeters[i] > perimeters[max_solutions_index]:
                max_solutions_index = i

    for i in range(prev_limit // 2 + 1, max_cathetus):
        for j in range(i + 1, max_cathetus):
            sum_of_squares = i * i + j * j
            if sum_of_squares in cache.squares:
                k = cache.squares[sum_of_squares]
                perimeter = i + j + k
                if perimeter <= limit:
                    perimeters[perimeter] += 1
                    if perimeters[perimeter] > perimeters[max_solutions_index]:
                        max_solutions_index = perimeter

    print(perimeters)

    return max_solutions_index


def parse_input():
    """
    parse hackerrank input
    https://www.hackerrank.com/contests/projecteuler/challenges/euler039
    """

    cache = create_right_triangles()

    test_cases = int(input().strip())
    for _ in range(test_cases):
        limit = int(input().strip())
        print(solve_problem_1(limit, cache))


def solve_problem(limit):
    """solve the problem up to the given limit"""

    cache = create_right_triangles()
    return solve_problem_1(limit, cache)


def problem():
    """solve the project Euler problem"""

    print(solve_problem(1000))


def debug_assertions():
    """unit tests"""
    assert solve_problem(120) == 120

    cache = create_right_triangles()
    assert solve_problem_1(12, cache) == 12
    assert solve_problem_1(13, cache) == 12
    assert solve_problem_1(60, cache) == 60
    assert solve_problem_1(80, cache) == 60
    assert solve_problem_1(15, cache) == 12

    # WIP
    # cache = create_right_triangles()
    # assert solve_problem_2(12, cache) == 12
    # assert solve_problem_2(13, cache) == 12
    # assert solve_problem_2(60, cache) == 60
    # assert solve_problem_2(80, cache) == 60
    # assert solve_problem_2(15, cache) == 12


def main():
    """THE main"""
    debug_assertions()

    # parse_input()   # hackerrank
    problem()


if __name__ == "__main__":
    main()
