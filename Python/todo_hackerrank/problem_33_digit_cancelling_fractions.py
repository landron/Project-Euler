#!/bin/python3
"""
tag_digits

https://projecteuler.net/problem=33
    Digit cancelling fractions

https://www.hackerrank.com/contests/projecteuler/challenges/euler033
    !hard
    todo_hackerrank : 16.67
        replace brute force in "solve_problem_base" with numbers generator as in the original answer

    "
    1) The digits removed from the numerator and the denominator should be the
    same and could be in any order. For example, 6483/8644=3/4 where the
    numerator canceled {6,4,8} and the denominator canceled {8,6,4};

    2) Leading zeros are allowed in the post-cancled number. For instance,
    4808/8414=8/14 is a valid fraction for N=4 and K=2.
    "

    2018.04.15 : Score: 16.67   (4 timeouts, 1 wrong answer)

pylint 1.8.1
    "Your code has been rated at 7.84/10."
"""


def are_equals(nom1, denom1, nom2, denom2):
    return nom1 * denom2 == nom2 * denom1


def get_greatest_common_divisor(a, b):
    if a == b:
        return a
    elif a < b:
        return get_greatest_common_divisor(b, a)
    elif b == 0:
        return a
    return get_greatest_common_divisor(b, a % b)


def is_curious(start, end, common, K):
    p_10 = 10**K
    nom = start * p_10 + common
    denominator = common * p_10 + end
    return are_equals(nom, denominator, start, end)


def is_curious_calc(start, end, common):
    digits = 0
    quot = common
    while quot > 1:
        quot /= 10
        digits += 1
    return is_curious(start, end, common, digits)


def get_digits(nb):
    digits = []
    while nb > 0:
        digits.insert(0, nb % 10)
        nb //= 10
    return digits


def eliminate_digits(source, digits, N, seq, see_used):
    """
    the digits must have the same positions, ex: 127/762 is alright
    """
    assert len(source) == N
    assert len(digits) == N

    # be sure to use all the digits
    used = [False] * len(seq)

    nb = 0
    trailing_zeros = False
    for i in range(N):
        skip = False
        for j in range(len(seq)):
            assert seq[j] < N
            if digits[i] == source[seq[j]]:
                if i < seq[j] and digits == source:  # already seen
                    return 0
                # use only once !!
                if used[j]:
                    continue  # break should be fine
                skip = True
                trailing_zeros = source[seq[j]] == 0
                used[j] = True
                break
        if skip:
            continue
        nb *= 10
        nb += digits[i]

    if see_used:
        for i in used:
            if not i:
                return 0

    return nb if not trailing_zeros else 0


def eliminate_digits_same(digits, N, seq):
    return eliminate_digits(digits, digits, N, seq, True)


# Ex. : N = 4 : [0, 1, 2], [0, 1, 3], [0, 2, 3]
def get_next_comb(indexes, N):
    mi = len(indexes) - 1
    assert indexes[mi] < N

    i = mi
    indexes[i] += 1
    while indexes[i] == N:
        indexes[i] = 0
        if i == 0:
            return False
        i -= 1
        indexes[i] += 1

    # the combination is different now, but we also want different ascending values
    j = i + 1
    while j < mi + 1:
        indexes[j] = indexes[j - 1] + 1
        if indexes[j] == N:
            break
        j += 1
    if j < mi + 1:
        # the replace is quite weird in Python
        for k in range(j, mi + 1):
            indexes[k] = N - 1
        return get_next_comb(indexes, N)

    return True


def is_curious_2(nom_in, denom_in, N, K):
    assert K < N
    assert K >= 1

    nom = get_digits(nom_in)
    denom = get_digits(denom_in)

    assert len(nom) == N
    assert len(denom) == N

    seq = []
    for i in range(K):
        seq += [i]

    while True:
        nom_n = eliminate_digits_same(nom, N, seq)
        if nom_n != 0:
            denom_n = eliminate_digits(nom, denom, N, seq, True)
            if denom_n != 0:
                # print(nom, denom, nom_n, denom_n, seq)
                if are_equals(nom_in, denom_in, nom_n, denom_n):
                    return True

        # keep only sequences that point to distinct digits
        distinct_digits = False
        while not distinct_digits:
            if not get_next_comb(seq, N):
                return False
            distinct_digits = True
            for i in range(len(seq) - 1):
                for j in range(i + 1, len(seq)):
                    if nom[seq[i]] == nom[seq[j]]:
                        distinct_digits = False
                        break
        # if not get_next_comb(seq, N):
        #     return False

    # to avoid warning: never here
    return False


