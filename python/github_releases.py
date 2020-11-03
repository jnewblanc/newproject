'''
Print a list of github repo release dates and names that are sorted by date

It addition to it's primary function, this script demonstrates basic
understanding of:
    o functional programming and coding style
    o use of standard libraries
    o api calls and parsing
    o custom sorting
    o error checking and exception handling
'''

#
# Github API for releases:
#   https://developer.github.com/v3/repos/releases/


import argparse
from datetime import datetime
import os
import pprint
import re
import requests
debug = False

# The following fields will be displayed, with the first being the sort key
desired_fields = ['created_at', 'name', 'url']
desired_date_format = "%m/%d/%y"
default_baseurl = "https://api.github.com"


def getData(url):
    ''' Pull down json from an api, and return the results as a python dict '''

    log("INFO Pulling data from url {}".format(url))

    # Make request & catch known connection exceptions
    try:
        r = requests.get(url, verify=True)
    except requests.exceptions.ConnectionError:
        log("ERROR API Request failed to connect")
        exit(1)
    except requests.exceptions.SSLError:
        log("ERROR https API Request failed due to invalid certificate")
        exit(1)

    # Basic error checking of http/https return code
    if r.status_code != 200:
        log("ERROR API Request returned error code {}".format(
            r.status_code) +
            " .  Please verify that the \"owner/repo\" is correct.")
        exit(1)

    return(r.json())


def sortFunc(oneItem):
    ''' Sort Function - return the first desired field as the sort key '''
    return(oneItem[desired_fields[0]])


def github_str_to_date(datestr):
    ''' given a github date string, return a python date object'''
    # 2020-06-06T04:10:45Z
    datefmt = "%Y-%m-%dT%H:%M:%SZ"
    dateobj = datetime.strptime(datestr, datefmt)
    return(dateobj)


def log(logstr):
    ''' Basic logging function
        Can easily be expanded or reimplemented as needed'''
    logdatefmt = "%m/%d/%y %H:%M:%S"
    print(datetime.now().strftime(logdatefmt), logstr)


def showData(rel_dict):
    ''' Output data sorted/formatted as desired '''
    if debug:
        pprint.pprint(rel_dict)

    # Display header
    print(" : ".join(desired_fields))

    # Loop through the data, using the sorting function to sort by field 0 (date)
    for one_rel in sorted(rel_dict, key=sortFunc):
        # put values into a list, so we can join and print them nicely
        field_vals = []
        for one_field in desired_fields:
            # If field value is a date, reformat it to be more readable.
            if re.match('[0-9][0-9][0-9][0-9]-[0-9][0-9]-', one_rel[one_field]):
                one_rel[one_field] = (github_str_to_date(
                    one_rel[one_field]).strftime(desired_date_format))
            field_vals.append(one_rel[one_field])
        print(" : ".join(field_vals))


def get_args():
    ''' Parse arguments and validate input'''
    parser = argparse.ArgumentParser(description="github releases")
    parser.add_argument("--repo", type=str, help="github repository")
    parser.add_argument("--baseurl", type=str, help="github baseurl",
                        default=default_baseurl)
    args = parser.parse_args()

    # argparse required parameters aren't verbose enough, so we'll construct our
    #   own response to the missing required arguments.
    if not args.repo or not re.match(r'\w+/\w+', args.repo):
        print("Usage: {} --repo <owner/repo>".format(os.path.basename(__file__)))
        print("  For example: {} --repo atom/atom".format(os.path.basename(__file__)))
        exit(1)

    return(args)


if __name__ == "__main__":
    args = get_args()
    apiUrl = '{}/repos/{}/releases'.format(args.baseurl, args.repo)
    showData(getData(apiUrl))
