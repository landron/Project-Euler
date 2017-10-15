#!/bin/python3
'''    
    https://projecteuler.net/problem=48
        last 10 digits of 1^1 + 2^2 + ... + 1000^1000
        O(n^2), it actually goes pretty fast
'''

import sys

def add_step(sum, value, reminder):
    sum += value
    sum += reminder
    if sum < 10:
        return (sum, 0)
    else:
        return (sum-10, 1)

def sum_ordered(sum, to_add, limit):

    size_max = len(to_add)
    if 0 != limit and size_max > limit:
        size_max = limit
    if size_max > len(sum):
        sum += [0] * (size_max - len(sum))

    reminder = 0
    for i in range(size_max):
        (sum[i], reminder) = add_step(sum[i], to_add[i], reminder)

    #  keep the reminder if there is space
    if reminder != 0 and (0 == limit or limit > size_max):
        new_size_max = len(sum)
        if new_size_max > limit:
            new_size_max = limit
        for i in range(size_max, new_size_max):
            (sum[i], reminder) = add_step(sum[i], 0, reminder)
            if reminder == 0:
                break
        if reminder != 0 and (0 == limit or limit > new_size_max):
            sum += [reminder]
            reminder = 0

    return (sum, reminder)

# \todo:  do not limit hte size for limit = 0
def prod_to_n(a, m, limit):

    size_max = len(a)
    if 0 != limit and size_max > limit:
        size_max = limit

    assert len(a) >= size_max

    reminder = 0
    for i in range(size_max):
        a[i] *= m 
        a[i] += reminder
        reminder = a[i]//10
        a[i] = a[i]%10

        # print (a, reminder)

    #  keep the reminder if there is space
    if reminder != 0 and (size_max < limit or limit == 0):
        # get digits in the reminder
        digits = []
        while 0 != reminder:
            digits += [reminder%10]
            reminder = reminder//10
        a += digits

    return reminder

def prod_keep_last_n(a, m, n):
    if len(a) >= n:
        prod_to_n(a, m, n)
    else:
        reminder = prod_to_n(a, m, len(a))
        a += [reminder]
    return a

def sum_of_prods_step(sum, step, digits_no):
    next = [1]
    # print(step)
    for _ in range(step):
        prod_keep_last_n(next, step, digits_no)
    # print(step, next)
    sum_ordered(sum, next, digits_no)
    # print(step, next, sum)

def sum_of_prods_all(limit, digits_no):
    sum = [1]
    for i in range(2, limit+1):
        sum_of_prods_step(sum, i, digits_no)
    return sum

def sum_of_prods(limit):
    # 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
    sum = [7, 1, 3, 1, 7, 0, 5, 0, 4, 0]
    for i in range(11, limit+1):
        if 0 == i%50:
            print(i)
        sum_of_prods_step(sum, i, 10)
    return sum

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

def problem():
    # 9110846700
    result = sum_of_prods(1000)
    result_str = ""    
    for i in reversed(result):
        result_str += chr(ord('0')+i)
    print(result, result_str)

def main():
    debug_assertions()    
    problem()

if __name__ == "__main__":
    main()
