"""
    Problem 19 : Counting Sundays
    http://projecteuler.net/problem=19
        How many Sundays fell on the first of the month during the twentieth century \
            (1 Jan 1901 to 31 Dec 2000)?
        Short answer: 12*100/7 = 171
    Version: 2016.01.02

    pylint--version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10
"""

def is_leap_year(year):
    """is the given year a leap one? it affects February"""
    return year%4 == 0 and (year%100 != 0 or year%400 == 0)

def count_sundays():
    """solve the problem, print the needed time"""
    days_by_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # 1900 is not a leap year
    assert not is_leap_year(1900)
    # Convention: 0 = Monday
    day1 = 365%7
    year = 1901
    sundays = 0
    while year != 2001:
        days_by_month[1] = 29 if is_leap_year(year) else 28
        for month in days_by_month:
            day1 += month
            if day1%7 == 6:
                sundays += 1
        year += 1

    return sundays

if __name__ == "__main__":
    print(count_sundays())
