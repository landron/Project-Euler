"""
    Problem 12 : Highly divisible triangular number
    http://projecteuler.net/problem=12
        What is the value of the first triangle number to have over five hundred divisors?
    Version: 2015.01.17
    https://projecteuler.net/profile/landron.png

    pylint.bat --version
        No config file found, using default configuration
        pylint 1.4.0,
        astroid 1.3.2, common 0.63.2
        Python 3.4.2 (v3.4.2:ab2c023a9432, Oct  6 2014, 22:15:05) [MSC v.1600 32 bit (Intel)]
    Your code has been rated at 10.00/10

    Knowledge base:
        1. pop "really" removes elements
        2. I had a lot of problems solving this one because I initially wrongly calculated the
        number of divisors for numbers with more of three prime divisors
"""

import itertools
import time
from proj_euler import get_primes

HARD_ASSERT = False

def get_divisor_and_power(item):
    """generate tuple for primes of power 1"""
    return item if isinstance(item, tuple) else (item, 1)

def extend_item(item):
    """the list of divisors for given prime and power"""
    item = get_divisor_and_power(item)
    assert 1 != item[0]
    return [1] + [item[0]**(i+1) for i in range(item[1])]

def combine_same_prime_lists(list1, list2):
    """get all the divisors from two lists based on the same prime"""
    assert 1 == list1[0] and 1 == list2[0]
    assert list1[1] == list2[1]

    # the two lists are based on the same prime
    if HARD_ASSERT:
        for i in range(min(len(list1), len(list2))):
            assert list1[i] == list2[i]
        list_max = list1 if len(list1) > len(list2) else list2
        # print(list_max)
        for i in range(2, len(list_max)):
            # if list_max[i] != list_max[1] * list_max[i-1]:
            #     print(list_max[i], list_max[1], list_max[i-1])
            assert list_max[i] == list_max[1] * list_max[i-1]

    return extend_item((list1[1], len(list1)-1+len(list2)-1))

def combine_divisors_lists(list1, list2):
    """get all the divisors from two lists"""
    assert 1 == list1[0] and 1 == list2[0]
    if list1[1] == list2[1]:
        return combine_same_prime_lists(list1, list2)

    # the two lists are disjoint
    if HARD_ASSERT:
        for i in list1[1:]:
            assert not i in list2
        for i in list2[1:]:
            assert not i in list1

    return [i*j for i in list1 for j in list2]

def combine_divisors_items(item1, item2):
    """get all the divisors from two simple item"""
    list1 = extend_item(item1)
    list2 = extend_item(item2)
    return combine_divisors_lists(list1, list2)

def combine_divisors(item1, item2):
    """get all the divisors from two items or lists"""
    if not isinstance(item1, list):
        item1 = extend_item(item1)
    if not isinstance(item2, list):
        item2 = extend_item(item2)
    return combine_divisors_lists(item1, item2)

def combine_sorted(item1, item2):
    """get all the divisors in a sorted list"""
    return sorted(combine_divisors(item1, item2))

def extend_primes(item):
    """get the divisors from the list of primes"""
    assert isinstance(item, list)
    divisors = extend_item(item[0])
    for prime in item[1:]:
        divisors = combine_divisors(extend_item(prime), divisors)
    # print(divisors)
    return divisors

def extend(item):
    """extend a simple item or a list of primes"""
    if isinstance(item, list):
        return extend_primes(item)
    return extend_item(item)

def combine_primes(item1, item2):
    """get all the divisors from two lists of primes"""
    return combine_divisors(extend(item1), extend(item2))

def combine_primes_sorted(item1, item2):
    """get all the divisors from two lists of primes in a sorted list"""
    return sorted(combine_primes(item1, item2))

