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

CATEGORY = {"politics":'news/politics', "business":'business', "sports":'sports', "lifestyle":'lifestyle', "fashion":'taxonomy/term/4991'}  #taxonomy/term/4991 is fashion
MAX_WORKER = 5
news_links = {}
prepared_links = {}
link =[]

def get_nst_news_link(soup, category):
   for item in soup.find_all("span", attrs={"class":"field-content"}):
      if item.find('a') is not None:
         link.append("https://www.nst.com.my/{link}".format(link=item.find('a')['href']))
   news_links[category] = set(link)
   link.clear()

def get_news_data(link):
   soup = get_soup_html(link)
   
   try:
      heading = soup.find('div',attrs={"class":'ph-wrapper'}).text #heading
   except:
      heading = None
   try:
      imgPath =  (soup.find("div",attrs={"class":"field-content"})).find('img')['src'] # image path
   except:
      imgPath = None
   try:
      summary = " ".join([p.text for p in soup.find("div",attrs={"class":"field-item even"}).select('p')])
   except:
      summary = None
   return {
      'image' : imgPath,
      'heading' : heading,
      'desc' : summary,
      'link' : link
   }

def get_soup(category:None):
   return get_soup_html("https://www.nst.com.my/{link}".format(link=category))

@time_taken
def main():
   #threading
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      #submit to pool object 
      pool = [ executor.submit(get_nst_news_link, get_soup(value), key) for key,value in CATEGORY.items() ]
      #on complete
      for task in as_completed(pool):
         task.result()
   # prepare links of category to links news
   for category, links in news_links.items():
      prepared_links[category] = []
      with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
         pool_links = [executor.submit(get_news_data, link) for link in links]
         sleep(5)
         #print("sleeping")
         for task_link in as_completed(pool_links):
            prepared_links[category].append(task_link.result())

   with open('{path}/malaysia/nst.json'.format(path=masterPath), 'w') as f:           #the output at asiaone_output.json
      f.write(json.dumps(prepared_links))

if __name__ == "__main__":
    get_proxy()
    main()