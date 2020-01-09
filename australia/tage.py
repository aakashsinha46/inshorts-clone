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
CATEGORY = {"politics":'politics', "business":'business', "world":'world', "sports":'sport', "lifestyle":'lifestyle', "technology":'technology', "health":'healthcare'}
link=[]

def get_cbc_news_links(soup, category):
   for item in soup.find_all('h3',{'class': '_2XVos'}):
      link.append('https://www.theage.com.au{links}'.format(links=item.find('a')['href']))
   news_links[category] = set(link)
   link.clear()

def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1",{'itemprop': 'headline'}).text.strip()
   except:
      heading = None
   try:
      imgpath = soup.find('div', {'class': '_1lwW_'}).find('img')['src']
   except :
      try:
         imgpath = soup.find('picture').find('img')[src]
         print(imgpath)
         print(link)
      except:
         imgpath = None    
   try:
      summary = " ".join([p.text.strip() for p in soup.find('div', attrs={'class':'_1665V undefined'}).find_all('p')])
   except:
      summary = None     
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link': link
    }

def get_soup(category:None):
   return get_soup_html("https://www.theage.com.au/{link}".format(link=category))

@time_taken

def main():
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

   with open('tage.json', 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))     

if __name__ == "__main__":
   get_proxy()
   main()
