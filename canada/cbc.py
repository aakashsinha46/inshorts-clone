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
CATEGORY = ['news/politics', 'news/business', 'news/health', 'news/entertainment', 'news/technology', 'news/world', 'sports']

link=[]

# categorise links
def get_cbc_news_links(soup, category):
   for item in soup.find("div", attrs={"class":"contentArea"}).find_all('a'):
      if item is not None:
         if ':' in item['href']:
            link.append(item['href'])
         else:
            link.append('https://www.cbc.ca{links}'.format(links = item['href']))
   news_links[category] = set(link)


def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1", attrs={'class':"detailHeadline"}).text
   except:
      heading = None
   try:
      imgpath = soup.find('img')['srcset'].split(",")[-1]
      if imgpath is '':
         imgpath = soup.find('img')['src'].split(",")[-1]
   except :
      imgpath = None
   try:
      summary = " ".join([p.text for p in soup.find('div', attrs={'class':'story'}).find_all('p')])
   except:
      summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://www.cbc.ca/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_cbc_news_links, get_soup(value), value) for key,value in enumerate(CATEGORY) ]
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
   
   with open('cbc.json', 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))     
   

if __name__ == "__main__":
   get_proxy()
   main()
