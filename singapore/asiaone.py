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

CATEGORY = {"entertainment":'showbiz', "technology":'digital', "lifestyle":'lifestyle', "health":'health','world':'world'}
MAX_WORKER = 5
news_links = {}
prepared_links = {}

def get_asiaone_news_link(soup, category):
   link1 =[link['href']for item in soup.find_all("div", attrs={"class": "content overlay"})  for link in item.find_all('a', href=True) ]     
   link2 = [innerlink['href'] for item in soup.find_all("div", attrs={"class": "card col-xs-12 col-sm-4"}) for link in item.find_all("div", attrs={"class": "content"}) for innerlink in link.find_all('a', href=True) ]
   links = link1 + link2
   news_links[category] = set(links)
   links.clear()

def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1", attrs={"class": "ui header page__title"}).text #heading
   except:
      heading = None
   try:
      p = soup.find("div", attrs={"class": "field field-name-field-image"})
      q = p.find("div", attrs={"class": "content"})
      r = q.find("img", attrs={"class": "img-responsive"})
      imgPath = r['src']  # image path
   except:
      imgPath = None
   try:
      g = soup.find("div", attrs={"class": "field field-name-body field--type-text-with-summary field--label-hidden field-item"})
      summary = " ".join([p.text for p in g.select('p')])  #summary
   except:
      summary: None

   return {
      'image' : 'https://www.asiaone.com{image}'.format(image=imgPath),
      'heading' : heading,
      'desc' : summary,
      'link' : link      
   }

def get_soup(category:None):
   return get_soup_html("https://www.asiaone.com/{link}".format(link=category))

@time_taken
def main():
   #threading
   
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      #submit to pool object 
      pool = [ executor.submit(get_asiaone_news_link, get_soup(value), key) for key,value in CATEGORY.items()]
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
   
   with open('{path}/singapore/asiaone.json'.format(path=masterPath), 'w') as f:           #the output at asiaone_output.json
      f.write(json.dumps(prepared_links))
   
if __name__ == "__main__":
   get_proxy()
   main()