def get_power(number, prime):
    """gets the maximal power of the prime that divides the number"""
    i = 1
    for i in itertools.count(1):
        if 0 != number%(prime**i):
            break
    i -= 1
    return (number//(prime**i), i)

def get_prime_divisors(number, primes):
    """get the prime divisors of a given number"""
    assert 1 < number
    assert primes
    divisors = []
    for prime in primes:
        (number, power) = get_power(number, prime)
        if 0 != power:
            divisors.append((prime, power))
        if number == 1:
            break
    assert 1 == number
    return divisors

def get_triangular_divisors(number, primes):
    """get the prime divisors of the resulting triangular number"""
    if 0 == number%2:
        second = number+1
        first = number//2
    else:
        first = number
        second = (number+1)//2
    list1 = get_prime_divisors(first, primes)
    list2 = get_prime_divisors(second, primes)
    # the number are coprimes
    return combine_primes(list1, list2)

def first_triangle_number_base(number_of_divisors):
    """get the first triangular number with the given number of divisors"""

    limit = 100
    primes = get_primes(limit)
    for i in itertools.count(3):
        if i == limit:
            limit *= 10
            primes = get_primes(limit)
        assert i < limit

        # !getting only the length of the list is enough
        divisors = get_triangular_divisors(i, primes)
        if len(divisors) >= number_of_divisors:
            return (len(divisors), i, i*(i+1)//2)

def first_triangle_number(number_of_divisors):
    """get the first triangular number with the given number of divisors"""
    return first_triangle_number_base(number_of_divisors)[2]

def debug_validations_basic():
    """basic functions validations"""
    assert [1, 2, 3, 6] == combine_sorted(2, 3)
    assert [1, 2, 3, 6] == combine_sorted((2, 1), (3, 1))
    assert [1, 2, 3, 6, 9, 18] == combine_sorted((2, 1), (3, 2))
    assert [1, 2, 4, 8, 16] == combine_sorted((2, 3), 2)
    assert [1, 2, 4, 8, 16, 32, 64] == combine_sorted((2, 2), (2, 4))
    assert combine_sorted((2, 4), (2, 2)) == combine_sorted((2, 2), (2, 4))
    assert combine_sorted((2, 5), 2) == combine_sorted((2, 2), (2, 4))
    assert [1, 2, 4, 8, 16, 32, 64] == combine_sorted([1, 2, 4], [1, 2, 4, 8, 16])

    assert [1, 2, 4, 7, 14, 28] == combine_sorted((2, 2), 7)
    assert [1, 2, 4, 7, 14, 28] == combine_primes_sorted((2, 2), 7)
    assert [1, 2, 3, 4, 6, 11, 12, 22, 33, 44, 66, 132] == combine_primes_sorted([(2, 2), 3], 11)
    assert combine_primes_sorted(3, [(2, 2), 11]) == combine_primes_sorted([(2, 2), 3], 11)
    # [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120]
    assert 16 == len(combine_primes_sorted((2, 3), [3, 5]))

    assert [(2, 2), (3, 2)] == get_prime_divisors(36, get_primes(100))
    assert [(2, 4), (3, 2)] == get_prime_divisors(144, get_primes(100))
    assert [(2, 2), (3, 1), (7, 1)] == get_prime_divisors(84, get_primes(100))

def debug_validations_triangular():
    """triangular validations"""
    assert [1, 2, 4, 7, 14, 28] == get_triangular_divisors(7, get_primes(100))
    assert [1, 2, 3, 6, 11, 22, 33, 66] == get_triangular_divisors(11, get_primes(100))
    assert 16 == len(get_triangular_divisors(15, get_primes(100)))

    assert 28 == first_triangle_number(5)
    assert 28 == first_triangle_number(6)
    assert 36 == first_triangle_number(7)
    assert 36 == first_triangle_number(9)
    assert 120 == first_triangle_number(10)
    assert 120 == first_triangle_number(16)
    assert 300 == first_triangle_number(17)
    assert 300 == first_triangle_number(18)
    assert 528 == first_triangle_number(19)
    assert 528 == first_triangle_number(20)
    assert 630 == first_triangle_number(21)
    assert 630 == first_triangle_number(24)
    assert 2016 == first_triangle_number(25)
    assert 2016 == first_triangle_number(36)
    assert 3240 == first_triangle_number(37)
    assert 3240 == first_triangle_number(40)

def debug_validations():
    """all the assertions"""
    debug_validations_basic()
    debug_validations_triangular()

# version 1:  8.49 seconds -> 10.31 seconds
def problem_13():
    """solve the problem, print the needed time"""
    start = time.time()

    # print(len(sorted(get_triangular_divisors(24, get_primes(100)))))
    # (576, 12375, 76576500)
    # print(first_triangle_number_base(500))
    result = first_triangle_number(500)
    print("Result {0} in {1:.2f} seconds".format(result, time.time()-start))


if __name__ == "__main__":
    debug_validations()

    problem_13()
