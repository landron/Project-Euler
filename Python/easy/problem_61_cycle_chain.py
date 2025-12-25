"""
This is private code.

https://projecteuler.net/problem=61
https://www.hackerrank.com/contests/projecteuler/challenges/euler061/problem

pylint, flake8
"""

import time


USE_LIB = True

if USE_LIB:
    from project_euler.proj_euler import get_combinatorics_start
else:

    class Combinatorics:
        """
        Generate k-permutations & combinations
        """

        def __init__(self, is_combinations, limit, limit_subset=0):
            """
            initialisation
            taken = used indexes (each index appears one time only)
            """
            self.is_combinations = is_combinations

            assert limit_subset <= limit
            if limit_subset == 0:
                limit_subset = limit

            self.taken = [False] * limit
            self.indexes = []

            for i in range(limit_subset):
                self.indexes.append(i)
                self.taken[i] = True

        def get_limit(self):
            """
            the superior limit of our groupings
            """
            return len(self.taken)

        def get_limit_subset(self):
            """
            the count of our generated set
            """
            return len(self.indexes)

        def current(self):
            """
            current permutation/combination
            """
            return self.indexes

        @staticmethod
        def get_combinatorics_next(indexes, taken, is_combinations):
            """
            P(n,k) = k-permutations of n
                Number (n, k) = n! / (n-k)!
            k-combination of a set

            n & k are deduced (not explicitly set):
                n = len(taken)
                k = len(indexes)
            """
            assert is_combinations in [True, False]
            assert indexes and taken

            max_i = len(indexes) - 1
            limit = len(taken)
            assert indexes[max_i] < limit

            i = max_i

            found = False
            while not found:
                found = True

                # propagate the value change
                #   if the limit is reached, we increment the previous digits
                #   (like for a number base "limit")

                taken[indexes[i]] = False
                indexes[i] += 1

                while indexes[i] == limit or taken[indexes[i]]:
                    if indexes[i] == limit:
                        if i == 0:
                            return False
                        i -= 1
                        # available now
                        taken[indexes[i]] = False
                    indexes[i] += 1
                assert indexes[i] != limit, "test"

                taken[indexes[i]] = True

                # give proper values to the remaining

                if not is_combinations:
                    next_free = 0
                    for j in range(i + 1, max_i + 1):
                        while taken[next_free]:
                            next_free += 1
                            assert next_free != limit
                        taken[next_free] = True
                        indexes[j] = next_free
                else:
                    # taken ignored
                    for j in range(i + 1, max_i + 1):
                        indexes[j] = indexes[j - 1] + 1
                        if indexes[j] == limit:
                            found = False
                            break

            # print(indexes, taken)

            return True

        def get_next(self):
            """
            get the next combination/permutation
            """
            if not Combinatorics.get_combinatorics_next(
                self.indexes, self.taken, self.is_combinations
            ):
                self.indexes = []
                return None
            return self.current()

    def get_combinatorics_start(is_combinatorics, limit, limit_subset=0):
        """
        limit, limit_subset = (usually known as) n, k
            P(n,k) = k-permutations of n
        """
        return Combinatorics(is_combinatorics, limit, limit_subset)


def set_dic(dic, number):
    """
    add dictionary entry: half a number
    """
    idx = number // 100
    if idx in dic:
        dic[idx].append(number)
    else:
        dic[idx] = [number]


def gen_triangle():
    """
    triangle numbers dictionary
    """
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i * (i + 1) // 2
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i * (i + 1) // 2
        i += 1
    return dic


def gen_square():
    """
    square numbers dictionary
    """
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i * i
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i * i
        i += 1
    return dic


def gen_pentagonal():
    """
    pentagonal numbers dictionary
    """
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i * (3 * i - 1) // 2
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i * (3 * i - 1) // 2
        i += 1
    return dic


def gen_hexagonal():
    """
    hexagonal numbers dictionary
    """
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i * (2 * i - 1)
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i * (2 * i - 1)
        i += 1
    return dic


def gen_heptagonal():
    """
    heptagonal numbers dictionary
    """
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i * (5 * i - 3) // 2
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i * (5 * i - 3) // 2
        i += 1
    return dic


def gen_octogonal():
    """
    octogonal numbers dictionary
    """
    i = 1
    next_one = 1
    dic = {}
    while next_one < 10**3:
        next_one = i * (3 * i - 2)
        i += 1
    while next_one < 10**4:
        set_dic(dic, next_one)
        next_one = i * (3 * i - 2)
        i += 1
    return dic


def find_current_step(dicts, order, current, solutions):
    """
    Recursively complete the current chain.
    """
    size = len(dicts)

    if len(current) == size:

        def get_sum(solution, size):
            if solution[0][0] // 100 != solution[-1][0] % 100:
                return 0
            # validate solution: distinct numbers
            #     needed for hackerrank, not project Euler
            unique = [0] * size
            for i, _ in enumerate(solution):
                unique[i] = solution[i][0]
            unique = set(unique)
            if len(unique) < size:
                return 0
            total = 0
            for i in unique:
                total += i
            return total

        total = get_sum(current, size)
        if total:
            # print(current, total)
            solutions.append(total)
        return

    assert len(current) < size
    position = len(current) - 1
    prev = current[-1][0]
    dic = dicts[1 + order[position]]
    if prev % 100 not in dic:
        return
    for i in dic[prev % 100]:
        current.append((i, 1 + order[position]))
        find_current_step(dicts, order, current, solutions)
        current.pop()


def find_current(dicts, order, solutions):
    """
    Solve with the given dictionaries for the current order.
    """
    for i in dicts[0]:
        for j in dicts[0][i]:
            find_current_step(dicts, order, [(j, 0)], solutions)


def solve(dicts_selection):
    """
    Find the cyclic number:
    * generate all the numbers (triangle, square, etc) with
        4 digits, grouped by the first two digits.
    * generate all the permutations of the last 5 dictionaries
    * try to find a cycle in each permutation
    """
    all_dicts = [
        gen_triangle(),
        gen_square(),
        gen_pentagonal(),
        gen_hexagonal(),
        gen_heptagonal(),
        gen_octogonal(),
    ]
    dicts = []
    for i in dicts_selection:
        dicts.append(all_dicts[i - 3])

    comb = get_combinatorics_start(False, len(dicts_selection) - 1)
    # print(comb.current())
    solutions = []
    find_current(dicts, comb.current(), solutions)

    while comb.get_next():
        # print(comb.current())
        find_current(dicts, comb.current(), solutions)
    return solutions


def problem():
    """
    Solve the problem as formulated on the original site.
    """
    start = time.time()

    selection = [3, 4, 5, 6, 7, 8]
    result = solve(selection)
    print(f"solve({selection}): {result} in {time.time() - start:.2f}s")


def parse_input():
    """
    read input and solve the problem as defined on HackerRank
    """
    _ = int(input().strip())
    selection = []
    for i in [int(i) for i in input().strip().split()]:
        assert i not in selection
        selection.append(i)
        assert 3 <= i <= 8
    current = solve(selection)
    if current:
        # remove duplicates
        current = list(set(current))
        current.sort()
        for i in current:
            print(i)
        print()


def debug_validations():
    """all the assertions"""


if __name__ == "__main__":
    debug_validations()

    # original problem
    # problem()

    # harden/generalized HackerRank problem
    # parse_input()
