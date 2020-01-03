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
CATEGORY = ['sports', 'business', 'life', 'health', 'technology', 'news/world', 'life/fashion-beauty']
news_links={}
link=[]
# categorise links
def get_montrealGazette_links(soupAll, category):
   soup = soupAll.find('div', attrs={'id': 'main'})
   for item in soup.find_all('h2'):
      try:
         link.append(item.find('a')['href'])
      except:
         pass
   for item in soup.find_all('h4'):
      try:
         link.append(item.find('a')['href'])
      except:
         pass
   for item in soup.find_all('h3'):
      try:
         link.append(item.find('a')['href'])
      except:
         pass
   news_links[category] = set(link)
   #pprint.pprint(news_links)

def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1", attrs={'class':"entry-title"}).text
   except:
      heading = None
      print(link)
   try:
      imgpath = soup.find('figure').find('img')['src']
   except :
      imgpath = None
   try:
      summary = " ".join([p.text for p in soup.find('div', attrs={"itemprop":"articleBody"}).find_all('p')])
   except:
      summary = None
      print(link)
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://montrealgazette.com/category/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_montrealGazette_links, get_soup(value), value) for key,value in enumerate(CATEGORY) ]
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
   
   with open('montrealGazette.json', 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links)) 

if __name__ == "__main__":
   get_proxy()
   main()
'''
if __name__ == "__main__":
   get_proxy()
   soup = get_soup_html('https://montrealgazette.com/category/sports')
   get_montrealGazette_links(soup,'lol')
   get_news_data('https://montrealgazette.com/sports/hockey/canada-rides-four-power-play-goals-in-first-to-pound-czechs-for-top-spot/wcm/2e06fa55-cdc4-4a8c-af47-1234cf576a7c')
'''