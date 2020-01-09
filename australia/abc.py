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
CATEGORY = {"politics":'politics/', "sports":'sport/', "health":'health/', "world":'world/', "business":'business/', "techonology":'technology/'}
news_links={}
link=[]
# categorise links  'world/' 'business/', 'sport/', 'technology/', 'health/', 'world/'
def get_abc_news_links(soup, category):
   soup2 = soup.find('div',attrs={'class':"c75l"})
   try:
      for item in soup2.find_all("h3"):
         link.append('https://www.abc.net.au{links}'.format(links = item.find('a')['href']))
   except:
      try:
         for item in soup.find_all('div', attrs={"class":"_1b2z1"}):
            link.append('https://www.abc.net.au{links}'.format(links = item.find('a')['href']))
      except:
         print('polop')

   news_links[category] = set(link)
   link.clear()

def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("div", attrs={'class':"article section"}).find('h1').text
   except:
      try:
         heading = soup.find('h1', attrs={"itemprop":"name"}).text
      except:
         heading = None
   try:
      imgpath = soup.find('div', attrs={"class" : 'inline-content photo full'}).find('img')['src'] 
   except :
      try:
         imgpath = soup.find('div', attrs={'class':"component comp-image lightbox-trigger"}).find('img')['srcset'].split(',')[-1]
         print(imgpath)
      except:
         imgpath = None
   try:
      summary = " ".join([p.text for p in soup.find('div', attrs={"class":"article section"}).find_all('p')])
   except:
      try:
         summary = " ".join([p.text for p in soup.find('div', attrs={"class":"comp-rich-text article-text clearfix"}).find_all('p')])
      except:
         summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://www.abc.net.au/news/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_abc_news_links, get_soup(value), key) for key,value in CATEGORY.items() ]
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
   
   with open('abc.json', 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))     
   
if __name__ == "__main__":
   get_proxy()
   main()
