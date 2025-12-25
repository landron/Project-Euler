#!/bin/python3
"""
https://projecteuler.net/problem=32
    Pandigital numbers

https://www.hackerrank.com/contests/projecteuler/challenges/euler032
    Score: 100.00

pylint 1.8.1
    Your code has been rated at 9.08/10.
"""

import math
import itertools

####################################################
# proj_euler.py


def get_primes(limit):
    """minor optimization version of the previous"""
    # not rounded since we skip 1 & 2
    primes = [i * 2 + 3 for i in range(limit // 2 - 1)]
    limit_of_sieve = 1 + math.floor(math.sqrt(limit))
    for i in range(3, limit_of_sieve, 2):
        if primes[i // 2 - 1]:
            for j in range(i * i, limit, 2 * i):
                primes[j // 2 - 1] = 0
    return [2] + [i for i in primes if i != 0]


def __get_power(number, prime):
    """gets the maximal power of the prime that divides the number"""
    if number % prime != 0:
        return (number, 0)
    power = 1
    divisor = prime * prime
    while number % divisor == 0:
        divisor *= prime
        power += 1
    return (number // int(divisor / prime), power)


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
        if number == 1:
            break
    if number != 1:
        #   a prime number
        divisors.append((number, 1))
    return divisors


def get_divisors_as_primes(number, primes=None):
    """get the divisors of a given number as a list of primes and powers"""
    if not primes:
        primes = get_primes(1 + math.floor(math.sqrt(number)))
    return get_prime_divisors(number, primes)


def get_divisors(number, primes=None):
    """get all the divisors of a given number"""
    divisors_and_powers = get_divisors_as_primes(number, primes)

    divisors_expanded = []
    for item in divisors_and_powers:
        divisors_expanded.append([item[0] ** (i + 1) for i in range(item[1])])

    divisors = []
    for i in range(1 + len(divisors_expanded)):
        for item in itertools.combinations(divisors_expanded, i):
            for j in list(itertools.product(*item)):
                prod = 1
                for k in j:
                    prod *= k
                divisors.append(prod)

    divisors = sorted(divisors)
    return divisors


####################################################


def get_digits(number):
    digits = []
    while number > 0:
        digits.append(number % 10)
        number //= 10
    return digits


def are_distinct(digits):
    for i in range(len(digits) - 1):
        for j in range(i + 1, len(digits)):
            if digits[i] == digits[j]:
                return False
    return True


def is_pandigital(number_digits, mul, div, N):
    mul_digits = get_digits(mul)
    div_digits = get_digits(div)

    # print("107", number_digits, mul_digits, div_digits,
    #       (len(number_digits) + len(mul_digits) + len(div_digits)) == N)
    # print("108", number_digits, mul, div)

    if len(number_digits) + len(mul_digits) + len(div_digits) != N:
        return False

    # print("113", number_digits, mul, div)

    arr = [False] * 10
    for i in number_digits:
        assert not arr[i]
        arr[i] = True
    for i in mul_digits:
        if arr[i]:
            return False
        arr[i] = True
    for i in div_digits:
        if arr[i]:
            return False
        arr[i] = True

    # 0 took a righteous position :(
    if arr[0]:
        return False
    for i in range(1, N + 1):
        if not arr[i]:
            return False

    return True


def solve_problem(N):
    """
    MAX:    10000 is enough : [4396, 5346, 5796, 6952, 7254, 7632, 7852]
        (altough I calculated a maximum of 100000)
    """
    MAX = 10000
    MIN = 1000 if N == 9 else 10

    pandigital = []

    primes = get_primes(math.floor(math.sqrt(MAX)))
    for i in range(MIN, MAX):
        divisors = get_divisors(i, primes)
        if len(divisors) == 2:
            continue

        digits = get_digits(i)
        if not are_distinct(digits):
            continue

        mul = i
        for div in divisors:
            if div == mul:
                break
            if div == 1:
                continue
            mul = i // div

            if is_pandigital(digits, mul, div, N):
                # print("pandigital:", i, div, mul)
                pandigital += [i]
                break
            if div == mul:
                break

    # print(pandigital)
    sum_ = 0
    for i in pandigital:
        sum_ += i
    return sum_


def parse_input():
    """
    https://www.hackerrank.com/contests/projecteuler/challenges/euler032
    """
    N = int(input().strip())
    result = solve_problem(N)
    print(result)


def problem():
    return solve_problem(9)


def debug_assertions():
    assert is_pandigital([2, 1], 4, 3, 4)
    assert is_pandigital([3, 7, 1, 2], 58, 64, 8)


def main():
    debug_assertions()

    # parse_input()
    # print(solve_problem(8))
    print(problem())


if __name__ == "__main__":
    main()
