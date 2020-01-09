import sys
sys.path.insert(0,'../')
from proxy_get_soup import get_soup_html,get_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken
import pprint

MAX_WORKER = 5
news_links = {}
prepared_links = {}
CATEGORY = {"politics":'category/leisure/health/',"sports":'home-sports/', "business":'category/business/local-business/'}

# categorise links
def get_freemalaysiatoday_news_links(soup, category):
   links = [item.find('a')['href'] for item in soup.find_all("div", attrs={"class": "td-module-thumb"})]
   news_links[category]=set(links)
   links.clear()
   #print(news_links)
 
def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = (soup.find("h1", attrs={"class":"entry-title"})).text
   except:
      heading = None
   try: 
      imgpath = soup.find('figure').find('img')['src']
   except :
      try:
         imgpath = soup.find('img', attrs={'class':'size-full'})['src']
      except:
         imgpath = None
   try:
      g = soup.find('div',attrs={'class':'td-post-content tagdiv-type'})
      summary = " ".join(p.text for p in g.find_all('p'))
   except:
      summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://www.freemalaysiatoday.com/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_freemalaysiatoday_news_links, get_soup(value), key) for key,value in CATEGORY.items() ]
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
   
   with open('freemalaysiatoday.json', 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))     
   

if __name__ == "__main__":
   get_proxy()
   main()
  
