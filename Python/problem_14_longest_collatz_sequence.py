"""
Problem 14 : Longest Collatz sequence
https://projecteuler.net/problem=14
    Which starting number, under one million, produces the longest chain?

The best solution ... is the brute force one :(
TODO:   can we consider only the even numbers (in the upper half)?

Version: 2016.01.01

pylint --version
    No config file found, using default configuration
    pylint 1.5.2,
    astroid 1.4.3
    Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
Your code has been rated at 10.00/10
"""

import time
from functools import reduce

# HARDONE = [639, 1918, 959, 2878, 1439, 4318, 2159, 6478, 3239, 9718, 4859, 14578, 7289, 21868, \
# 10934, 5467, 16402, 8201, 24604, 12302, 6151, 18454, 9227, 27682, 13841, 41524, 20762, 10381, \
# 31144, 15572, 7786, 3893, 11680, 5840, 2920, 1460, 730, 365, 1096, 548, 274, 137, 412, 206, 103, \
# 310, 155, 466, 233, 700, 350, 175, 526, 263, 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, \
# 334, 167, 502, 251, 754, 377, 1132, 566, 283, 850, 425, 1276, 638, 319, 958, 479, 1438, 719, \
# 2158, 1079, 3238, 1619, 4858, 2429, 7288, 3644, 1822, 911, 2734, 1367, 4102, 2051, 6154, 3077, \
# 9232, 4616, 2308, 1154, 577, 1732, 866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, 92, \
# 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]
HARD_LIMIT = 80
# HARD_LIMIT = 0
HARD_LIMIT_PERCENTAGE = 0.75
# HARD_LIMIT_PERCENTAGE = 0
HARD_NUMBER_FIRST = 871


def generate_collatz_base(numbers):
    """recursively generate the Collatz series"""
    assert numbers[-1] > 0
    if numbers[-1] == 1:
        return numbers
    if numbers[-1] % 2 == 0:
        numbers.append(int(numbers[-1] / 2))
    else:
        numbers.append(3 * numbers[-1] + 1)
    return generate_collatz_base(numbers)


def generate_collatz(number):
    """recursively generate the Collatz series: easy to use wrapper around the real worker"""
    assert number != 0
    numbers = generate_collatz_base([number])
    return len(numbers)


def generate_collatz_length(number):
    """recursively generate the Collatz series, only the length"""
    assert number > 0
    if number == 1:
        return 1
    next_number = int(number / 2) if (number % 2 == 0) else 3 * number + 1
    return 1 + generate_collatz_length(next_number)


def add_new_size(table, element, size, longest, print_it):
    """add the sequence to the table and see if we have a new partial solution"""
    limit = len(table)

    assert element <= limit
    if element > limit:
        # print(element, limit)
        return False

    # assert 0 == table[element-1]  # possible: the divisible by 3 series
    if table[element - 1] != 0:
        return False
    table[element - 1] = size

    if table[longest.val - 1] < size:
        if print_it:
            print("New best: ", element, "-", size)
        longest.val = element

    return True


def process(value, size, solved_table, longest, print_it):
    """process the next sequence, particularly the series of divisible by 3"""
    assert value > 1 and value != 4

    (table, found_count) = solved_table
    limit = len(table)

    # Did it: "OverflowError: integer division result too large for a float"
    if value % 3 == 1 and (int((value - 1) / 3) % 3 != 0):
        if add_new_size(table, value, size, longest, print_it):
            found_count += 1
    elif add_new_size(table, value, size, longest, print_it):
        found_count += 1

        # special case: already divisible by 3
        if value % 3 == 1:
            assert int((value - 1) / 3) % 3 == 0
            value = int((value - 1) / 3)
            size1 = size + 1
            while value < limit:
                if add_new_size(table, value, size1, longest, print_it):
                    found_count += 1
                value *= 2
                size1 += 1

    return found_count


