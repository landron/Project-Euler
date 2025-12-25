"""
Square roots as continued fractions
    https://projecteuler.net/problem=64

Detect cycles is not possible:
    2 = 1; 2
    41 = 6; 2, 2, 12
    55 = 7; 2, 2, 2, 14

"All irrational square roots of integers have a special form for the
period; a symmetrical string, like the empty string (for √2) or 1,2,1
(for √14), followed by the double of the leading integer."
"""

import math


def representation(number):
    """
    continued fraction representation

    cycle detection does not work:
        2 = 1; 2
        41 = 6; 2, 2, 12
        55 = 7; 2, 2, 2, 14
    "Period of continued fraction for square root of n
            (or 0 if n is a square)."
    """
    integer = math.floor(math.sqrt(number))
    if integer**2 == number:
        return [integer]

    def get_next(number, subtrahend, denominator):
        # get integer out of reciprocal of (root-subtrahend)/denominator
        """
        1/(a-b) = (a+b)/(a^2-b^2)

        (root+subtrahend)/new_denominator
        """
        # print(subtrahend, denominator)
        new_denominator = number - subtrahend * subtrahend
        assert new_denominator % denominator == 0
        assert denominator, "only for square numbers"
        new_denominator = new_denominator // denominator
        integer = (math.floor(math.sqrt(number)) + subtrahend) // new_denominator
        return (integer, -(subtrahend - integer * new_denominator), new_denominator)

    subtrahend = integer
    denominator = 1

    rep = []
    # for i in range(20):
    while True:
        next_val, subtrahend, denominator = get_next(number, subtrahend, denominator)
        assert next_val > 0, "0 is impossible ?"
        rep.append(next_val)
        if next_val == 2 * integer:
            break

    # print(number, rep)
    return [integer] + rep


def problem(limit):
    """
    solve PE problem
    """
    odd_period = 0
    for i in range(2, limit + 1):
        rep = representation(i)
        # representation includes the square root besides the period
        if len(rep) % 2 == 0:
            odd_period += 1
    return odd_period


def problem_hackerrank():
    """
    https://www.hackerrank.com/contests/projecteuler/challenges/euler064/problem
    """
    limit = int(input().strip())
    print(problem(limit))


def test_period_series():
    """
    Reference
        "Period of continued fraction for square root of n
            (or 0 if n is a square)."
        https://oeis.org/A003285

        https://planetmath.org/tableofcontinuedfractionsofsqrtnfor1n102
    """
    # fmt: off
    series = [
        0, 1, 2, 0, 1,
        2, 4, 2, 0, 1,
        2, 2, 5, 4, 2,
        0, 1, 2, 6, 2,
        6, 6, 4, 2, 0,
        1, 2, 4, 5, 2,
        8, 4, 4, 4, 2,
        0, 1, 2, 2, 2,
        3, 2, 10, 8, 6,
        12, 4, 2, 0, 1,
        2, 6, 5, 6, 4,
        2, 6, 7, 6, 4,
        11, 4, 2, 0, 1,
        2, 10, 2, 8, 6,
        8, 2, 7, 5, 4,
        12, 6, 4, 4, 2,
        0, 1, 2, 2, 5,
        10, 2, 6, 5, 2,
        8, 8, 10, 16, 4,
        4, 11, 4, 2, 0,
        1, 2, 12,
    ]
    # fmt: on
    for i, val_ref in enumerate(series):
        val = representation(i + 1)
        assert len(val) > 0
        # if len(val) - 1 != val_ref:
        #     print(i+1, val_ref)
        #     print(val)
        assert len(val) - 1 == val_ref


def debug_validations():
    """unit tests"""
    assert representation(2) == [1, 2]
    assert representation(3) == [1, 1, 2]
    assert representation(5) == [2, 4]
    assert representation(6) == [2, 2, 4]
    assert representation(7) == [2, 1, 1, 1, 4]
    assert representation(8) == [2, 1, 4]
    assert representation(10) == [3, 6]
    assert representation(11) == [3, 3, 6]
    assert representation(12) == [3, 2, 6]
    assert representation(13) == [3, 1, 1, 1, 1, 6]
    assert representation(14) == [3, 1, 2, 1, 6]
    assert representation(23) == [4, 1, 3, 1, 8]
    # problems
    assert representation(29) == [5, 2, 1, 1, 2, 10]
    assert representation(41) == [6, 2, 2, 12]
    assert representation(55) == [7, 2, 2, 2, 14]

    assert problem(13) == 4

    test_period_series()


if __name__ == "__main__":
    debug_validations()

    # print(representation(55))
    # print(problem(100))
    # problem_hackerrank()
