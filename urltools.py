"""
Tools for parsing/analyzing url string.
"""
__author__ = 'Casper CY Chiang'
__version__ = '0.0.1'

import re
import sys
import urllib2
import codecs

import mafan
from mafan import text
from collections import Counter
from progressbar import *

ignoreList = ['www', 'http:', 'https:', 'app', 'apps', 'us', 'store']

def check_network_connection():
    try:
        response = urllib2.urlopen('http://www.google.com.tw', timeout = 1)
        return True
    except urllib2.URLError as err:
        print "No network connection."
        pass
    return False

def get_url(url_string, IS_CONTAINS_CHINESE):
    if IS_CONTAINS_CHINESE:
        url_string = urllib2.quote(url_string, safe="%/:=&?~#+!$,;'@()*[]")

    request = urllib2.Request(url_string)
    opener = urllib2.build_opener()
    result = opener.open(request)
    return result.url

if __name__ == "__main__":
    domainNameBucket = []

    widgets = ['Parsing: ', Percentage(),
                ' ', Bar(),
                ' ', ETA(),
                ' ', ' ']

    if len(sys.argv) == 2 and check_network_connection():
        fileName = sys.argv[1]
        print "File Name: " + fileName + "\n"

        try:
            unencode_urlsFile = open(fileName, 'r')
            unencode_urlsList = unencode_urlsFile.readlines()
            urlsListLength = len(unencode_urlsList)

            pbar = ProgressBar(widgets=widgets, maxval=urlsListLength).start()
            with codecs.open(fileName,'r',encoding='utf8') as urlsFile:
                for index, url in enumerate(urlsFile.readlines()):

                    IS_CONTAINS_CHINESE = text.contains_chinese(url)

                    if IS_CONTAINS_CHINESE:
                        result = get_url(unencode_urlsList[index], IS_CONTAINS_CHINESE)
                    else:
                        result = get_url(url, IS_CONTAINS_CHINESE)

                    resultSplit = result.split('/')
                    resultSplit.remove('')
                    for item in ignoreList:
                        if item in resultSplit:
                            resultSplit.remove(item)

                    domainNameBucket.append(resultSplit[0])
                    pbar.update(index)

            pbar.finish()
            print ""
            countResult = Counter(domainNameBucket)
            print countResult

        except IOError:
            print "IOError"
