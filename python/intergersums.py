# integersums.py
#
# My solution to problem from https://realpython.com/python-practice-problems/
""" Sum of Integers Up To n
    Write a function, add_it_up(), that takes a single integer as input
    and returns the sum of the integers from zero to the input parameter.

    The function should return 0 if a non-integer is passed in.
"""

from functools import reduce

test_nums = [1, 3, 4, 5, 6, 3.5, "pickle"]
expected_results = [1, 6, 10, 15, 21, 0, 0]


def process_nums(a, b):
    ''' Used as a function to pass to reduce() '''
    return(a + b)


def add_it_up(num):
    ''' return the sum of an int and all the numbers below it.
        Return 0 if it's not an int '''

    # Handle non integers
    if not isinstance(num, int):
        return(0)

    # Compute the factorial and return it
    onesum = reduce(process_nums, range(1, num + 1))
    return(onesum)


# Tests
for i in range(0, len(test_nums)):
    onesum = add_it_up(test_nums[i])
    if onesum == expected_results[i]:
        print("{}: {} worked with result {}".format(i, test_nums[i], onesum))
    else:
        print("{}: {} failed with result {}.  Expected {}".format(
            i, test_nums[i], onesum, expected_results[i]))
