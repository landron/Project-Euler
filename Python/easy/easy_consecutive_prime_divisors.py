#!/bin/python3
'''
    Distinct primes factors
        "Find the first four consecutive integers to have four distinct
        prime factors each. What is the first of these numbers?"
        14, 15
        644, 645, 646

    HackerRank: easy ?
        Python 3:   76.92
        PyPy3 :     100

        2019.01.25, 20:24 : Score: 53.85 (100), timeouts
        2019.01.25, 20:59 : same score, better primes limit
        2019.01.25, 22:30 : Score: 69.23 (100)
                            generating exclusions
        2019.01.25, 23:11 : 76.92
                            even better exclusions (2M 4 passes in 10s)

        2019.01.25, 00:40 : Done with PyPy3.

    Your code has been rated at 9.82/10 (previous run: 9.82/10, +0.00)
        too many branches/statements

    tag_primes, tag_divisors
'''
import time

DEBUG = True
USE_LIB = False

if USE_LIB:
    from lib.proj_euler import get_primes, get_primes_for_divisors_of,\
        get_prime_divisors
else:
    import math

    def get_primes(limit):
        """minor optimization version of the previous"""
        # not rounded since we skip 1 & 2
        primes = [i*2+3 for i in range(limit//2-1)]
        limit_of_sieve = 1+math.floor(math.sqrt(limit))
        for i in range(3, limit_of_sieve, 2):
            if primes[i//2-1]:
                for j in range(i*i, limit, 2*i):
                    primes[j//2-1] = 0
        return [2]+[i for i in primes if i != 0]

    def __get_power(number, prime):
        """gets the maximal power of the prime that divides the number"""
        if number % prime:
            return (number, 0)
        power = 1
        divisor = prime*prime
        while number % divisor == 0:
            divisor *= prime
            power += 1
        return (number//int(divisor/prime), power)

    def get_prime_divisors(number, primes):
        """get the prime divisors of a given number
                the sqrt(number) is enough for the limit of the primes because
                    we consider the remainder, a last "big" prime number
        """
        assert number > 1
        assert primes
        limit = 1 + math.floor(math.sqrt(number))
        divisors = []
        for prime in primes:
            if limit < prime:
                break
            (number, power) = __get_power(number, prime)
            if power != 0:
                divisors.append((prime, power))
                # if divisors_limit and divisors_limit < len(divisors):
                #     return divisors
            if number == 1:
                break
        if number != 1:
            #   a prime number
            divisors.append((number, 1))
        return divisors

    def get_primes_for_divisors_of(limit):
        """
            Get the list of primes until the greatest possible
            divisor of the given limit.

            Returns the list of these prime numbers.

            ATTENTION: this does not include all the prime numbers smaller
                than the given limit!
        """
        return get_primes(1 + math.floor(math.sqrt(limit)))

###########################################################################


def parse_input():
    '''
        read input and solve the problem as defined on hackerrank

        try to get some speed - 500000, 4:
            1. Needed time: 35.45 seconds.
            2. Needed time: 34.05 seconds.
                using "divisors number limit"

            3. Needed time: 7.04 seconds.
                using exclusion list of primes: 1,2,3

            4. Needed time: 11.94 seconds.
                get_primes corrected
    '''
    limit, consecutives_no = (int(i) for i in input().strip().split())
    # limit, consecutives_no = 2000000, 4

    start = time.time()
    # solution = solve_hk(limit, consecutives_no)
    solve_hk(limit, consecutives_no)

    if DEBUG:
        print("Needed time: {0:.2f} seconds.".format(time.time()-start))


def solve_hk_by_exclusions(limit, distinct_prime_factors):
    '''
        solve the problem as defined on hackerrank
        Find all the solutions.
            by generate some exclusions, then test the remaining numbers
    '''
    limit += 1

    # primes = get_primes_for_divisors_of(limit)
    primes = get_primes(limit)

    def generate_exclusion_list_1(  # pylint: disable=unused-variable
            limit, primes, distinct_prime_factors):
        '''288604 elements, 19s'''
        exclusion = [False] * (1+limit+distinct_prime_factors)
        for i in range(4):
            exclusion[i] = True

        # primes
        for i in primes:
            exclusion[i] = True
        # powers of primes
        for i, val in enumerate(primes):
            to_exclude = val*val
            if to_exclude >= len(exclusion):
                break
            while to_exclude < len(exclusion):
                exclusion[to_exclude] = True
                to_exclude *= val
        # products of primes
        #   directly enumerate(exclusion) is too slow
        if distinct_prime_factors != 2:
            for i, val in enumerate(primes):
                for j in range(i):
                    to_exclude = primes[j] * val
                    if to_exclude >= len(exclusion):
                        break
                    exclusion[to_exclude] = True
        #   way too slow
        if 0 and distinct_prime_factors != 3:
            for i, val in enumerate(primes):
                if not i % 1000:
                    print(i)
                if val*2*3 > len(exclusion):
                    break
                for j in range(i):
                    for k in range(j):
                        to_exclude = primes[k] * primes[j] * val
                        if to_exclude >= len(exclusion):
                            break
                        exclusion[to_exclude] = True
        return exclusion

    def generate_exclusion_list_2(limit, primes, distinct_prime_factors):
        '''improved version of the previous ?
            289604 elements, 19s
            497961 elements, 4s with 3 primes products included
            976076 elements for 2M, 4
        '''
        exclusion = [False] * (1+limit+distinct_prime_factors)
        for i in range(4):
            exclusion[i] = True

        if distinct_prime_factors == 2:
            for i, val in enumerate(primes):
                exclusion[val] = True
                # powers of primes
                to_exclude = val*val
                if to_exclude >= len(exclusion):
                    break
                while to_exclude < len(exclusion):
                    exclusion[to_exclude] = True
                    to_exclude *= val
        elif distinct_prime_factors == 3:
            for i, val in enumerate(primes):
                to_exclude = val
                while to_exclude < len(exclusion):
                    exclusion[to_exclude] = True
                    for j in range(i):
                        to_exclude_2 = primes[j] * to_exclude
                        if to_exclude_2 >= len(exclusion):
                            break
                        exclusion[to_exclude_2] = True
                    to_exclude *= val
        else:
            for i, val in enumerate(primes):
                to_exclude = val
                while to_exclude < len(exclusion):
                    exclusion[to_exclude] = True
                    for j in range(i):
                        to_exclude_2 = primes[j] * to_exclude
                        if to_exclude_2 >= len(exclusion):
                            break
                        exclusion[to_exclude_2] = True
                        limit_3 = j
                        for k in range(limit_3):
                            to_exclude_3 = primes[k] * to_exclude_2
                            if to_exclude_3 >= len(exclusion):
                                break
                            exclusion[to_exclude_3] = True
                    to_exclude *= val
        return exclusion

    def generate_exclusion_list(limit, primes, distinct_prime_factors):
        return generate_exclusion_list_2(limit, primes, distinct_prime_factors)

    exclusion = generate_exclusion_list(limit, primes, distinct_prime_factors)
    if DEBUG:
        excluded = 0
        for _, val in enumerate(exclusion):
            if val:
                excluded += 1
        print("Start: ", excluded)

    def generate_solution(limit, primes, distinct_prime_factors,
                          consecutives_limit, exclusion):
        solution = []

        # for i in range(6, limit):
        i = 6
        while i < limit:
            if exclusion[i]:
                i += 1
                continue

            try_it = True
            for j in range(distinct_prime_factors):
                assert i+j < 1+limit+distinct_prime_factors,\
                       "out of range: {0} and {1}".format(i, j)
                if exclusion[i+j]:
                    i += j
                    try_it = False
            if not try_it:
                continue

            consecutives = 0
            for j in range(consecutives_limit):
                consecutives_len = len(get_prime_divisors(i+j, primes))
                if distinct_prime_factors != consecutives_len:
                    break
                consecutives += 1
            if consecutives_limit == consecutives:
                solution.append(i)
                print(i)
                i += 1
            else:
                i += (consecutives+1)

        return solution

    consecutives_limit = distinct_prime_factors
    return generate_solution(
        limit, primes, distinct_prime_factors, consecutives_limit, exclusion)


def solve_hk_by_generating(limit, distinct_prime_factors):
    '''
        solve the problem as defined on hackerrank
        Find all the solutions by generating them.

        Too slow:
            0.5M 4  Needed time: 41.51 seconds.
    '''
    limit += (1+distinct_prime_factors)

    primes = get_primes(1+limit//distinct_prime_factors)

    def generator(primes, generated, val, primes_index, level):
        if level == 0:
            generated[val] = True
        else:
            for i in range(primes_index):
                to_add = primes[i] * val
                while to_add < len(generated):
                    generator(primes, generated, to_add, i, level-1)
                    to_add *= primes[i]

    generated = [False] * limit
    generator(primes, generated, 1, len(primes), distinct_prime_factors)
    if DEBUG:
        # for i, val in enumerate(generated):
        #     if val:
        #         print(i, end= ' ')
        # print()

        count = 0
        for _, val in enumerate(generated):
            if val:
                count += 1
        print("Start: ", count)

    consecutives_limit = distinct_prime_factors
    consecutives = 0
    for i, val in enumerate(generated):
        if not val:
            consecutives = 0
        else:
            consecutives += 1
            if consecutives_limit == consecutives:
                print(i-consecutives+1)
                consecutives = 0


def solve_hk(limit, distinct_prime_factors):
    '''
        solve the problem as defined on hackerrank
        Find all the solutions.
    '''
    # return solve_hk_by_generating(limit, distinct_prime_factors)
    return solve_hk_by_exclusions(limit, distinct_prime_factors)


def solve():
    '''
        solve problem and return the solution
        This version tries to get the maximum sequence, not all the solutions.

        3 distinct prime factors: 644, 645, 646
            6 series: 6850

        Solution: 5 at 357642 .
            357642 [(2, 1), (3, 3), (37, 1), (179, 1)]
            357643 [(11, 1), (13, 1), (41, 1), (61, 1)]
            357644 [(2, 2), (7, 1), (53, 1), (241, 1)]
            357645 [(3, 1), (5, 1), (113, 1), (211, 1)]
            357646 [(2, 1), (17, 1), (67, 1), (157, 1)]
            Needed time: 89.20 seconds.
    '''
    limit = 1000000
    distinct_prime_factors = 4

    primes = get_primes_for_divisors_of(limit)

    consecutives = 0
    solution = lambda: None  # noqa: E731
    solution.max = 0
    solution.first = 0
    for i in range(644, limit):
        consecutives_len = len(get_prime_divisors(i, primes))
        if distinct_prime_factors == consecutives_len:
            consecutives += 1
        else:
            if consecutives > solution.max:
                solution.max = consecutives
                solution.first = i - consecutives

                if 1:  # pylint: disable=using-constant-test
                    print("Solution:", solution.max, "at", solution.first, ".")
                    for j in range(solution.first,
                                   solution.first+solution.max):
                        print(j, get_prime_divisors(j, primes))

            consecutives = 0

    return solution.first


def problem():
    '''
        solve the problem as defined on original site

        Longest series below 1M with distinct primes factors.
        Solution: 5 at 357642 .
            357642 [(2, 1), (3, 3), (37, 1), (179, 1)]
            357643 [(11, 1), (13, 1), (41, 1), (61, 1)]
            357644 [(2, 2), (7, 1), (53, 1), (241, 1)]
            357645 [(3, 1), (5, 1), (113, 1), (211, 1)]
            357646 [(2, 1), (17, 1), (67, 1), (157, 1)]
        Needed time: 89.20 seconds.
    '''

    start = time.time()
    solution = solve()
    print("Needed time: {0:.2f} seconds.".format(time.time()-start))

    return solution


def debug_assertions():
    '''
        simple unit tests
    '''
    primes_1k = get_primes_for_divisors_of(1000)
    assert len(get_prime_divisors(644, primes_1k)) == 3
    assert len(get_prime_divisors(645, primes_1k)) == 3
    assert len(get_prime_divisors(646, primes_1k)) == 3


def main():
    '''
        main
    '''
    debug_assertions()

    # original problem
    print(problem())

    # harden/generalized problem
    # parse_input()


if __name__ == "__main__":
    main()
