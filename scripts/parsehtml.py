import sys
import os
#from urllib.request import urlopen
import html5lib
from pprint import pprint

##print(html5lib)
##
##with open("index.html", "rb") as f:
##    document = html5lib.parse(f)
##
##print(document.keys())

##with open("index.html") as f:
##    parser = html5lib.HTMLParser(strict=True)
##    document = parser.parse(f)
##    print(document)
##

"""Parse elements in an html file as an xml tree
NOT WORKING"""

with open("index.html", "r") as file:
    readed = file.read()
    file.close()
    print(readed)

#print(html5lib.parse(readed))
