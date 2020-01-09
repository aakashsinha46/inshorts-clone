import sys
sys.path.insert(0,'../')
from proxy_get_soup import get_soup_html, get_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken
import pprint

CATEGORY = {"entertainment":'showbiz',"sports": 'sports',"technology": 'tech-gadgets',"business": 'money', "lifestyle":'life'}
MAX_WORKER = 5
news_links = {}
prepared_links = {}

def get_malaymail_news_link(soup, category):
   links = [item2.find('a')['href'] for item in soup.find_all("div", attrs={"class":"content"}) for item2 in item.find_all("li")]
   for index, item in enumerate(links):
      if item.find("https://www.malaymail.com"):
         link = "https://www.malaymail.com{item}".format(item=item)
         links[index] = link
   news_links[category] = links
   
def get_news_data(link):
   soup = get_soup_html(link)

   try:
      heading = soup.find("h1").text 
   except:
      heading = None
   try:
      imgPath = soup.find("figure").find('img')['src'] # image path
   except:
      imgPath = None
   try:
      summary = " ".join([p.text for p in soup.find("div",attrs={"class":"col-12 col-md-7 col-lg-8 primary"}).select('article >p')]) 
   except:
      summary = None
   
   return {
      'image' : imgPath,
      'heading' : heading,
      'desc' : summary,
      'link' : link      
   }

def get_soup(category :None):
   return get_soup_html("https://www.malaymail.com/news/{link}".format(link=category))

@time_taken
def main():
   #threading
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      #submit to pool object 
      pool = [ executor.submit(get_malaymail_news_link, get_soup(value), key) for key,value in CATEGORY.items() ]
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
   
   with open( 'malaymail.json', 'w') as f:           #the output output.json
      f.write(json.dumps(prepared_links))

if __name__ == "__main__":
    get_proxy()
    main()

   
