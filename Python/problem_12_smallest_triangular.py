"""
Problem 12 : Highly divisible triangular number
http://projecteuler.net/problem=12
    What is the value of the first triangle number to have over five hundred divisors?
Version: 2016.01.2
http://projecteuler.net/profile/landron.png

pylint --version
    No config file found, using default configuration
    pylint 1.5.2,
    astroid 1.4.3
    Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
Your code has been rated at 10.00/10

Knowledge base:
    1. pop "really" removes elements
    2. I had a lot of problems solving this one because I initially wrongly calculated the
    number of divisors for numbers with more of three prime divisors

Optimizations:
    1. calculate only once the prime divisors for each n in the (n,n+1) sequences
    2. don't really get the divisors (formula from the site: 012_overview.pdf)
        D(N) = (a1+1) * (a2+1) * (a3+1) * ...
        an being the exponents of the distinct prime numbers which are factors of N

        for coprime numbers:
        D(t) = D(n/2)(D(n+1) if n is even
        or D(t) = D(n)(D((n+1)/2) if (n+1) is even
    3. for a number, the last possible prime divisor is sqrt
        (except if it is a prime!)
    4. since we know the result: start with the primes until 13000
"""

# import math
import itertools
from time import time
from project_euler.proj_euler import get_primes, get_prime_divisors

HARD_ASSERT = False


def get_divisor_and_power(item):
    """generate tuple for primes of power 1"""
    return item if isinstance(item, tuple) else (item, 1)


def extend_item(item):
    """the list of divisors for given prime and power"""
    item = get_divisor_and_power(item)
    assert item[0] != 1
    return [1] + [item[0] ** (i + 1) for i in range(item[1])]


def combine_same_prime_lists(list1, list2):
    """get all the divisors from two lists based on the same prime"""
    assert list1[0] == 1 and list2[0] == 1
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
            assert list_max[i] == list_max[1] * list_max[i - 1]

    return extend_item((list1[1], len(list1) - 1 + len(list2) - 1))


def combine_divisors_lists(list1, list2):
    """get all the divisors from two lists"""
    assert list1[0] == 1 and list2[0] == 1
    if list1[1] == list2[1]:
        return combine_same_prime_lists(list1, list2)

    # the two lists are disjoint
    if HARD_ASSERT:
        for i in list1[1:]:
            assert i not in list2
        for i in list2[1:]:
            assert i not in list1

    return [i * j for i in list1 for j in list2]


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


# def get_power(number, prime):
#     """gets the maximal power of the prime that divides the number"""
#     i = 1
#     for i in itertools.count(1):
#         if 0 != number%(prime**i):
#             break
#     i -= 1
#     return (number//(prime**i), i)

# def get_prime_divisors(number, primes):
#     """get the prime divisors of a given number"""
#     assert 1 < number
#     assert primes
#     limit = 1 + math.floor(math.sqrt(number))
#     divisors = []
#     for prime in primes:
#         if limit < prime:
#             break
#         (number, power) = get_power(number, prime)
#         if 0 != power:
#             divisors.append((prime, power))
#         if number == 1:
#             break
#     if 1 != number:
#         #   a prime number
#         divisors.append(number)
#     return divisors


def divide_by_2(primes):
    """divide a list of primes by 2"""
    assert primes[0][0] == 2
    if primes[0][1] == 1:
        return primes[1:]
    return [(2, primes[0][1] - 1)] + primes[1:]


def divisors_number(primes):
    """get the number of divisors from a list of primes"""
    divisors = 1
    for prime in primes:
        divisors *= 1 + get_divisor_and_power(prime)[1]
    return divisors


def get_triangular_divisors(number, previous, primes):
    """get the divisors of the resulting triangular number knowing the previous list
    the numbers are coprime => we can safely combine the lists
    """
    if number % 2 == 0:
        second = get_prime_divisors(number + 1, primes)
        divisors = combine_primes(divide_by_2(previous), second)
    else:
        second = get_prime_divisors(number + 1, primes)
        divisors = combine_primes(previous, divide_by_2(second))
    return (second, divisors)


