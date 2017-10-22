#!/bin/python3
'''
    https://projecteuler.net/problem=26
        Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.

        error 1:    no, the length of the repetend is not limited t the number of digits, 10
                    there is always a repetend (that can be 0/9 for 1/8 by exemple) because these are rational numbers ;)
        https://en.wikipedia.org/wiki/Repeating_decimal
            Totient rule, https://en.wikipedia.org/wiki/Full_reptend_prime

    https://www.hackerrank.com/contests/projecteuler/challenges/euler026
         Score: 100.00 (solve_problem_3)

    pylint 1.5.5
        Your code has been rated at 7.86/10.
'''

import math

####################################################################################

def get_primes(limit):
    # not rounded since we skip 1 & 2
    primes = [i*2+3 for i in range(limit//2-1)]
    limit_of_sieve = 1+math.floor(math.sqrt(limit))
    for i in range(3, limit_of_sieve, 2):
        if primes[i//2-1]:
            for j in range(i*i, limit, 2*i):
                primes[j//2-1] = 0
    return [2]+[i for i in primes if i != 0]

def no_digits(number, base=10):
    """get the number of the digits of the given number in the given base"""
    digits = 0
    while number >= 1:
        number //= base
        digits += 1
    return digits

####################################################################################

def get_repetend_length(big_10, number):
    assert big_10 > number

    reminders = set()

    current = big_10%number
    while current != 0 and current not in reminders:
        reminders.add(current)
        current = (current*10)%number

    length = len(reminders) if current != 0 else 0
    # print(number, length)
    return length

# Score: 66.67
def solve_problem_1(limit):
    maxi = lambda: None
    maxi.val = 2
    maxi.repeating = 0

    big_10 = 10
    for i in range(2, limit):
        if i == big_10:
            big_10 *= 10
        if big_10%i == 0:
            continue

        repetend_len = get_repetend_length(big_10, i)
        if repetend_len > maxi.repeating:
            maxi.repeating = repetend_len
            maxi.val = i
            # print(maxi.val, maxi.repeating)

    return (maxi.val, maxi.repeating)

# a little risky, as not these numbers are primes
# Score: 66.67 (3/4)
def solve_problem_2(limit):
    maxi = lambda: None
    maxi.val = 2
    maxi.repeating = 0

    primes = get_primes(limit)

    big_10 = 10
    for i in primes:
        if i > big_10:
            big_10 *= 10
        if big_10%i == 0:
            continue

        repetend_len = get_repetend_length(big_10, i)
        if repetend_len > maxi.repeating:
            maxi.repeating = repetend_len
            maxi.val = i
            # print(maxi.val, maxi.repeating)

    return (maxi.val, maxi.repeating)

# stop after the first full reptend prime
# I think the function is correct for limits that are powers of 10
# Score: 100.00
def solve_problem_3(limit):
    maxi = lambda: None
    maxi.val = 2
    maxi.repeating = 0

    primes = get_primes(limit)
    primes = primes[::-1]

    big_10 = 10**no_digits(limit)

    for i in primes:
        if i < big_10/10:
            big_10 /= 10
        if big_10%i == 0:
            continue

        repetend_len = get_repetend_length(big_10, i)
        if repetend_len == i-1:
            maxi.repeating = repetend_len
            maxi.val = i
            break

    return (maxi.val, maxi.repeating)

def solve_problem(limit):
    # return solve_problem_1(limit)
    return solve_problem_1(limit) if limit < 100 else solve_problem_3(limit)

def solve_problem_get_number_only(limit):
    (number, _) = solve_problem(limit)
    return number

# https://www.hackerrank.com/contests/projecteuler/challenges/euler026
def parse_input():
    cases = int(input().strip())
    for _ in range(cases):
        limit = int(input().strip())
        print(solve_problem_get_number_only(limit))

def problem():
    print(solve_problem(1000))

def debug_assertions():
    assert solve_problem(5) == (3, 1)
    assert solve_problem(10) == (7, 6)
    assert solve_problem(100) == (97, 96)

def main():
    debug_assertions()

    # parse_input()
    # problem()

if __name__ == "__main__":
    main()
