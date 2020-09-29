# caesar.py
#
# My solution to problem from https://realpython.com/python-practice-problems/
""" Caesar Cipher
    A Caesar cipher is a simple substitution cipher in which each letter of the
    plain text is substituted with a letter found by moving n places down the
    alphabet. For example, assume the input plain text is the following:

        abcd xyz

    If the shift value, n, is 4, then the encrypted text would be the following:

        efgh bcd

    You are to write a function that accepts two arguments, a plain-text
    message and a number of letters to shift in the cipher. The function will
    return an encrypted string with all letters transformed and all
    punctuation and whitespace remaining unchanged.

    Note: You can assume the plain text is all lowercase ASCII except for
    whitespace and punctuation.
"""

test_inputs = [("foo", 2), ("pickle", 5), ("easy one", 3)]
expected_results = ["hqq", "unhpqj", "hdvb rqh"]


def get_shifted_letter(onechar, shift_amount=0):
    ''' Return a corresponding letter, given a letter starting point and
        a integer offset '''

    # Set up our alphabet / shift table
    alphabet_chars = list("abcdefghijklmnopqrstuvwxyz")

    # Handle non alphabetic characters
    if onechar not in alphabet_chars:
        return(onechar)

    # Get the starting position
    pos = alphabet_chars.index(onechar)

    # calculate the resulting position
    newpos = (pos + shift_amount) % len(alphabet_chars)

    # return the character at the new position
    return(alphabet_chars[newpos])


def encrypt_word(msg, shift_amount=0):
    ''' return string where each character is shifted by x amount.
        ignore non alpha-numerics'''

    # use list comprehension to call our letter shifter for each letter
    encrypted_list = [get_shifted_letter(one_letter, shift_amount) for one_letter in list(msg)]

    # join the letters back into a string and return it
    return("".join(encrypted_list))


# Test
for i in range(0, len(test_inputs)):
    print("Test {}: Encrypting {} with offset {} - Expected result {}".format(
        i, test_inputs[i][0], test_inputs[i][1], expected_results[i]))
    result = encrypt_word(test_inputs[i][0], test_inputs[i][1])
    if result == expected_results[i]:
        print("  pass")
    else:
        print("  fail - result was {}".format(result))