def get_triangular_divisors_number(number, previous, primes):
    """like the previous, but only the number of divisors"""
    if number % 2 == 0:
        second = get_prime_divisors(number + 1, primes)
        divisors = divisors_number(divide_by_2(previous)) * divisors_number(second)
    else:
        second = get_prime_divisors(number + 1, primes)
        divisors = divisors_number(previous) * divisors_number(divide_by_2(second))
    return (second, divisors)


def first_triangle_number_base(number_of_divisors):
    """get the first triangular number with the given number of divisors"""
    limit = 13000  # 100
    primes = get_primes(limit)
    # 3 because get_prime_divisors wants > 1 (2/2 = 1)
    previous = get_prime_divisors(3, primes)
    for i in itertools.count(3):
        if i == limit:
            limit *= 10
            primes = get_primes(limit)
        assert i < limit

        # !getting only the length of the list is enough
        (previous, divisors) = get_triangular_divisors_number(i, previous, primes)
        if divisors >= number_of_divisors:
            return (divisors, i, i * (i + 1) // 2)
    return (0, 0, 0)


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
    assert divisors_number([(2, 2), 7]) == 6
    assert [1, 2, 3, 4, 6, 11, 12, 22, 33, 44, 66, 132] == combine_primes_sorted(
        [(2, 2), 3], 11
    )
    assert divisors_number([(2, 2), 3, 11]) == 12
    assert combine_primes_sorted(3, [(2, 2), 11]) == combine_primes_sorted(
        [(2, 2), 3], 11
    )
    # [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120]
    assert len(combine_primes_sorted((2, 3), [3, 5])) == 16
    assert divisors_number([(2, 3), 3, 5]) == 16

    assert [(2, 2), (3, 2)] == get_prime_divisors(36, get_primes(100))
    assert [(2, 4), (3, 2)] == get_prime_divisors(144, get_primes(100))
    assert [(2, 2), (3, 1), (7, 1)] == get_prime_divisors(84, get_primes(100))


def debug_get_triangular_divisors(number, primes):
    """get_triangular_divisors version without the previous list parameter"""
    assert number > 4
    previous = get_prime_divisors(number, primes)
    return get_triangular_divisors(number, previous, primes)[1]


def debug_validations_triangular():
    """triangular validations"""
    assert [1, 2, 4, 7, 14, 28] == debug_get_triangular_divisors(7, get_primes(100))
    assert [1, 2, 3, 6, 11, 22, 33, 66] == debug_get_triangular_divisors(
        11, get_primes(100)
    )
    assert len(debug_get_triangular_divisors(15, get_primes(100))) == 16

    assert first_triangle_number(5) == 28
    assert first_triangle_number(6) == 28
    assert first_triangle_number(7) == 36
    assert first_triangle_number(9) == 36
    assert first_triangle_number(10) == 120
    assert first_triangle_number(16) == 120
    assert first_triangle_number(17) == 300
    assert first_triangle_number(18) == 300
    assert first_triangle_number(19) == 528
    assert first_triangle_number(20) == 528
    assert first_triangle_number(21) == 630
    assert first_triangle_number(24) == 630
    assert first_triangle_number(25) == 2016
    assert first_triangle_number(36) == 2016
    assert first_triangle_number(37) == 3240
    assert first_triangle_number(40) == 3240


def debug_validations():
    """all the assertions"""
    debug_validations_basic()
    debug_validations_triangular()


# version 1:  8.49 seconds -> 10.31 seconds
# version 2:  4.64 seconds -> 4.72 seconds
#   optimization 1: calculate the prime divisors only once for each divisor
# version 3:  3.95 seconds -> 4.64 seconds
#   optimization 2: don't generate the divisors, only calculate their number
# version 4:  0.59 seconds -> 0.74 seconds
#   optimization 3: limit the maximum prime divisor
# version 5:  0.57 -> 0.66
#   optimization 4: limit of primes = 13000
def problem_12():
    """solve the problem, print the needed time"""
    start = time()

    # print(len(sorted(get_triangular_divisors(24, get_primes(100)))))
    # (576, 12375, 76576500)
    result = first_triangle_number_base(500)
    # print(result)
    assert result[2] == 76576500
    print(f"Result {result[2]} in {time() - start:.2f} seconds")


if __name__ == "__main__":
    debug_validations()

    problem_12()
