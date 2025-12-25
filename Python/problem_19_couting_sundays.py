"""
    Problem 19 : Counting Sundays
    http://projecteuler.net/problem=19
        How many Sundays fell on the first of the month during the twentieth century \
            (1 Jan 1901 to 31 Dec 2000)?
        Short answer: 12*100/7 = 171
    Version: 2016.05.05

    pylint--version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10

    hackerrank:
        brute froce:                3/8 (timeout for the others)
        get_first_day improved:     6/8 (2 wrong answers)           Score: 71.43
        get_leap_years_to_1900:     Score: 100.00
            400 years margin correction

    Attention !
        1582 introduces the Gregorian calendar
"""


def is_leap_year(year):
    """is the given year a leap one? it affects February"""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# 1 Jan 1900 was a Monday.
def get_leap_years_to_1900(year):
    """calculate the number of leap years between 1900 and the given one"""
    years = year - 1900 if year > 1900 else 1900 - year
    leap_years = years // 4 - years // 100
    if year >= 1900:
        if years >= 100:
            leap_years += 1 + (years - 100) // 400
    elif years >= 300:
        leap_years += 1 + (years - 300) // 400
    return (years, leap_years)


def get_first_day_1(year):
    """get the first day of a given year: brute force"""
    assert not is_leap_year(1900)
    days = 0
    if year >= 1900:
        for i in range(1900, year):
            days += 366 if is_leap_year(i) else 365
        return days % 7
    else:
        for i in range(year, 1900):
            days += 366 if is_leap_year(i) else 365
        return 7 - days % 7


def get_first_day_2(year):
    """get the first day of a given year: calculus"""
    (years, leap_years) = get_leap_years_to_1900(year)
    # print(years, leap_years, is_leap_year(year))
    if year >= 1900 and is_leap_year(year):
        # calculate for 1 of january
        assert leap_years > 0
        leap_years -= 1
    days = 365 * years + leap_years
    day1 = days % 7
    if year >= 1900:
        return day1
    else:
        return 0 if day1 == 0 else 7 - day1


# 1 Jan 1900 was a Monday.
# Convention: 0 = Monday
def get_first_day(year):
    """get the first day of a given year"""
    return get_first_day_2(year)