def solve_problem_base(N, K):
    """
    N = total number of digits, K = number of digits to eliminate
    brute force

        not good enough for 4 digits
    """
    nominator = []
    denominator = []

    cnt = 0

    for i in range(10 ** (N - 1), 10**N):
        for j in range(i + 1, 10**N):
            cnt += 1
            if cnt == 1000:
                # print("Evaluating:",i,j)
                pass
            if is_curious_2(i, j, N, K):
                print("curious: {0}/{1}".format(i, j))
                nominator += [i]
                denominator += [j]

                # count it only once
                break

    # print(nominator, denominator)
    return (nominator, denominator)


# https://projecteuler.net/problem=33 only
def solve_problem_original_base():
    nominator = []
    denominator = []

    for i in range(10, 100):
        d1 = i // 10
        d2 = i % 10
        for j in range(1, 10):
            if d1 == d2 == j:
                continue
            if is_curious(d1, d2, j, 1):
                # print("curious: {0}{1}/{1}{2}".format(d1, j, d2))
                nominator.append(d1 * 10 + j)
                denominator.append(j * 10 + d2)

    # print(nominator, denominator)
    return (nominator, denominator)


# https://projecteuler.net/problem=33 only
def solve_problem_original():
    (nominator, denominator) = solve_problem_original_base()

    nom = 1
    for i in nominator:
        nom *= i
    denom = 1
    for i in denominator:
        denom *= i

    gcd = get_greatest_common_divisor(nom, denom)
    return denom // gcd


# https://www.hackerrank.com/contests/projecteuler/challenges/euler033
def solve_problem(N, K):
    (nominator, denominator) = solve_problem_base(N, K)

    nom = 0
    for i in nominator:
        nom += i
    denom = 0
    for i in denominator:
        denom += i

    return (nom, denom)


# https://www.hackerrank.com/contests/projecteuler/challenges/euler033
def parse_input():
    (N, K) = (int(i) for i in input().strip().split(" "))
    (sum_nominators, sum_denominators) = solve_problem(N, K)
    print(sum_nominators, sum_denominators)


def problem():
    return solve_problem_original()


def debug_get_comb(initial, N):
    a = initial[:]
    b = [list(a)]
    while get_next_comb(a, N):
        b += [list(a)]
    return b


def debug_assertions():
    assert are_equals(49, 98, 4, 8)
    assert not are_equals(49, 98, 4, 9)

    assert is_curious_calc(1, 4, 6)
    assert is_curious_calc(1, 5, 9)
    assert is_curious_calc(2, 5, 6)
    assert is_curious_calc(4, 8, 9)

    assert get_greatest_common_divisor(42, 28) == 14
    assert get_greatest_common_divisor(42, 56) == 14
    assert get_greatest_common_divisor(54, 24) == 6

    assert eliminate_digits_same([1, 2, 3, 4], 4, [1, 2]) == 14
    assert eliminate_digits_same([1, 2, 1, 2], 4, [0, 1]) != 0
    assert eliminate_digits_same([1, 2, 1, 2], 4, [0, 1]) == 12
    assert eliminate_digits_same([1, 2, 1, 3], 4, [1, 2]) == 0
    assert eliminate_digits_same([1, 2, 1, 3], 4, [0, 3]) != 2
    assert eliminate_digits_same([1, 2, 1, 3], 4, [0, 3]) == 21
    assert eliminate_digits([1, 6], [6, 4], 2, [1], False) == 4
    assert eliminate_digits([1, 6], [7, 4], 2, [1], False) == 74

    assert get_digits(12252) == [1, 2, 2, 5, 2]

    assert debug_get_comb([0, 1, 2], 4) == [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    assert debug_get_comb([0, 1], 4) == [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]

    # after reading the discussions forum
    assert is_curious_2(6483, 8644, 4, 3)
    # zeros
    assert is_curious_2(4808, 8414, 4, 2)
    assert is_curious_2(3016, 6032, 4, 2)
    assert is_curious_2(490, 980, 3, 1)
    assert not is_curious_2(490, 980, 3, 2)
    assert not is_curious_2(1306, 6530, 4, 3)
    # positions does not matter
    assert is_curious_2(127, 762, 3, 2)
    # others
    assert is_curious_2(1616, 6464, 4, 1)

    if 0:  # pylint: disable=using-constant-test
        assert solve_problem(2, 1) == (110, 322)
        assert solve_problem(3, 1) == (41518, 81969)
        assert solve_problem(3, 2) == (6299, 13983)


def main():
    debug_assertions()

    # print(problem())
    # parse_input()
    print(solve_problem(3, 2))

    if 0:  # pylint: disable=using-constant-test
        print(solve_problem(4, 1))

        # curious: 1045/9405
        # curious: 1267/1629
        # curious: 1324/2317
        # curious: 1594/9564
        # curious: 1603/3206
        # curious: 1623/2164
        # curious: 1687/6748
        # curious: 1837/7348
        print(solve_problem(4, 3))


if __name__ == "__main__":
    main()
