"""
https://projecteuler.net/problem=66
Diophantine Equation
x^2 - Dy^2 = 1

https://en.wikipedia.org/wiki/Pell%27s_equation#Example

Other tries:
 * try all integers as x, get divisors and then process D
    hard to process all squares
 * try all integers as D - too much
    61: x = 1_766_319_049
    109: x = 158_070_671_986_249

# continued fraction (also problems 64, 65)
"All square roots are periodic when written as continued fractions"
"""

from fractions import Fraction
import math
import time


def solve_brute(limit):
    """
    Return the solution of the problem.

    200: {61, 109, 149, 151, 157, 166, 181, 193, 199}
        D larger than 25_000_000
    """
    # it will keep all D for each we find a solution
    not_found = set(range(2, limit + 1))
    # add trivial solutions:
    # * x^2 - D*1^1 = 1
    # * there are no solutions in positive integers when D is square
    for i in range(2, 1 + math.floor(math.sqrt(limit))):
        not_found.remove(i * i)
        not_found.remove(i * i - 1)
    # print(not_found)

    d_with_largest_x = (0, 0)
    i = 0
    while not_found:
        i += 1
        to_remove = []
        for _, j in enumerate(not_found):
            term = i * i * j + 1
            x_val = math.isqrt(term)
            if x_val * x_val == term:
                to_remove.append(j)
                if x_val > d_with_largest_x[0]:
                    d_with_largest_x = (j, x_val)
                    # print(f"i={i} max={d_with_largest_x}", flush=True)
        if to_remove:
            not_found.difference_update(to_remove)
            # print(len(not_found), flush=True)
        # if i%100000 == 0 and len(not_found) < 10:
        #     print(i, not_found, flush=True)
    if len(not_found) == 1:
        d_with_largest_x = (not_found.pop(), 0)
    return d_with_largest_x


def continued_fraction_sqrt(number):
    """
    Calculate the continued fraction representation of the square root of a
    number.
    """
    # pylint: disable=invalid-name
    if math.isqrt(number) ** 2 == number:
        return [math.isqrt(number)]  # Perfect square case

    m = 0
    d = 1
    a = math.isqrt(number)
    initial_a = a
    terms = [a]

    for _ in range(1000):  # Arbitrary limit to prevent infinite loop
        m = d * a - m
        d = (number - m**2) // d
        a = (initial_a + m) // d
        terms.append(a)

        # If we detect the periodic sequence, break the loop
        if a == 2 * initial_a:
            return terms
    # fmt: off
    assert False, (
        "Continued fraction did not converge within " +
        f"the limit: {number}"
    )
    # fmt: on
    return terms


def continued_fraction_to_fraction(frac):
    """
    Convert a continued fraction representation to a real fraction.
    """
    result = Fraction(frac[-1])
    for term in reversed(frac[:-1]):
        result = term + 1 / result
    return result


def solve(limit):
    """
    Return the solution of the problem.
    Using https://en.wikipedia.org/wiki/Pell%27s_equation#Example
    """
    d_with_largest_x = (0, 0)
    for i in range(2, limit + 1):
        # there are no solutions in positive integers when D is square
        term = math.isqrt(i)
        if term * term == i:
            continue
        frac = continued_fraction_sqrt(i)
        if len(frac) % 2 == 0:
            frac.extend(frac[1:-1])
        else:
            frac = frac[:-1]
        solution = continued_fraction_to_fraction(frac)
        if solution.numerator > d_with_largest_x[1]:
            d_with_largest_x = (i, solution.numerator)
    return d_with_largest_x


def parse_input():
    """
    read input and solve the problem as defined on HackerRank
    """
    limit = int(input().strip())
    solution = solve(limit)
    print(solution[0])


def problem():
    """
    Solve the problem as formulated on the original site.
    """
    start = time.time()

    result = solve(10000)

    duration = time.time() - start
    if duration >= 1:
        print(f"Result {result} in {duration:.2f} seconds")
    else:
        print(result)


def debug_validations():
    """
    unit tests
    """
    assert solve(7) == (5, 9)
    assert solve(10) == (10, 19)
    assert solve(20) == (13, 649)
    assert solve(100) == (61, 1766319049)

    assert continued_fraction_sqrt(7) == [2, 1, 1, 1, 4]
    assert continued_fraction_sqrt(13) == [3, 1, 1, 1, 1, 6]


if __name__ == "__main__":
    debug_validations()

    # original problem
    problem()

    # harden/generalized HackerRank problem
    # parse_input()
