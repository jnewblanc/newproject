# Given a strings that represents a patten of characters, find other strings
# that have a similar pattern of characters.  The pattern is the count of
# consecutive characters.  For example:
# Input:
#   pattern  = boo
#   dict[] = {abb,abc,xyz,xyy,sba,baa,skb}
# Output:
#   abb xyy baa


def find_pattern(oneStr):
    """ return a list of numbers, each one representing the number of
        consecutive characters in the given string """
    character_pattern = []
    last_letter = ''
    counter = 0
    for letter in list(oneStr):
        if last_letter == '':
            counter += 1
        elif letter == last_letter:
            counter += 1
        else:
            character_pattern.append(counter)
            counter = 1
        last_letter = letter

    character_pattern.append(counter)
    return(character_pattern)


def pattern_matches(character_pattern=[], newstr=''):
    """ determine whether a given string matches the pattern """
    if character_pattern == find_pattern(newstr):
        return True
    return(False)


def get_matches(character_pattern=[], data=[]):
    """ given a character pattern and a list of strings, return a list of
        strings that match the character_pattern """
    matches = []
    for onedata in data:
        if pattern_matches(cp, onedata):
            matches.append(onedata)
    return(matches)


if __name__ == "__main__":
    data = ["abb", "abc", "xyz", "xyy", "sba", "baa", "skb"]
    pattern = "boo"

    # Generate the initial pattern once and store results for comparison
    cp = find_pattern(pattern)

    print("{}".format(" ".join(get_matches(cp, data))))
