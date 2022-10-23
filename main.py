# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import nltk
# import urllib.request
# response = urllib.request.urlopen('http://php.net/')
# html = response.read()
# print (html)

from bs4 import BeautifulSoup
import urllib.request
response = urllib.request.urlopen('http://php.net/')
html = response.read()
soup = BeautifulSoup(html,"html.parser")
text = soup.get_text(strip=True)
print (text)

tokens = [t for t in text.split()]
print (tokens)