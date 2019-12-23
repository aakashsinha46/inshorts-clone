from requests_html import HTMLSession, HTML  
from bs4 import BeautifulSoup as bs
from pyppeteer.errors import NetworkError, TimeoutError
import pyppeteer
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from fake_useragent import UserAgent
import random
import logging
from socket import timeout
import requests
 
# create an HTML Session object
session = HTMLSession()

def return_soup(url=None):
   #time.sleep(10)
   print(url)
   while True:
      try :
         resp = session.get(url)
         resp.html.render()
         soup =  bs(resp.html.html, "lxml")
         #resp.close()
         #session.close()
         print('hola')
         return soup
      #resp.close(), session.close() this two functions needed to be called 
      #at the return so to clode the connection 
      except :
         resp.close()
         session.close()
         print('lol')

   
 
# Use the object above to connect to needed webpage
'''resp = session.get("https://www.straitstimes.com/sport")
soup = bs(resp.html.html,'lxml')
resp.html.render()  # ye bhai kabhi kabhi error de deta hai , pata nahi kyo, abhi chal raha hai

def get_html_soup():
   try:
      soup =  bs(resp.html.html, "lxml")
      links = [item['href'] for item in soup.find_all('a', attrs={"class" : "block-link"})]
      final_link = [ "https://www.straitstimes.com/{link}".format(link=item) for item in links]
      print(final_link)

   except (TimeoutError, NetworkError):
      print('lol')
try:
   soup =  bs(resp.html.html, "lxml")
except (TimeoutError, NetworkError):
      print('lol')

links = [item['href'] for item in soup.find_all('a', attrs={"class" : "block-link"})]
final_link = [ "https://www.straitstimes.com/{link}".format(link=item) for item in links]
print(final_link)

resp.close()
session.close()'''

