"""
    This is private code.

    https://projecteuler.net/problem=61
    https://www.hackerrank.com/contests/projecteuler/challenges/euler061/problem
        WIP
        todo_hackerrank 

    pylint, flake8
"""
import time


USE_LIB = True

if USE_LIB:
    from project_euler.proj_euler import get_combinatorics_start
else:
    # import math
    pass


def set_dic(dic, number):
    '''
        add dictionary entry: half a number
    '''
    idx = number//100
    if idx in dic:
        dic[idx].append(number)
    else:
        dic[idx] = [number]


def gen_triangle():
    '''
        triangle numbers dictionary
    '''
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i*(i+1)//2
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i*(i+1)//2
        i += 1
    return dic


def gen_square():
    '''
        square numbers dictionary
    '''
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i*i
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i*i
        i += 1
    return dic


def gen_pentagonal():
    '''
        pentagonal numbers dictionary
    '''
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i*(3*i-1)//2
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i*(3*i-1)//2
        i += 1
    return dic


def gen_hexagonal():
    '''
        hexagonal numbers dictionary
    '''
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i*(2*i-1)
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i*(2*i-1)
        i += 1
    return dic


def gen_heptagonal():
    '''
        heptagonal numbers dictionary
    '''
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i*(5*i-3)//2
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i*(5*i-3)//2
        i += 1
    return dic


def gen_octogonal():
    '''
        octogonal numbers dictionary
    '''
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i*(3*i-2)
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i*(3*i-2)
        i += 1
    return dic


def find_solution_step(dicts, order, solution):
    '''
        Recursively complete the solution chain.
    '''
    if len(solution) == 6:
        first = solution[0][0]
        last = solution[-1][0]
        total = 0
        if first//100 == last % 100:
            for i in solution:
                total += i[0]
            print(solution, total)
        return total
    assert len(solution) < 6
    position = len(solution) - 1
    prev = solution[-1][0]
    dic = dicts[1+order[position]]
    if prev % 100 not in dic:
        return 0
    total = 0
    for i in dic[prev % 100]:
        solution.append((i, 1+order[position]))
        res = find_solution_step(dicts, order, solution)
        if res:
            total = res
        solution.pop()
    return total


def find_solution(dicts, order):
    '''
        Solve with the given dictionaries for the current order.
    '''
    total = 0
    for i in dicts[0]:
        for j in dicts[0][i]:
            res = find_solution_step(dicts, order, [(j, 0)])
            if res:
                total = res
    return total


def solve(dicts_selection):
    '''
        Find the cyclic number:
        * generate all the numbers (triangle, square, etc) with
            4 digits, grouped by the first two digits.
        * generate all the permutations of the last 5 dictionaries
        * try to find a cycle in each permutation
    '''
    all_dicts = [gen_triangle(), gen_square(), gen_pentagonal(),
                 gen_hexagonal(), gen_heptagonal(), gen_octogonal()]
    dicts = []
    for i in dicts_selection:
        dicts.append(all_dicts[i-3])

    comb = get_combinatorics_start(False, 5)
    # print(comb.current())
    total = find_solution(dicts, comb.current())
    assert not total

    while comb.get_next():
        # print(comb.current())
        res = find_solution(dicts, comb.current())
        if res:
            total = res
    return total


def problem():
    """
        Solve the problem as formulated on the original site.
    """
    start = time.time()

    result = solve([3, 4, 5, 6, 7, 8])
    print(f"solve(): {result} in {time.time()-start:.2f}s")


def parse_input():
    '''
        read input and solve the problem as defined on HackerRank
    '''
    _ = int(input().strip())
    selection = []
    for i in [int(i) for i in input().strip().split()]:
        assert i not in selection
        selection.append(i)
        assert 3 <= i <= 8
    solution = solve(selection)
    solution.sort()
    for i in solution:
        print(i, end='')
    print()


def debug_validations():
    """all the assertions"""


if __name__ == "__main__":
    debug_validations()

    # original problem
    # problem()

    # harden/generalized HackerRank problem
    # parse_input()