def add(next_to_process, solved_table, new_element, longest, print_it):
    """see the next sequence: is it valid? has to be processed? new partial solution found?"""

    # R: 96, 0: Too many arguments (8/5) (too-many-arguments)
    (value, size) = new_element
    (all_lengths, found_count, processed) = solved_table
    limit = len(all_lengths)

    if value <= limit:
        if all_lengths[value - 1] != 0:
            return found_count

    # processed: some improvement
    elif value in processed:
        return found_count
    else:
        processed.add(value)

    next_to_process.append((value, size))
    if value < limit:
        return process(value, size, (all_lengths, found_count), longest, print_it)
    else:
        return found_count

    # ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
    # time

    # # 1 list
    # 440:    3s
    # 500:    24s
    # 700:    28s

    # # 2 lists (to_process1 and to_process2)
    # 440:    1s
    # 500:    7s
    # 700:    8s

    # # 2 lists + no processed list
    # 1000:     nope

    # # 2 lists + HARD_LIMIT
    # 1000:     18s [703, 871, 937]

    # # 2 lists + HARD_LIMIT_PERCENTAGE
    # 1000:       1s
    # 10000:      166s
    # 10000:      157s (improved, no processed, 0.95)
    # 10000:      159s (previous + processed)
    # 10000:      27s (no processed, 0.9)
    # 10000:      17s (sort improvement, no processed, 0.9)
    # 100000:     143s (previous +  no processed, 0.7)
    # 100000:     139s (processed, 0.7)
    # 1000000:    234s (previous + processed, 0.7):   brutal approach

    # ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##


def find_longest_chain_generate_all(all_lengths, print_it=False):
    """finds the longest Collatz sequence by trying to generate all the sequences backwards:
    the real worker function"""
    limit = len(all_lengths)

    best = lambda: 0
    best.val = 4

    # the current size has to be remembered as there can be always two paths to follow
    to_process1 = []
    to_process2 = []
    processed = set([i + 1 for i, x in enumerate(all_lengths) if x != 0])
    found = add(
        to_process2, (all_lengths, len(processed), processed), (8, 4), best, print_it
    )

    # to hard to process
    limit_top = HARD_LIMIT if limit >= HARD_NUMBER_FIRST else 0

    while found != limit:
        assert found < limit
        choose1 = len(to_process1) != 0 and (
            len(to_process2) == 0 or to_process1[0] < to_process2[0]
        )

        (val, size) = to_process1.pop(0) if choose1 else to_process2.pop(0)
        found_saved = found

        # print("Popped: ", val, '(', size, ')')

        if limit_top == 0 or val * 2 < limit_top * limit:
            # we cannot eliminate the values by 2x multiplication: they need to be processed

            found = add(
                to_process2,
                (all_lengths, found, processed),
                (val * 2, size + 1),
                best,
                print_it,
            )  # pylint: disable=line-too-long
            if choose1 and found != found_saved:
                to_process2 = sorted(set(to_process2), key=lambda x: x[0])

        if val % 3 == 1:
            to_add = int((val - 1) / 3)
            # it has to be an odd number, otherwise we would divide it
            # if to_add%2 == 1 and to_add > 1 and not (to_add in processed):
            if to_add % 2 == 1:
                found = add(
                    to_process1,
                    (all_lengths, found, processed),
                    (to_add, size + 1),
                    best,
                    print_it,
                )  # pylint: disable=line-too-long
                if found != found_saved:
                    to_process1 = sorted(set(to_process1), key=lambda x: x[0])
                # to_process1 = sorted(set(to_process1), key=lambda x: x[1])  #even slower
                # print(to_process1)

        if len(to_process1) + len(to_process2) == 0:
            break

        if found_saved != found:
            if print_it:
                print(found)
            if 0.995 * limit <= found and HARD_NUMBER_FIRST < limit:
                zeros_print = [i + 1 for i in range(limit) if all_lengths[i] == 0]
                if zeros_print:
                    print(zeros_print)
            if HARD_LIMIT_PERCENTAGE != 0 and HARD_LIMIT_PERCENTAGE * limit < found:
                break

    return best.val


def find_longest_chain_generate(limit, print_it=False):
    """finds the longest Collatz sequence by trying to generate all the sequences backwards"""
    assert limit >= 4

    all_lengths = [0 for i in range(limit)]
    # avoid the cycle 1,2,4
    # print(1,2,4)
    all_lengths[1 - 1] = 1
    all_lengths[2 - 1] = 2
    all_lengths[4 - 1] = 3

    best_value = find_longest_chain_generate_all(all_lengths, print_it)

    zeros = [i + 1 for i in range(limit) if all_lengths[i] == 0]
    if zeros:
        if print_it:
            print("Zeros size:", len(zeros))
        for i in zeros:
            assert all_lengths[i - 1] == 0
            all_lengths[i - 1] = generate_collatz(i)
            if all_lengths[best_value - 1] < all_lengths[i - 1]:
                best_value = i

    return (all_lengths, best_value)


