#!/bin/python3
"""
https://projecteuler.net/problem=48
    last 10 digits of 1^1 + 2^2 + ... + 1000^1000
    O(n^2), it actually goes pretty fast

https://www.hackerrank.com/contests/projecteuler/challenges/euler048
    60/100
    an easy enough optimization would be to use prime factorization and keep the results
    todo_hackerrank

pylint 1.5.5
    Your code has been rated at 8.37/10 (previous run: 8.27/10, +0.10)
"""


def add_step(sum_, value, reminder):
    sum_ += value
    sum_ += reminder
    if sum_ < 10:
        return (sum_, 0)
    else:
        return (sum_ - 10, 1)


def sum_ordered(sum_, to_add, limit):

    size_max = len(to_add)
    if limit != 0 and size_max > limit:
        size_max = limit
    if size_max > len(sum_):
        sum_ += [0] * (size_max - len(sum_))

    reminder = 0
    for i in range(size_max):
        (sum_[i], reminder) = add_step(sum_[i], to_add[i], reminder)

    #  keep the reminder if there is space
    if reminder != 0 and (limit == 0 or limit > size_max):
        new_size_max = len(sum_)
        if new_size_max > limit:
            new_size_max = limit
        for i in range(size_max, new_size_max):
            (sum_[i], reminder) = add_step(sum_[i], 0, reminder)
            if reminder == 0:
                break
        if reminder != 0 and (limit == 0 or limit > new_size_max):
            sum_ += [reminder]
            reminder = 0

    return (sum_, reminder)


def prod_to_n(a, m, limit):

    size_max = len(a)
    if limit != 0 and size_max > limit:
        size_max = limit

    assert len(a) >= size_max

    reminder = 0
    for i in range(size_max):
        a[i] *= m
        a[i] += reminder
        reminder = a[i] // 10
        a[i] = a[i] % 10

        # print (a, reminder)

    #  keep the reminder if there is space
    if reminder != 0 and (size_max < limit or limit == 0):
        # get digits in the reminder
        digits = []
        while reminder != 0:
            digits += [reminder % 10]
            reminder = reminder // 10
        a += digits

    return reminder


def prod_keep_last_n(a, m, n):
    if len(a) >= n:
        prod_to_n(a, m, n)
    else:
        reminder = prod_to_n(a, m, len(a))
        a += [reminder]
    return a


def sum_of_prods_step(sum_, step, digits_no):
    next_term = [1]
    # print(step)
    for _ in range(step):
        prod_keep_last_n(next_term, step, digits_no)
    # print(step, next_term)
    sum_ordered(sum_, next_term, digits_no)
    # print(step, next_term, sum_)


def sum_of_prods_all(limit, digits_no):
    sum_ = [1]
    for i in range(2, limit + 1):
        sum_of_prods_step(sum_, i, digits_no)
    return sum_


# Optimizations:
# - 10 divisible add nothing
# - another: prime factorization and keep already calculated
def sum_of_prods(limit):
    # 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
    sum_ = [7, 1, 3, 1, 7, 0, 5, 0, 4, 0]
    for i in range(11, limit + 1):
        if i % 10 == 0:
            if i % 50 == 0:
                # print(i)
                pass
            continue
        sum_of_prods_step(sum_, i, 10)
    return sum_


def problem_solve(limit_sum):
    result = sum_of_prods(limit_sum)
    result_str = ""
    for i in reversed(result):
        if len(result_str) != 0 or i != 0:
            result_str += chr(ord("0") + i)
    return (result, result_str)


def debug_assertions():
    assert sum_ordered([1], [2], 3) == ([3], 0)
    assert sum_ordered([7], [6], 3) == ([3, 1], 0)
    assert sum_ordered([7], [6], 1) == ([3], 1)

    assert prod_keep_last_n([4], 3, 10) == [2, 1]
    assert prod_keep_last_n([7, 3], 3, 2) == [1, 1]
    assert prod_keep_last_n([9, 4], 7, 3) == [3, 4, 3]
    assert prod_keep_last_n([6, 2], 7, 3) == [2, 8, 1]
    assert prod_keep_last_n([9, 2], 8, 3) == [2, 3, 2]

    assert sum_of_prods(10) == [7, 1, 3, 1, 7, 0, 5, 0, 4, 0]
    assert sum_of_prods(11) == [8, 2, 9, 1, 4, 7, 6, 1, 7, 5]
    assert sum_of_prods_all(3, 0) == [2, 3]
    assert sum_of_prods_all(4, 0) == [8, 8, 2]
    assert sum_of_prods_all(10, 0) == [7, 1, 3, 1, 7, 0, 5, 0, 4, 0, 1]
    assert sum_of_prods_all(10, 10) == [7, 1, 3, 1, 7, 0, 5, 0, 4, 0]


# https://www.hackerrank.com/contests/projecteuler/challenges/euler048
def parse_input():
    limit_sum = int(input().strip())
    (_, result_str) = problem_solve(limit_sum)
    print(result_str)


# 9110846700
def problem():
    (result, result_str) = problem_solve(1000)
    print(result, result_str)


def main():
    debug_assertions()

    # parse_input()
    problem()


if __name__ == "__main__":
    main()
