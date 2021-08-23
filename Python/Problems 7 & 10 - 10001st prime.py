'''
    http://projecteuler.net/problem=7
      What is the 10 001st prime number?
    http://projecteuler.net/problem=10
      Problem 10. Sum all primes below N million

    Version: 2016.05.01

    https://www.hackerrank.com/contests/projecteuler/challenges/euler007
        todo_hackerrank:    75/100

    TODO:
        ? 1. find_primes_number_count, position <= 0
        2. find_primes_number_count is still not fast enough (Sieve of Eratosthenes) for the latest
            test case of http://www.hackerrank.com/contests/projecteuler/challenges/euler007
        See "Is there a known mathematical equation to find the nth prime?", http://goo.gl/er9cas

    pylint --version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 9.87/10 (previous run: 9.73/10, +0.13)
'''

from math import log
from time import time
from datetime import datetime

from project_euler.project_euler import get_primes

HARD_VALIDATE = False

def find_primes_number_count(limit, position=1):
    """find the number of prime numbers below the given limit"""
    assert position > 0
    primes = get_primes(limit)
    if position-1 < len(primes):
        return (len(primes), primes[position-1])
    return (len(primes), 0)

# get_primes_limits(limitInf, limitSup) doesn't work as there are more primes in the interval
# [2016-05-01 16:22] Total time: 2.50 seconds / HARD_VALIDATE, both problems
def find_prime_number2(position):
    """find the nth prime number; version 2, in production
        this time we know approximately where to search for
    """
    if position < 6:
        return find_prime_number1(position)

    # Consequence Two: The nth prime is about n (ln n + ln (ln n))
    limit_sup = int(position * (log(position)+log(log(position))))

    result = find_primes_number_count(limit_sup, position)[1]
    assert result != 0
    return result

# [2016-05-01 16:21] Total time: 2.98 seconds / HARD_VALIDATE, both problems
def find_prime_number1(position):
    """find the nth prime number; version 1, deprecated"""
    limit = 100
    prime = 0
    while prime == 0:
        (_, prime) = find_primes_number_count(limit, position)
        limit *= 10
    return prime

def find_prime_number(position):
    """the function to find the nth prime number"""
    # return find_prime_number1(position)
    return find_prime_number2(position)

def find_primes_sum(limit):
    """calculate the sum of all the prime numbers smaller than the given limit"""
    primes = get_primes(limit)
    # print(primes)
    return sum(primes)

def validate_primes_number_count():
    """module's assertions: count primes"""
    assert find_primes_number_count(100)[0] == 25
    assert find_primes_number_count(1000)[0] == 168
    assert find_primes_number_count(10000)[0] == 1229
    if HARD_VALIDATE:
        assert find_primes_number_count(100000)[0] == 9592
        assert find_primes_number_count(1000000)[0] == 78498
    assert find_prime_number(3) == 5
    assert find_prime_number(6) == 13
    assert find_prime_number(15) == 47
    assert find_prime_number(16) == 53
    assert find_prime_number(20) == 71
    assert find_prime_number(25) == 97
    assert find_prime_number(168) == 997

def validate_find_primes_sum():
    """module's assertions: primes sum"""
    assert find_primes_sum(9) == 17
    assert find_primes_sum(10) == 17
    assert find_primes_sum(11) == 17
    assert find_primes_sum(12) == 28
    assert find_primes_sum(29) == 100
    assert find_primes_sum(30) == 129
    assert find_primes_sum(100) == 1060
    assert find_primes_sum(1000) == 76127
    assert find_primes_sum(10000) == 5736396
    assert find_primes_sum(25000) == 32405717
    if HARD_VALIDATE:
        assert find_primes_sum(2000000) == 142913828922

# 0.5 - 0.6 seconds
def problem_7():
    """solve the problem 7, print the needed time"""
    start = time()
    result = find_prime_number(10001)
    assert  result == 104743
    print("Problem 7 - result {0:d} in {1:.2f} seconds".format(result, time()-start))

# around 1 second, be aware of the validations
def problem_10():
    """solve the problem 10, print the needed time"""
    start = time()
    result = find_primes_sum(2000000)
    assert result == 142913828922
    print("Problem 10 - result {0:d} in {1:.2f} seconds".format(result, time()-start))

def main():
    """the main function, exported like this for external utilisation"""
    start = time()

    validate_primes_number_count()
    validate_find_primes_sum()

    problem_7()
    # problem_10()

    # for i in range(1,100):
    #     print(find_prime_number(i))

    print("[{0}] Total time: {1:.2f} seconds".format(datetime.now().strftime("%Y-%m-%d %H:%M")\
        , time()-start))

if __name__ == "__main__":
    main()
