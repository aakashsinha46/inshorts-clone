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
CATEGORY = {"techonlogy":''}

link=[]

# categorise links
def get_cbc_news_links(soup, category):
   
   for item in soup.find_all("div", attrs={"class":"story story--large"}):
      link.append(item.find('a')['href'])
   news_links[category] = set(link)
 
def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find('h1',{'class':'u-m-0_25'}).text.strip()
   except:
      heading = None   
   try:
      item = soup.find('div', attrs={'class':"post-imageBleed"})
      imgpath = (item.find('div',attrs={'class':'post-featuredImage u-m-1_5'})).find('img')['src']
      #class="post-featuredImage u-m-1_5"
   except :
      imgpath = None    
   try:
      summary = " ".join([p.text for p in soup.find('div', attrs={'class':'post-body fb-quotable u-m-3'}).find_all('p')])
   except:
      summary = None   
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://thenextweb.com/ca{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_cbc_news_links, get_soup(value), key) for key,value in CATEGORY.items() ]
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
   
   with open('{path}/canada/tnw.json'.format(path=masterPath), 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))     
   
if __name__ == "__main__":
   get_proxy()
   main()
