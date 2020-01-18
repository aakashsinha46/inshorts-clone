import pprint
import json
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

import os
masterPath = os.getcwd() #main project dir, it does not return pwd it return the calling dir

import sys
sys.path.insert(0, masterPath)

#user defined modules
from proxy_get_soup import get_soup_html,get_proxy
from decorators import time_taken

MAX_WORKER = 5
news_links = {}
prepared_links = {}
CATEGORY = {"world":'world', "lifestyle":'lifestyle', "entertainment":'entertainment', "technology":'technology', "business":'finance', "sports":'sport', "health":'lifestyle/health', "fashion":'lifestyle/fashion'}
news_links={}
link=[]

#sidebar-rhc widget_newscorpau_query_posts
def get_news9_news_links(soup, category):
   for item1 in soup.find_all('div', attrs={'class':'widget'}):
      if item1.find('div', attrs={'id':"anchor-video"}):
         continue
      for items in item1.find_all('div', attrs={"class":"story-block"}):
         for item in items.find_all('h4'):
            link.append(item.find('a')['href'])   
   try:
      for item in soup.find('ul', attrs={"class":"breaking-news-list"}).find_all('li'):
         link.append(item.find('a')['href'])
   except:
      try:
         for item in soup.find('ul', attrs={"class":"trending-news-list"}).find_all('li'):
            link.append(item.find('a')['href'])
      except:
         pass
   for item in link:
      if '/video/' in str(item):
         link.remove(item)

   news_links[category] = set(link)
   link.clear()

def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1").text
   except:
      heading = None
   try:
      imgpath = soup.find('div', attrs={"class" : 'image-wrapper'}).find('img')['src']
   except :
      imgpath = None
   try:
      summary = " ".join([p.text for p in soup.find('article', attrs={"id":"story"}).find_all('p')])
   except:
      try:
         summary = " ".join([p.text for p in soup.find('div', attrs={"id":"story"}).find_all('p')])
      except:
         summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://www.news.com.au/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_news9_news_links, get_soup(value), key) for key,value in CATEGORY.items() ]
      # on complete
      for task in as_completed(pool):
         task.result()

   # prepare links of category to links newsfemalemag
   for category, links in news_links.items():
      prepared_links[category] = []
      with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
         pool_links = [executor.submit(get_news_data, link) for link in links]
         sleep(10)
         for task_link in as_completed(pool_links):
            prepared_links[category].append(task_link.result())

   with open('{path}/australia/newsAu.json'.format(path=masterPath), 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))

if __name__ == "__main__":
   get_proxy()
   main()
