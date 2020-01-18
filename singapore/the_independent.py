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
CATEGORY = {"business":'economy/', "lifestyle":'lifestyle/'}

# categorise links
def get_independent_news_links(soup, category):
   links = [item.find('a')['href'] for item in soup.find_all("h3", attrs={"class": "entry-title td-module-title"})]
   news_links[category]=set(links)
   links.clear()
   
def get_news_data(link):
   soup = get_soup_html(link)
   try:
      if soup.find('figure') is not None:
         imgpath = ((soup.find('figure')).find('a')['href'])
      else:
         imgpath = None
   except:
      imgpath = None
   try:
      heading = (soup.find("h1", attrs={"class":"tdb-title-text"})).text
   except:
      heading = None
   try:
      summary =  " ".join(p.text for items in soup.find_all("div", attrs={"class" : "tdb-block-inner td-fix-index"}) for p in items.find_all("p"))
   except:
      summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }
   
def get_soup(category:None):
   return get_soup_html("http://theindependent.sg/news/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_independent_news_links, get_soup(value), key) for key,value in CATEGORY.items() ]
      # on complete
      for task in as_completed(pool):
         task.result()

   # prepare links of category to links news
   for category, links in news_links.items():
      prepared_links[category] = []
      with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
         pool_links = [executor.submit(get_news_data, link) for link in links]
         sleep(10)
         #print("sleeping")
         for task_link in as_completed(pool_links):
            prepared_links[category].append(task_link.result())
   
   with open('{path}/singapore/the_independent.json'.format(path=masterPath), 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))      

if __name__ == "__main__":
   get_proxy()
   main()
