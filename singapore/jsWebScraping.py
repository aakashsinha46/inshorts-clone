from requests_html import HTMLSession, HTML  
from bs4 import BeautifulSoup as bs
from pyppeteer.errors import NetworkError, TimeoutError
import pyppeteer
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken
 
# create an HTML Session object
session = HTMLSession()
MAX_WORKER = 5
news_links = {}
prepared_links = {}
CATEGORY = ['sport', 'lifestyle']
 
# Use the object above to connect to needed webpage
resp = session.get("https://www.straitstimes.com/sport")
soup = bs(resp.html.html,'lxml')
resp.html.render()  # ye bhai kabhi kabhi error de deta hai , pata nahi kyo, abhi chal raha hai
'''
def get_html_soup():
   try:
      soup =  bs(resp.html.html, "lxml")
      links = [item['href'] for item in soup.find_all('a', attrs={"class" : "block-link"})]
      final_link = [ "https://www.straitstimes.com/{link}".format(link=item) for item in links]
      print(final_link)

   except (TimeoutError, NetworkError):
      print('lol')'''
try:
   soup =  bs(resp.html.html, "lxml")
except (TimeoutError, NetworkError):
      print('lol')

links = [item['href'] for item in soup.find_all('a', attrs={"class" : "block-link"})]
final_link = [ "https://www.straitstimes.com/{link}".format(link=item) for item in links]
print(final_link)

resp.close()
session.close()

