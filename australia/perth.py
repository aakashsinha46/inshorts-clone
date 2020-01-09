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
CATEGORY = {"lifestyle":'lifestyle',"business":'business',"entertainment":'entertainment', "sports":'sport', "world":'news/world', "technology":'technology', "fashion":'lifestyle/fashion', "health":'lifestyle/health-wellbeing'}
link=[]

# categorise links
def get_cbc_news_links(soup, category):
   for item in soup.find_all('a',{'class': 'Card-Header css-v9imzv'}):
      if '.com' in str(item['href']) or '.org' in str(item['href']):
         pass
      else:
         link.append('https://www.perthnow.com.au{links}'.format(links=item['href']))

   for item in soup.find_all('a', attrs={'class':"css-1v5gzqy"}):
      if '.com' in str(item['href']) or '.org' in str(item['href']):
         pass
      else:
         link.append('https://www.perthnow.com.au{links}'.format(links=item['href']))

   for item in soup.find_all('a', attrs={'class':"css-f3rrhs"}):
      if '.com' in str(item['href']) or '.org' in str(item['href']):
         pass
      else:
         link.append('https://www.perthnow.com.au{links}'.format(links=item['href']))

   news_links[category] = set(link)
   link.clear()

def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1",{'class': 'css-1hlpc8v'}).text
   except:
      heading = None 
   try:
      imgpath = soup.find('img', {'class':'css-s8hxba'})['src']
   except :
      imgpath = None 
   try:
      summary = " ".join([p.text for p in soup.find('div', attrs={'class':'css-8atqhb'}).find_all('p')])
   except:
      summary = None     
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link': link
   }

def get_soup(category:None):
   return get_soup_html("https://www.perthnow.com.au/{link}".format(link=category))

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

   with open('perth.json', 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))

if __name__ == "__main__":
   get_proxy()
   main()
