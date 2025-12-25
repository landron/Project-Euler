"""
http://projecteuler.net/problem=7
  What is the 10 001st prime number?
http://projecteuler.net/problem=10
  Problem 10. Sum all primes below N million

Version: 2023.04.14

TODO:   hackerrank_10
"""

from datetime import datetime
from math import log
import sys
from time import time

from project_euler.proj_euler import get_primes

HARD_VALIDATE = False


def find_primes_number_count(limit, position=1):
    """find the number of prime numbers below the given limit"""
    assert position > 0
    primes = get_primes(limit)
    if position - 1 < len(primes):
        return (len(primes), primes[position - 1])
    return (len(primes), 0)


def find_prime_number2(position):
    """
    Purpose
        find the nth prime number; version 2, in production
    this time we know approximately where to search for

    Performance
    get_primes_limits(limitInf, limitSup) doesn't work as there are more primes in the interval
    [2016-05-01 16:22] Total time: 2.50 seconds / HARD_VALIDATE, both problems
    """
    if position < 6:
        return find_prime_number1(position)

    # Consequence Two: The nth prime is about n (ln n + ln (ln n))
    limit_sup = int(position * (log(position) + log(log(position))))

    result = find_primes_number_count(limit_sup, position)[1]
    assert result != 0
    return result


def find_prime_number1(position):
    """
    Purpose
        find the nth prime number; version 1, deprecated

    [2016-05-01 16:21] Total time: 2.98 seconds / HARD_VALIDATE, both problems
    """
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


def problem_7():
    """
    Purpose
        solve the problem 7, print the needed time
    Performance
        0.5 - 0.6 seconds
    """
    start = time()
    result = find_prime_number(10001)
    assert result == 104743
    print(f"Problem 7 - result {result:d} in {time()-start:.2f} seconds")


def problem_10():
    """
    Purpose
        solve the problem 10, print the needed time

    Performance
        around 1 second, be aware of the validations
    """
    start = time()
    result = find_primes_sum(2000000)
    assert result == 142913828922
    print(f"Problem 10 - result {result:d} in {time()-start:.2f} seconds")


def hackerrank_7():
    """
    https://www.hackerrank.com/contests/projecteuler/challenges/euler007
    Nth prime
    """
    limit = 1000
    primes = get_primes(limit)

    test_cases = int(sys.stdin.readline())
    for _ in range(test_cases):
        position = int(sys.stdin.readline())
        while position > len(primes):
            limit *= 2
            primes = get_primes(limit)
        print(primes[position - 1])


def hackerrank_10():
    """
    https://www.hackerrank.com/contests/projecteuler/challenges/euler010
    sum of the primes below the given limit

    timeout:        6,7
    wrong results:  the rest, except 0 and 4

    Idea: keep a list with all the numbers < limit and their calculated sums
    """
    limit = 1000
    primes = get_primes(limit)
    sums = {}

    test_cases = int(sys.stdin.readline())
    for _ in range(test_cases):
        new_limit = int(sys.stdin.readline())
        sum_of = 0
        last_index = 0
        if new_limit > limit:
            limit = 1 + new_limit
            primes = get_primes(limit)

        # TODO: wrong result
        if 0:  # pylint: disable=using-constant-test
            for key, val in sums.items():
                if last_index < key < new_limit:
                    last_index = val[0]
                    sum_of = val[1]

        # print(sum_of, last_index)
        for i, val in enumerate(primes[last_index:]):
            if val > new_limit:
                last_index = i
                break
            sum_of += val
        sums[new_limit] = (last_index, sum_of)
        print(sum_of)


def main():
    """main"""
    start = time()

    validate_primes_number_count()
    validate_find_primes_sum()

    problem_7()
    # problem_10()

    # for i in range(1,100):
    #     print(find_prime_number(i))

    print(
        f'[{datetime.now().strftime("%Y-%m-%d %H:%M")}] '
        f"Total time: {time()-start:.2f} seconds"
    )


if __name__ == "__main__":
    main()
    # hackerrank_10()
