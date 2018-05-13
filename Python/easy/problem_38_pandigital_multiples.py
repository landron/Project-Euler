#!/bin/python3
'''
    https://projecteuler.net/problem=38
        Pandigital multiples

    https://www.hackerrank.com/contests/projecteuler/challenges/euler038

    pylint 1.8.1
        Your code has been rated at 9.85/10.

    tag_permutation, tag_digits
'''

PROJ_EULER = 1

if PROJ_EULER:
    import sys
    sys.path.append("..") # Adds higher directory to python modules path.
    # pylint: disable=import-error
    from proj_euler import get_permutation_start, get_permutation_next
    from proj_euler import get_digits
else:
    def get_permutation_next(indexes, taken, limit):
        '''
            Number (N, K) = N! / (N-K)!
        '''
        assert indexes
        max_i = len(indexes)-1
        assert indexes[max_i] < limit

        i = max_i

        # propagate the value change
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

        taken[indexes[i]] = True

        # give proper values to the remaining

        next_free = 0
        for j in range(i+1, max_i+1):
            while taken[next_free]:
                next_free += 1
                assert next_free != limit
            taken[next_free] = True
            indexes[j] = next_free

        # print(indexes, taken)

        return True

    def get_permutation_start(indexes, taken, limit, subset=0):
        '''
            initialisation; taken = used indexes (each index appears one time only)

            limit, subset = (usually known as) N, K
        '''
        if subset == 0:
            subset = limit

        # not like this: it will create another list
        # taken = [False] * limit
        for i in range(limit):
            taken.append(False)

        for i in range(subset):
            indexes.append(i)
            taken[i] = True

    def number_of_digits(number, base=10):
        """get the number of the digits of the given number in the given base"""
        digits = 0
        while number >= 1:
            number //= base
            digits += 1
        return digits

    # the result is in reversed order
    def get_digits(number, base=10):
        """get the digits of the given number in the given base"""
        digits = []
        while number >= 1:
            digits.append(number%base)
            number //= base
        return digits

##################################################################################################

def number_from_permutation(indexes, limit=0):
    '''get the number from the (reversed) digits'''
    assert limit <= len(indexes)
    if limit == 0:
        limit = len(indexes)
    max_digit = len(indexes)

    number = 0
    for i in range(limit):
        number *= 10
        number += (max_digit - indexes[i])
    return number

def is_prod(indexes, digits_n, idx, factor):
    '''
        is there a multiple contained in these digits ?
            = verify that the digits following idx is the product by factor
            of the number until digits_n
    '''
    assert digits_n != 0
    assert factor > 1

    prod = number_from_permutation(indexes, digits_n)*factor
    # list is reversed
    prod_idx = get_digits(prod)

    limit = len(indexes)
    if len(prod_idx)+idx > limit:
        return 0
    for i in range(len(prod_idx)):
        expected = prod_idx[len(prod_idx)-i-1]
        real = limit - indexes[idx+i]
        if expected != real:
            # print(prod_idx, indexes, idx)
            return 0
    return idx+len(prod_idx)

def get_solution(indexes, max_multiplier):
    '''
        max_multiplier: needed only for the hackerrank variant
    '''
    # number of digits in the number < n/2 to contain at least 2 numbers (x, x*2)
    for i in range(len(indexes)//2):
        if max_multiplier != 0:
            mul = number_from_permutation(indexes, i+1)
            # print(mul)
            if  mul >= max_multiplier:
                return 0
        j = i+1
        prod = 2
        while j < len(indexes):
            j = is_prod(indexes, i+1, j, prod)
            if j == 0:
                # print("Failed: ", i, j, prod)
                break
            assert j <= len(indexes)
            prod += 1
        if j != 0:
            return number_from_permutation(indexes, i+1)
    return 0

def is_solution(indexes):
    '''are the given digits a solution ?'''
    return get_solution(indexes, 0) != 0

def solve_problem(no_digits, max_multiplier=0, stop_when_found=True):
    '''
        0 is excluded among digits
    '''

    multipliers = []

    # generate all the pandigital numbers

    indexes = []
    taken = []
    get_permutation_start(indexes, taken, no_digits)
    # print(indexes)
    # print(number_from_permutation(indexes))
    if is_solution(indexes):
        # get_solution ignored here
        return number_from_permutation(indexes)
    while get_permutation_next(indexes, taken, no_digits):
        # print(indexes)
        # print(number_from_permutation(indexes))
        mul = get_solution(indexes, max_multiplier)
        # 0 = no solution, 1 = direct soltuion
        if mul > 1:
            if stop_when_found:
                return number_from_permutation(indexes)
            multipliers.append(mul)

    return 0 if stop_when_found else multipliers

def parse_input():
    '''
        solve the problem as defined on hackerrank
        https://www.hackerrank.com/contests/projecteuler/challenges/euler038
    '''
    (N, K) = [int(j) for j in input().strip().split(' ')]
    sol = solve_problem(K, N, False)
    sol.sort()
    for i in sol:
        print(i)

def problem():
    '''
        solve the problem as defined on project Euler site
    '''
    return solve_problem(9)

def debug_assertions():
    '''unit tests'''
    assert number_from_permutation([0, 3, 8, 5, 1, 4, 7, 6, 2]) == 961485237
    assert number_from_permutation([0, 3, 8, 5, 1, 6, 2, 4, 7]) == 961483752
    assert number_from_permutation([0, 3, 8, 5, 1, 6, 2, 7, 4]) == 961483725
    # 918273645
    assert is_solution([0, 8, 1, 7, 2, 6, 3, 5, 4])
    assert not is_solution([0, 1, 8, 7, 2, 6, 3, 5, 4])
    assert not is_solution([0, 8, 1, 7, 2, 6, 3, 4, 5])
    # 192384576
    assert is_solution([8, 0, 7, 6, 1, 5, 4, 2, 3])
    assert not is_solution([8, 1, 7, 6, 0, 5, 4, 2, 3])
    assert not is_solution([0, 8, 1, 2, 7, 3, 4, 6, 5])
    # 932718654
    assert is_solution([0, 6, 7, 2, 8, 1, 3, 4, 5])
    # 18365472 = 8 pandigital
    assert is_solution([7, 0, 5, 2, 3, 4, 1, 6])
    assert not is_solution([7, 0, 5, 4, 3, 2, 1, 6])
    assert is_solution([1, 0, 7, 3, 2, 6, 5, 4])

def main():
    '''main: unit tests, project Euler, hackerrank'''
    debug_assertions()

    # project Euler
    # print(problem())

    # hackerrank
    # print(solve_problem(8, 100, False))
    # print(solve_problem(9, 1000, False))
    # parse_input()

if __name__ == "__main__":
    main()
