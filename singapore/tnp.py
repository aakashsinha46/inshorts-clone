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
CATEGORY = {"sports":'sports', "business":'news/business', "fashion":'lifestyle/fashion'}

# categorise links
def get_tnp_news_links(soup, category):
   links = [item.find('a')['href'] for item in soup.find_all("h2", attrs={"class": "card-title"})]
   news_links[category]=links
   
def get_news_data(link):
   soup = get_soup_html(link)
   try:
      if soup.find('figure',attrs={'class':'group-media-frame field-group-html-element'})is not None:
         imgpath = (soup.find('figure',attrs={'class':'group-media-frame field-group-html-element'})).find('img')['src']
      else:
         imgpath = None
   except:
      imgpath = None
   try:
      heading = (soup.find("h1", attrs={'class':'story-headline'})).text
   except:
      heading = None
   try:
      summary =  " ".join(p.text for p in soup.select('div.body-copy > p'))
   except:
      summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }
   
def get_soup(category:None):
   return get_soup_html("https://www.tnp.sg/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_tnp_news_links, get_soup(value), key) for key,value in CATEGORY.items() ]
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
   
   with open('{path}/singapore/tnp.json'.format(path=masterPath), 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))
   
if __name__ == "__main__":
   get_proxy()
   main()