def count_sundays_base(day1, year, first_month, last_month):
    """calculate the number of sundays in the first day of the month for an interval in a year"""

    # last month does not matter is day1 is not external parameter
    days_by_month = [day1, 31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_by_month[2] = 29 if is_leap_year(year) else 28

    day1 = sundays = 0
    for month in range(1, first_month):
        day1 += days_by_month[month - 1]
    for month in range(first_month, 1 + last_month):
        day1 += days_by_month[month - 1]
        # print("day1 ({0}): ".format(month), day1%7)
        if day1 % 7 == 6:
            sundays += 1
    if last_month == 12:
        day1 += days_by_month[12]
    return (sundays, day1)


def count_sundays_noday1(year, first_month, last_month):
    """shortcut"""

    day1 = get_first_day(year)
    (sundays, _) = count_sundays_base(day1, year, first_month, last_month)
    return sundays


def count_sundays_full_corrected(start, stop):
    """How many Sundays fell on the first of the month between two dates(both inclusive)?
    days ignored
    """
    assert start[1] >= 1 and start[1] <= 12
    assert stop[1] >= 1 and stop[1] <= 12

    day1 = get_first_day(start[0])
    sundays = 0

    if start[0] == stop[0]:
        (sundays_year, day1) = count_sundays_base(day1, start[0], start[1], stop[1])
        sundays += sundays_year
    else:
        (sundays_year, day1) = count_sundays_base(day1, start[0], start[1], 12)
        sundays += sundays_year

    for year in range(start[0] + 1, stop[0]):
        (sundays_year, day1) = count_sundays_base(day1, year, 1, 12)
        sundays += sundays_year

    if start[0] != stop[0]:
        (sundays_year, day1) = count_sundays_base(day1, stop[0], 1, stop[1])
        sundays += sundays_year
    # print(sundays)

    return sundays


def count_sundays_full(start, stop):
    """How many Sundays fell on the first of the month between two dates(both inclusive)?"""

    if start[2] > 1:
        new_start = (
            (start[0], start[1] + 1, 1) if start[1] != 12 else (start[0] + 1, 1, 1)
        )
        return count_sundays_full_corrected(new_start, stop)
    else:
        return count_sundays_full_corrected(start, stop)


def count_sundays(start, stop):
    """shortcut"""
    return count_sundays_full((start, 1, 1), (stop, 12, 31))


def read_solve_print():
    """read from console: hackerrank test"""

    number_of_intervals = int(input().strip())
    results = []
    for _ in range(0, number_of_intervals):
        date1 = [int(arr_temp) for arr_temp in input().strip().split(" ")]
        date2 = [int(arr_temp) for arr_temp in input().strip().split(" ")]

        results.append(count_sundays_full(date1, date2))
    for result in results:
        print(result)


def debug_validations():
    """all the assertions"""
    for year in range(1900, 1905):
        assert (year - 1900) == get_first_day(year)
    assert get_first_day(1905) == 6
    for year in range(1897, 1900):
        assert (7 - (1900 - year)) == get_first_day(year)
    assert get_first_day(1) == 0
    assert get_first_day(1582) == 4
    # 1582 introduces the Gregorian calendar
    assert get_first_day(1585) == 1
    assert get_first_day(1584) == 6
    assert get_first_day(1583) == 5
    assert get_first_day(1599) == 4
    assert get_first_day(1600) == 5
    assert get_first_day(1601) == 0
    assert get_first_day(1602) == 1
    assert get_first_day(1896) == 2
    assert get_first_day(2000) == 5
    assert get_first_day(2001) == 0
    assert get_first_day(3099) == 6
    assert get_first_day(3100) == 0
    assert get_first_day(3350) == 3

    assert count_sundays_noday1(1900, 1, 8) == 2
    assert count_sundays_noday1(1900, 4, 7) == 2
    assert count_sundays_noday1(1900, 4, 6) == 1

    assert count_sundays(1899, 1899) == 2
    assert count_sundays(1900, 1900) == 2
    assert count_sundays(1901, 1901) == 2
    assert count_sundays(1900, 1901) == 4
    assert count_sundays(1899, 1901) == 6
    assert count_sundays(2000, 2000) == 1
    assert count_sundays(2001, 2001) == 2
    assert count_sundays(2000, 2001) == 3

    assert count_sundays_full((1900, 1, 1), (1901, 1, 1)) == 2
    assert count_sundays_full((1900, 1, 1), (1900, 1, 1)) == 0
    assert count_sundays_full((1900, 4, 1), (1900, 5, 1)) == 1
    assert count_sundays_full((1900, 4, 2), (1900, 5, 1)) == 0
    assert count_sundays_full((1900, 12, 2), (1901, 5, 1)) == 0
    assert count_sundays_full((1900, 12, 2), (1901, 9, 1)) == 1
    assert count_sundays_full((1900, 12, 1), (1901, 12, 2)) == 2
    assert count_sundays_full((1900, 12, 2), (1901, 2, 2)) == 0

    # big ones
    assert count_sundays(1900, 2010) == 190
    assert count_sundays(1901, 2001) == 173

    # hackerrank
    assert count_sundays_full((1900, 1, 1), (1910, 1, 1)) == 18
    assert count_sundays_full((2000, 1, 1), (2020, 1, 1)) == 35

    # Project Euler
    assert count_sundays(1901, 2000) == 171


def main():
    """main function: defined explicitly for external calling and avoiding global scope"""
    debug_validations()
    # print(count_sundays(1900, 2010))
    # print(count_sundays_full((1900,12,2), (1901,5,1)))
    # print(get_first_day(2000))
    # read_solve_print()


if __name__ == "__main__":
    main()
