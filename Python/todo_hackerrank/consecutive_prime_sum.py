#!/bin/python3
'''
    Warning: avoid direct connection to the project Euler problem number

    Consecutive prime sum

    hackerrank: Hard
        50/100 : Runtimes errors
                 solve_with_primes_1

        60/100 : 1,7,8,9 "Terminated due to timeout"
                 solve_with_primes_2

        Next:
            - AKS primality test (Agrawal–Kayal–Saxena primality test)
            - Miller-Rabin test

    tag_primes
    tag_is_prime
    todo_hackerrank

    Reference
        Further reading
        https://stackoverflow.com/questions/1801391/what-is-the-best-algorithm-for-checking-if-a-number-is-prime
'''
import bisect
import math
import time

PROJ_EULER = True

if PROJ_EULER:
    from project_euler.proj_euler import get_primes, isprime
else:
    def get_primes_2(limit):
        """minor optimization version of the previous"""
        # not rounded since we skip 1 & 2
        primes = [i*2+3 for i in range(limit//2-1)]
        limit_of_sieve = 1+math.floor(math.sqrt(limit))
        for i in range(3, limit_of_sieve, 2):
            if primes[i//2-1]:
                for j in range(i*i, limit, 2*i):
                    primes[j//2-1] = 0
        return [2]+[i for i in primes if i != 0]

    def get_primes(limit):
        """get the list of primes until the given limit
                returns the list of them
        """
        return get_primes_2(limit)

    def isprime(n):  # pylint: disable=invalid-name
        """Returns True if n is prime.

            Reference
                https://stackoverflow.com/questions/1801391/what-is-the-best-algorithm-for-checking-if-a-number-is-prime
        """
        if n == 2:
            return True
        if n == 3:
            return True
        if n % 2 == 0:
            return False
        if n % 3 == 0:
            return False

        i = 5
        w = 2  # pylint: disable=invalid-name

        while i * i <= n:
            if n % i == 0:
                return False

            i += w
            w = 6 - w  # pylint: disable=invalid-name

        return True

###########################################################################


def solution_brute(debug=False):
    '''
        https://projecteuler.net/problem=50
        "The longest sum of consecutive primes below one-thousand that
        adds to a prime, contains 21 terms, and is equal to 953."

        - get_primes(limit/22)
        Lucky solution for 132 terms: 44683.
        Needed time: 26.79 seconds.

        - get_primes(limit)
        Lucky solution for 536 terms: 958577.
        Solution for 543 terms: 997651.
        Needed time: 170.47 seconds.

        opt: get the "luckiest" solution as a start
    '''
    limit = 1000000
    primes = get_primes(limit)
    # no_terms = 22
    no_terms = 131

    solution = 953

    def get_sum(primes, no_terms, index_start):
        current_sum = 0
        for i in range(no_terms):
            current_sum += primes[index_start+i]
        return current_sum

    while True:
        current_sum = get_sum(primes, no_terms, 0)
        if current_sum > limit:
            break

        if current_sum in primes:
            if debug:
                print("Lucky solution for {0} terms: {1}.".
                      format(no_terms, current_sum))
            solution = current_sum
        else:
            found = False
            for i in range(len(primes)-no_terms):
                current_sum -= primes[i]
                current_sum += primes[i+no_terms]

                if current_sum > limit:
                    break

                if current_sum in primes:
                    if debug:
                        print("Solution for {0} terms: {1}.".
                              format(no_terms, current_sum))
                    solution = current_sum
                    found = True
                    break
            if debug and not found and no_terms % 10 == 0:
                # print("No solution for {0} terms.".format(no_terms))
                pass

        no_terms += 1

    return solution


def get_primes_limited(limit):
    '''
        get the list of primes, but with a common sense upper limit
    '''
    limit_gen = limit if limit < 1000000 else 1000000
    return get_primes(limit_gen+1)


def solve_with_primes_func(primes, limit, debug, test_primality):
    '''
        optimization: get the "luckiest" solution as a start

        Possible optimizations:
        - cache primes set: done
        - cache sums
        - try to decompose numbers
    '''
    if len(primes) == 1:
        return 2, 1, 2

    solution = lambda: None  # noqa: E731
    solution.sum = 2
    solution.no_terms = 1
    solution.first = 2

    no_terms = 1

    def get_sum(primes, no_terms, index_start):
        current_sum = 0
        for i in range(no_terms):
            current_sum += primes[index_start+i]
        return current_sum

    def get_best_solution_starting_with_2(limit, primes, solution):
        no_terms = 1

        current_sum = get_sum(primes, no_terms, 0)
        no_terms_from_2 = 1

        while current_sum <= limit:
            if test_primality(primes, current_sum):
                if debug:
                    print("Lucky solution for {0} terms: {1}.".
                          format(no_terms_from_2, current_sum))
                no_terms = no_terms_from_2
                solution.sum = current_sum
                solution.no_terms = no_terms
                solution.first = 2

            current_sum += primes[no_terms_from_2]
            no_terms_from_2 += 1

        return no_terms

    no_terms = get_best_solution_starting_with_2(limit, primes, solution)

    while True:
        current_sum = get_sum(primes, no_terms, 0)
        if current_sum > limit:
            # if debug:
            #     print("Limit break for {0} terms.".format(no_terms))
            break

        if test_primality(primes, current_sum):
            if debug:
                print("Lucky solution for {0} terms: {1}.".
                      format(no_terms, current_sum))
            solution.sum = current_sum
            solution.no_terms = no_terms
            solution.first = 2
        else:
            for i in range(len(primes)-no_terms):
                current_sum -= primes[i]
                current_sum += primes[i+no_terms]

                if current_sum > limit:
                    break

                if test_primality(primes, current_sum):
                    if debug:
                        print("Solution for {0} terms: {1}.".
                              format(no_terms, current_sum))
                    solution.sum = current_sum
                    solution.no_terms = no_terms
                    solution.first = primes[i+1]
                    break

        no_terms += 1

    return solution.sum, solution.no_terms, solution.first


def solve_with_primes_1(primes, limit, debug):
    '''
        test primality using a large primes list

        10^7:  (9951191, 1587)
        10^8:  too much time in get_primes

        Hackerrank: 50/100
            Runtimes errors
    '''

    def search(alist, item):
        '''
            Locate the leftmost value exactly equal to item
            https://stackoverflow.com/questions/38346013/binary-search-in-a-python-list

            about 3 times faster than "item in alist"
        '''
        found = bisect.bisect_left(alist, item)
        return found != len(alist) and alist[found] == item

    def is_prime(primes, item):
        return search(primes, item)

    return solve_with_primes_func(primes, limit, debug, is_prime)


def solve_with_primes_2(primes, limit, debug):
    '''
        solve_with_primes_1 BUT test primality with is_prime function
            (to limit larger than 10^5 primes lists generations)

        works until 10^9
    '''
    def is_prime(primes, item):  # pylint: disable=unused-argument
        return isprime(item)
    return solve_with_primes_func(primes, limit, debug, is_prime)


def parse_input():
    '''
        solve the problem as defined on hackerrank
    '''
    no_tests = int(input().strip())
    tests = []
    max_limit = 0
    for _ in range(no_tests):
        limit = int(input().strip())
        if max_limit < limit:
            max_limit = limit
        tests.append(limit)

    primes = get_primes_limited(max_limit)

    for test in tests:
        solution = solve_with_primes_2(primes, test, False)
        print(solution[0], solution[1])


def solve(limit, debug=False):
    '''
        optimized solution for Hackerrank
            (solve_with_primes_1 is enough for project Euler,
            without any optimization)
    '''
    if 0:  # pylint: disable=using-constant-test
        primes = get_primes(limit+1)
        return solve_with_primes_1(primes, limit, debug)

    primes = get_primes_limited(limit)
    return solve_with_primes_2(primes, limit, debug)


def problem():
    '''
        solve the problem as defined on project Euler site

        solve_with_primes_2
            Needed time: 0.16 seconds.
            (997651, 543, 7)

            - function as parameter
            Needed time: 0.67 seconds.
            (997651, 543, 7)
    '''

    start = time.time()
    solution = solve(1000000, True)
    print("Needed time: {0:.2f} seconds.".format(time.time()-start))

    return solution


def test_range():
    '''
        test optimizations on a range: 10^4

        biggest first term: (21407, 85, 31)

        10000 limit
        start :             Total time: 90.11 seconds.
        binary search:      Total time: 30.55 seconds.
        primes list cache:  Total time: 13.08 seconds.

        solve_with_primes_2: roughly the same time
    '''

    start = time.time()

    limit = 10000
    primes = get_primes(limit)

    last = 0
    for i in range(2, limit):
        solution = solve_with_primes_2(primes, i, False)
        if solution[0] != last:
            print(solution)
            last = solution[0]

    print("Total time: {0:.2f} seconds.".format(time.time()-start))


def debug_assertions():
    '''
        simple unit tests
    '''
    assert solve(2)[0] == 2
    assert solve(3)[0] == 2
    assert solve(10)[0] == 5
    assert solve(100)[0] == 41
    assert solve(1000)[0] == 953


def main():
    '''
        main
    '''
    debug_assertions()

    # project Euler
    print(problem())

    # hackerrank
    # parse_input()

    # performance
    test_range()


if __name__ == "__main__":
    main()
