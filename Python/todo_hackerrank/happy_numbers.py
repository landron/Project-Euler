#!/usr/bin/env python3
# coding=utf-8
"""
Happy numbers properties:
    n = N digits number
    sum_happy(n) <= N*(9^2) = 81*N
    n >= 10^(N-1) > 81*N for N >= 4

HackerRank: 75/100
todo_hackerrank: 62.5/100
    not the fastest BigInteger implementation
    https://github.com/landron/Project-Euler/tree/master/CPP/happy-numbers

tag_nice
tag_recurrence_relation

flake8, pylint
"""
import time


def sum_of_pow_digits(number):
    """
    separate digit as a variable =>  67.91s
    """
    sum_of = 0
    while number >= 1:
        digit = number % 10
        number //= 10
        sum_of += digit * digit
    assert sum_of
    return sum_of


def get_precalculated_table(digits_no):
    """
    get the precalculated table: all the happy sums should be contain!
    """

    def get_presolved(digits_no):
        """
        n >= 10^(N-1) > 81*N for N >= 4
        """
        return 243 if digits_no < 4 else 81 * digits_no

    limit_presolved = 1 + get_presolved(digits_no)

    solved = [0] * limit_presolved
    solved[1] = 1

    for i in range(2, limit_presolved):
        if solved[i]:
            continue

        number = i
        gen = [i]
        while number not in [1, 89]:
            number = sum_of_pow_digits(number)
            if solved[number]:
                number = solved[number]
                break
            gen.append(number)

        for j in gen:
            solved[j] = number

    return solved


def problem_brute(digits_no):
    """
    10**1:  8
    10**2:  80      (72)
    10**3:  857     (57)
    10**4:  8558    (-12)
    10**5:  85623   (43)
    10**6:  856929  (690)

    10**7:  Result in 73.35 seconds.

    a limited dictionary (1000 by exemple) also gains some speed
        : 3* 81 is enough, apparently
        https://math.stackexchange.com/questions/1261396/square-of-digits-why-does-it-always-contain-1-or-89
    10**7:  Result in 64.71 seconds
            Result in 60.89 seconds

            Result in 48.91 seconds : "perfect" precalculated table
    """

    # pylint: disable=unused-variable
    def get_count_with_limited_dict(digits_no):
        """
        10**6:  Result 856929 in 5.72 seconds
        """
        limit = 10**digits_no

        solved = {1: 1}

        count_89 = 0
        for i in range(2, limit):
            if not i % (10**5):
                print(i)

            if i in solved:
                # print("solved", i, solved[i])
                continue

            gen = [i]
            number = i
            while number not in [1, 89]:
                number = sum_of_pow_digits(number)
                if number in solved:
                    number = solved[number]
                    break
                if number < limit:
                    gen.append(number)

            for j in gen:
                if j < 1000:
                    solved[j] = number
                # print(j)
            if number == 89:
                count_89 += len(gen)

        return count_89

    def get_count_with_list(digits_no):
        """
        10**6:  Result 856929 in 4.88 seconds
        10**7:  Result ... in 48.91 seconds
        """
        solved = get_precalculated_table(digits_no)

        limit = 10**digits_no

        count_89 = 0  # 1 is happy
        for i in range(2, limit):
            if not i % (10**5):
                print(i)

            happy_sum = sum_of_pow_digits(i)
            if solved[happy_sum] != 1:
                count_89 += 1
            else:
                # print(i, happy_sum)
                pass

        return count_89

    # count = get_count_with_limited_dict(digits_no)
    count = get_count_with_list(digits_no)
    return count


def problem_rec(digits_no, trace=False):
    """
    http://echochamber.me/viewtopic.php?t=96670

    Bryan Wolf's wonderful recursive solution:
        calculate the count recursively for each of
            81*digits_no possible sums

    100 digits: 14.64 seconds
    200 digits: 63.73 seconds
    """

    def get_happy_count_rec_pure(digits_no, number):
        assert digits_no >= 0
        if number < 0:
            return 0
        if digits_no == 0:
            return number == 0
        sum_of = 0
        for i in range(10):
            if number - i * i < 0:
                break
            sum_of += get_happy_count_rec_pure(digits_no - 1, number - i * i)
        return sum_of

    def get_happy_count_rec(digits_no, number, table):
        assert digits_no >= 0
        if number < 0:
            return 0
        if number == 0:
            return 1
        if digits_no == 0:
            return 0
        if table[digits_no - 1][number - 1] is not None:
            return table[digits_no - 1][number - 1]

        sum_of = 0
        for i in range(10):
            if number - i * i < 0:
                break
            sum_of += get_happy_count_rec(digits_no - 1, number - i * i, table)
        table[digits_no - 1][number - 1] = sum_of
        return sum_of

    def get_happy_count_with_hash(digits_no, number, table):
        count = get_happy_count_rec(digits_no, number, table)
        assert table[digits_no - 1][number - 1] is not None
        return count

    solved = get_precalculated_table(digits_no)
    precalculated = len(solved)

    if trace and 0:
        for i in range(100):
            count = get_happy_count_rec_pure(2, i)
            if count:
                print(i, count)

    happy = 0
    table = [[None for _ in range(precalculated)] for _ in range(digits_no)]
    for i in range(1, len(solved)):
        # if not i%(10**2):
        #     print(i, happy)

        if solved[i] == 1:
            count = get_happy_count_with_hash(digits_no, i, table)
            happy += count

    return 10**digits_no - happy - 1


def parse_input():
    """
    solve HackerRank problem

    Python 3:   62.50/100, 3 time-outs
    same Python 2, PyPy 2
    PyPy 3:     75.00/100, 2 time-outs
    """
    digits_no = int(input().strip())
    result = problem_rec(digits_no)
    result %= 10**9 + 7
    print(result)


def problem():
    """
    A fast method:
        "Happy Numbers"
        Postby BryanWolf » Wed Oct 31, 2012 8:27 pm UTC
        http://echochamber.me/viewtopic.php?t=96670

    Reference
        https://en.wikipedia.org/wiki/Happy_number
    """
    start = time.time()

    result = problem_rec(10)

    print("Result {0} in {1:.2f} seconds".format(result, time.time() - start))


def tests():
    """
    tests for the current problem

    pass -O to ignore assertions and gain some time:
        py -3 -O ./prob.py
    """
    start = time.time()

    if 0:  # pylint: disable=using-constant-test
        # unit tests - less than 5 seconds (4.61) with the classical solution

        assert problem_brute(1) == 7
        assert problem_brute(2) == 80
        assert problem_brute(3) == 857
        assert problem_brute(4) == 8558
        assert problem_brute(5) == 85623
        assert problem_brute(6) == 856929
    else:
        assert problem_rec(1) == 7
        assert problem_rec(2) == 80
        assert problem_rec(3) == 857
        assert problem_rec(4) == 8558
        assert problem_rec(5) == 85623
        assert problem_rec(6) == 856929

    duration = time.time() - start
    if duration:
        print("Tests in {0:.2f} seconds".format(duration))


def main():
    """main"""
    tests()

    problem()
    # parse_input()


if __name__ == "__main__":
    main()
