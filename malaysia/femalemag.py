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
CATEGORY = {'fashion': ''}
link=[]

# categorise links
def get_femalemag_news_links(soup, category):
   for item in soup.find_all("h2", attrs={"class":"title entry-title"}):
      if item.find('a') is not None:
         link.append(item.find('a')['href'])
   news_links[category] = set(link)

def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1").text
   except:
      heading = None
   try:
      imgpath = soup.find('div', attrs={'class':'theiaPostSlider_preloadedSlide'}).find('img')['data-lazy-src']
   except :
      imgpath = None
   try:
      summary = " ".join([p.text for p in soup.find('div', attrs={'class':'theiaPostSlider_preloadedSlide'}).find_all('p')])
   except:
      summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://femalemag.com.my/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_femalemag_news_links, get_soup(value), key) for key, value in CATEGORY.items() ]
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
   
   with open('{path}/malaysia/femalemag.json'.format(path=masterPath), 'w') as f:          #the output output.json
      f.write(json.dumps(prepared_links))
   
if __name__ == "__main__":
   get_proxy()
   main()
