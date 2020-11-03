''' webpage_filter - display a python filtered webpage '''

# Basic flow:
#   1. Stand up a http server
#   2. Grab url from get request
#   3. pull down the content based on the url
#   4. filter the content
#   5. return the resulting content via the http server

# ToDo: optimize filtering for better performance


# from bs4 import BeautifulSoup, Tag
import bottle
import datetime
import urllib.parse
import re
import requests

portnum = 8080
servername = 'localhost'

server = bottle.Bottle()


def get_webpage(url):
    ''' Pull down web content from a url and return it as a unicode string '''

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

    return(r.text)


def strip_scripts(data):
    """ Remove script content and return it """
    data = re.sub(r'<script.*?</script>', '<removed />', data, re.DOTALL)
    return(data)


def update_urls(data, svrurl, netloc):
    """ Prefix www URLs with this server's hostname/port """

    # Prefix www URLs with our proxy url
    data = re.sub(r'https://www\.', r'{}?x=https://www.'.format(svrurl), data)

    # Convert relative URLs to absolute and prefix our proxy url
    data = re.sub(r'<a href="/', r'<a href="{}?x=https://{}/'.format(svrurl,
                                                                     netloc),
                  data)
    return(data)


def disable_hide(data):
    """ Rename classes/tags that hide content """
    data = re.sub('<subscriber-only', '<disable-subscriber-only', data)
    return(data)


def thwart_trackers(data):
    """ munge known server names that are used for tracking """
    for tracker in ['addlightning', 'doubleclick', 'twitter', 'facebook', 'wa.me']:
        data = re.sub(tracker, tracker + "-disable", data)
    return(data)


def filter_content(data, svrurl="", netloc=""):
    """ Filter the content and return it """
#    data = strip_scripts(data)
    data = disable_hide(data)
    data = thwart_trackers(data)
    data = update_urls(data, svrurl, netloc)
    return(data)


def log(logstr):
    ''' Basic logging function '''
    logdatefmt = "%m/%d/%y %H:%M:%S"
    print(datetime.datetime.now().strftime(logdatefmt), logstr)


@server.route('/smdj')
def smdj():
    """ Use bottle to serve up the modified webpage """
    url = bottle.request.query.get('x')

    urldict = urllib.parse.urlparse(url)
    netloc = urldict.netloc

    svrurl = "http://{}:{}/smdj".format(servername, portnum)

    if url is None:
        return "Usage: {}?x=http://example.com/something".format(svrurl)

#    return '{}'.format(url)

    webcontent = filter_content(get_webpage(url), svrurl, netloc)
    return '{}'.format(webcontent)


if __name__ == "__main__":
    bottle.run(server, host=servername, port=portnum, debug=True)
