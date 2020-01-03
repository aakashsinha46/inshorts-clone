import sys
sys.path.insert(0,'../')
from proxy_get_soup import get_soup_html,get_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken

MAX_WORKER = 5
news_links = {}
prepared_links = {}
CATEGORY = ['sport', 'busniess']
link=[]


# categorise links
def get_techcrunch_news_links(soup, category):
   for item in soup.find_all("h3", attrs={"class":"teaser__heading"}):
      if item.find('a') is not None:
         link.append('https://www.channelnewsasia.com{links}'.format(links=item.find('a')['href']))
   news_links[category] = link
   print(news_links)


def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1", {"class":"article__title"}).text
      print(heading)
   except:
      heading = None
   try:
      img = [item for item in soup.find('picture', attrs={'class':'picture__container'}).find('source')['data-srcset'].split(',')]
      imgpath = img[-2] +','+ img[-1].split(' ')[0] 
      print(imgpath)
   except :
      imgpath = None
   try:
      summary = " ".join([p.text for p in soup.find('div', attrs={'class':'c-rte--article'}).find_all('p')])
      print(summary)
   except:
      summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://www.channelnewsasia.com/news/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_techcrunch_news_links, get_soup(value), value) for key,value in enumerate(CATEGORY) ]
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
   
   with open('newsasia.json', 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))     
   

if __name__ == "__main__":
   get_proxy()
   main()
