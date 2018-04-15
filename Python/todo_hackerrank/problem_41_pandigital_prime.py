#!/bin/python3
'''
    https://projecteuler.net/problem=41
        Pandigital primes
        Done, but the validation of the 8-digit primes takes already too much memory (2G)

    https://www.hackerrank.com/contests/projecteuler/challenges/euler041
        solve_problem_generate is very fast
        todo_hackerrank :   Score: 25.00 (2 ok, 3 timeouts)
            my cache (collections based) is not good enough
            neither the bisect based one

            cannot precalculate: too many
            optimization: verify that the numbers are pandigital and prime
                solve_problem_generate_testthem => no gain

    pylint 1.8.1
        Your code has been rated at 8.82/10.

    tag_cache
'''

import math
# import collections
import bisect

from proj_euler import get_primes
from proj_euler import get_digits, number_of_digits
from proj_euler import get_permutation_next, get_permutation_start

def is_pandigital(number_digits):
    assert len(number_digits) < 10

    arr = [False] * 10
    for i in number_digits:
        if arr[i]:
            return False
        arr[i] = True

    # 0 took a righteous position :(
    if arr[0]:
        return False
    for i in range(1, len(number_digits)+1):
        if not arr[i]:
            return False

    return True

def get_number(digits):
    """get the number from the digits"""
    nb = 0
    size = len(digits)
    for i in range(size):
        nb *= 10
        # +1 : skip 0
        nb += (size-digits[i])
    return nb

def is_prime(number, max_factor):
    # print(number, digits)
    if number < 3:
        return False
    for i in range(2, max_factor+1):
        if number%i == 0:
            return False
    return True

def solve_problem_generate_base(limit_digits, limit):

    max_factor = math.floor(math.sqrt(10**limit_digits))

    digits = []
    temp = []
    get_permutation_start(digits, temp, limit_digits)
    number = get_number(digits)
    if is_prime(number, max_factor) and number < limit:
        return number

    while get_permutation_next(digits, temp, limit_digits):
        number = get_number(digits)
        if is_prime(number, max_factor) and number < limit:
            return number

    return -1

def solve_problem_generate(limit_digits, limit):
    ret = -1
    while limit_digits > 0 and ret == -1:
        ret = solve_problem_generate_base(limit_digits, limit)
        limit_digits -= 1
    return ret

# too slow for hackerrank
def solve_problem_generate_reallimit(limit_in):
    limit_digits = number_of_digits(limit_in)
    return solve_problem_generate(limit_digits, limit_in)

def solve_problem_generate_testthem(limit_in):
    '''
        desperate try to pass the hackerrank tests
            just test for small enough numbers (instead of calculating based on the number of digits)
    '''
    no_digits = number_of_digits(limit_in)
    max_factor = math.floor(math.sqrt(limit_in))

    if limit_in > 7000000:
        return solve_problem_generate_reallimit(limit_in)

    i = limit_in
    while i > 100:
        digits = get_digits(i)
        if is_pandigital(digits) and is_prime(i, max_factor):
            return i
        if len(digits) < no_digits:
            no_digits -= 1
            max_factor = math.floor(math.sqrt(i))
        i -= 1

    return -1

def solve_problem_calculate_primes(limit):
    '''
        10**8 is too much for my computer: more than 2G memory
            => generate the numbers and try find a devisor < sqrt

        solve_problem_generate is much faste
    '''
    pandigital = -1

    primes = get_primes(limit)

    for i in range(len(primes)-1, 0, -1):
        prime = primes[i]

        digits = get_digits(prime)
        if is_pandigital(digits):
            # print("pandigital:", prime)
            pandigital = prime
            break

    return pandigital

def solve_problem_reallimit(limit):
    # return solve_problem_calculate_primes(limit)
    return solve_problem_generate_reallimit(limit)

def solve_problem_power10(limit_in):
    limit = 10**limit_in-1
    return solve_problem_generate_reallimit(limit)

def parse_input():
    '''
        https://www.hackerrank.com/contests/projecteuler/challenges/euler032
    '''
    calculated = dict()
    cache = []

    test_cases = int(input().strip())
    for _ in range(test_cases):
        limit = int(input().strip())

        # 10 digits (0 included is too slow)
        if number_of_digits(limit) > 7:
            limit = 10**7

        found = False
        pos = bisect.bisect_left(cache, limit)
        if pos != len(cache):
            after = cache[pos]
            if calculated[after] == -1:
                result = -1
                found = True
            elif pos and calculated[after] == calculated[cache[pos-1]]:
                result = calculated[after]
                found = True

        if found:
            # print("found in cache")
            pass
        else:
            # result = solve_problem_reallimit(limit)
            result = solve_problem_generate_testthem(limit)
        print(result)

        if not found:
            if limit not in calculated:
                calculated[limit] = result
                bisect.insort_left(cache, limit)
            if result != -1:
                if result not in calculated:
                    calculated[result] = result
                    bisect.insort_left(cache, result)
                    # do not delete in the middle
            else:
                pos = bisect.bisect_left(cache, limit)
                del cache[:pos]

        # print(cache)

def problem():
    return solve_problem_power10(9)

def debug_assertions():
    assert is_pandigital([4, 3, 2, 1])
    assert solve_problem_reallimit(100) == -1

    assert solve_problem_calculate_primes(5000) == 4231

def main():
    debug_assertions()

    # parse_input()
    # print(solve_problem_power10(7))
    print(problem())

if __name__ == "__main__":
    main()