def find_longest_chain_brute(limit, print_it=False):
    """finds the longest Collatz sequence using the brutal force approach"""
    best = lambda: 0
    best.val = 8
    best.size = 4

    # - limit/2: 2x has already a greater length
    for i in range(int(limit / 2), limit):
        size = generate_collatz_length(i)
        if size > best.size:
            best.val = i
            best.size = size
            if print_it:
                print("New best: ", best.val, "-", best.size)
        elif i % 1000 == 0:
            # print(i)
            pass

    return ([], best.val)


def find_longest_chain(limit, print_it=False):
    """the main function: it calls a variant worker"""
    start_time = time.time()

    best = find_longest_chain_brute(limit, print_it)[1]
    # best = find_longest_chain_generate(limit, print_it)[1]
    numbers = generate_collatz_base([best])
    if print_it:
        print("Best: ", numbers[0], "-", len(numbers))
        biggest_number = reduce(
            lambda x, y: x if x[1] > y[1] else y, enumerate(numbers)
        )
        print("Biggest number in sequence:", biggest_number)

    end_time = time.time()
    if print_it:
        print("Elapsed time:", 1 + int(end_time - start_time), "seconds.")

    return numbers


def debug_validations_generate():
    """all the assertions: Collatz lengths"""
    assert generate_collatz(1) == 1
    assert generate_collatz(2) == 2
    assert generate_collatz(3) == 8
    assert generate_collatz(4) == 3
    assert generate_collatz(6) == 9
    # 7  22  11  34  17  52  26  13  40  20  10  5  16  8  4  2  1
    assert generate_collatz(7) == 17
    assert generate_collatz(8) == 4
    assert generate_collatz(9) == 20
    assert generate_collatz(12) == 10  # 12  6  3  10  5  16  8  4  2  1
    assert generate_collatz(13) == 10
    # 15  46  23  70  35  106  53  160  80  40  20  10  5  16  8  4  2  1
    assert generate_collatz(15) == 18
    assert generate_collatz(19) == 21
    assert generate_collatz(27) == 112
    assert generate_collatz(171) == 125
    assert generate_collatz(235) == 128
    assert generate_collatz(327) == 144
    # [639, 1918, 959, 2878, 1439, 4318, 2159, 6478, 3239, 9718, 4859, 14578, 7289, \
    # 21868, 10934, 5467, 16402, 8201, 24604, 12302, 6151, 18454, 9227, 27682, 13841, \
    # 41524, 20762, 10381, 31144, 15572, 7786, 3893, 11680, 5840, 2920, 1460, 730, 365, \
    # 1096, 548, 274, 137, 412, 206, 103, 310, 155, 466, 233, 700, 350, 175, 526, 263, \
    # 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, 334, 167, 502, 251, 754, 377, \
    # 1132, 566, 283, 850, 425, 1276, 638, 319, 958, 479, 1438, 719, 2158, 1079, 3238, \
    # 1619, 4858, 2429, 7288, 3644, 1822, 911, 2734, 1367, 4102, 2051, 6154, 3077, 9232, \
    # 4616, 2308, 1154, 577, 1732, 866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, \
    # 92, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    assert generate_collatz(639) == 132  # even harder
    assert generate_collatz(667) == 145  # hard one
    assert generate_collatz(703) == 171  # hardest      (82, 250504)
    assert generate_collatz(763) == 153
    assert generate_collatz(871) == 179  # best by 1000
    assert generate_collatz(927) == 117
    assert generate_collatz(6171) == 262  # best by 10000
    assert generate_collatz(7131) == 195
    assert generate_collatz(7515) == 208
    assert generate_collatz(9225) == 229
    assert generate_collatz(69110) == 250
    assert generate_collatz(77031) == 351  # best by 100000
    assert generate_collatz(837799) == 525  # best by 1000000


def debug_validations():
    """all the assertions"""
    debug_validations_generate()
    assert [
        1,
        2,
        8,
        3,
        6,
        9,
        17,
        4,
        20,
        7,
        15,
        10,
        10,
        18,
        18,
        5,
        13,
        21,
        21,
        8,
    ] == find_longest_chain_generate(20, False)[0]
    assert [
        1,
        2,
        8,
        3,
        6,
        9,
        17,
        4,
        20,
        7,
        15,
        10,
        10,
        18,
        18,
        5,
        13,
        21,
        21,
        8,
        8,
        16,
        16,
        11,
        24,
        11,
        112,
        19,
        19,
        19,
    ] == find_longest_chain_generate(30, False)[0]


if __name__ == "__main__":
    debug_validations()
    # 837799 => size 525, 63s brute force
    # find_longest_chain(1000000, True)
    print("Solution: ", find_longest_chain(1000000, True)[0])
