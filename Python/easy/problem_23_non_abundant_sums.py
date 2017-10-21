#!/bin/python3
'''
    tag_divisors

    https://projecteuler.net/problem=23
        "Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers."

    https://www.hackerrank.com/contests/projecteuler/challenges/euler023

    pylint
        Your code has been rated at 8.06/10
'''

import math
import itertools

########################################################################################################################

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


def __get_power(number, prime):
    """gets the maximal power of the prime that divides the number"""
    if number%prime != 0:
        return (number, 0)
    power = 1
    divisor = prime*prime
    while number%divisor == 0:
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
        if number == 1:
            break
    if number != 1:
        #   a prime number
        divisors.append((number, 1))
    return divisors

def proj_euler_get_primes(limit):
    """get the list of primes until the given limit
            returns the list of them
    """
    return get_primes_2(limit)

def get_divisors_as_primes(number, primes=None):
    """get the divisors of a given number as a list of primes and powers"""
    if not primes:
        primes = get_primes(1 + math.floor(math.sqrt(number)))
    return get_prime_divisors(number, primes)

def proj_euler_get_divisors(number, primes=None):
    """get all the divisors of a given number"""
    divisors_and_powers = get_divisors_as_primes(number, primes)

    divisors_expanded = []
    for item in divisors_and_powers:
        divisors_expanded.append([item[0]**(i+1) for i in range(item[1])])

    divisors = []
    for i in range(1+len(divisors_expanded)):
        for item in itertools.combinations(divisors_expanded, i):
            for j in list(itertools.product(*item)):
                prod = 1
                for k in j:
                    prod *= k
                divisors.append(prod)

    divisors = sorted(divisors)
    return divisors

####################################################
# switch between project euler and hackerrank
import proj_euler

def get_primes(limit, use_proj_euler=True):
    return proj_euler.get_primes(limit) if use_proj_euler else get_primes_2(limit)

def get_divisors(number, primes, use_proj_euler=True):
    return proj_euler.get_divisors(number, primes) if use_proj_euler else proj_euler_get_divisors(number, primes)

####################################################

def is_abundant(n, primes, get_divisors_func, use_proj_euler):
    divs = get_divisors_func(n, primes, use_proj_euler)

    assert len(divs) >= 2
    if len(divs) == 2:
        return 0
    # eliminate the number itself
    divs[-1] = 0
    return n < sum(divs)

#
#   \todo:
#       "Every multiple of an abundant number is abundant"
#       "Every multiple (beyond 1) of a perfect number is abundant."
#
def get_abundant(limit, primes, get_divisors_func, use_proj_euler):
    abundant = []
    # 12 is the first one
    for i in range(11, 1+limit):
        if is_abundant(i, primes, get_divisors_func, use_proj_euler):
            abundant.append(i)
    return abundant

def is_sum_of_two_abundant(abundants, number):
    if number < 24:
        return False
    # "Every integer greater than 20161 can be written as the sum of two abundant numbers."
    #   (not the problem supposition)
    if number > 28123:
        return True

    for i in abundants:
        if i > number//2:
            return False
        if number-i in abundants:
            return True

    return False

def get_abundants(use_proj_euler=True):
    primes = get_primes(28123, use_proj_euler)
    abundant_list = get_abundant(28123, primes, get_divisors, use_proj_euler)
    return set(abundant_list)

# https://www.hackerrank.com/contests/projecteuler/challenges/euler023
def parse_input():
    abundants = get_abundants(False)

    test_cases = int(input().strip())
    for _ in range(test_cases):
        next_number = int(input().strip())
        print("YES" if is_sum_of_two_abundant(abundants, next_number) else "NO")

def problem():
    abundants = get_abundants()

    sum_of = 0
    for i in range(28123):
        if not is_sum_of_two_abundant(abundants, i):
            # print(i)
            sum_of += i
    print(sum_of)

def debug_assertions(abundants):
    pass

def main():
    # abundants = get_abundants()
    # debug_assertions(abundants)

    # parse_input()
    # problem()
    pass

if __name__ == "__main__":
    main()
