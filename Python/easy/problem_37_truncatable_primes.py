#! /usr/bin/python3
"""
tag_primes

https://projecteuler.net/problem=37

https://www.hackerrank.com/contests/projecteuler/challenges/euler037
Score: 100.00

"Your code has been rated at 10.00/10"
pylint --version
    No config file found, using default configuration
    pylint 1.8.1,
    astroid 1.6.0
    Python 3.6.4
"""

import math

####################################################


def get_primes(limit):
    """get the list of all primes up to the given limit"""

    # not rounded since we skip 1 & 2
    primes = [i * 2 + 3 for i in range(limit // 2 - 1)]
    limit_of_sieve = 1 + math.floor(math.sqrt(limit))
    for i in range(3, limit_of_sieve, 2):
        if primes[i // 2 - 1]:
            for j in range(i * i, limit, 2 * i):
                primes[j // 2 - 1] = 0
    return [2] + [i for i in primes if i != 0]


####################################################


def is_truncatable(prime, primes):
    """find out if the given prime is truncatable"""

    assert prime in primes
    assert not isinstance(prime, list) or prime <= primes[-1]

    # NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
    if prime < 10:
        return False

    number = prime
    digits = 0
    while number > 0:
        digits += 1
        # print(number)
        if number not in primes:
            return False
        number = number // 10

    number = prime
    digits = 10**digits
    while digits > 1:
        number = number % digits
        # print(number)
        if number not in primes:
            # print(prime)
            return False
        digits //= 10

    return True


def solve_problem(limit):
    """solve the problem up to the given limit"""

    primes_list = get_primes(limit)
    # this really speeds up the process
    primes = set(primes_list)
    # print(len(primes))

    sum_of_truncable_primes = 0
    for i, prime in enumerate(primes):  # pylint: disable=unused-variable
        if is_truncatable(prime, primes):
            # print(prime)
            sum_of_truncable_primes += prime
        # if i%1000 == 0:
        #     print('-', i)

    print(sum_of_truncable_primes)


def parse_input():
    """
    parse hackerrank input
    https://www.hackerrank.com/contests/projecteuler/challenges/euler037
    """
    limit = int(input().strip())
    solve_problem(limit)


def problem():
    """solve the project Euler problem"""

    solve_problem(1000000)


def debug_assertions():
    """unit tests"""

    primes = get_primes(10000)
    # print(primes)

    assert not is_truncatable(13, primes)
    assert not is_truncatable(89, primes)
    assert not is_truncatable(8311, primes)
    assert is_truncatable(3797, primes)


def main():
    """THE main"""
    debug_assertions()

    # parse_input()   # hackerrank
    problem()


if __name__ == "__main__":
    main()
