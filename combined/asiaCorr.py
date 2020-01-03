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
def get_asiaCorr_news_links(soup, category):
   for item in soup.find_all("h1", attrs={"class":"h2 entry-title"}):
      print("lol")
      if item.find('a') is not None:
         link.append(item.find('a')['href'])
   news_links[category] = link
   #print(news_links)


def get_news_data(link):
   soup = get_soup_html(link)
   try:
      heading = soup.find("h1", {"class":"entry-title single-title"}).text
      print(heading)
   except:
      heading = None
   try:
      imgpath = soup.find('section', attrs={'id':'article-content'}).find('figure').find('img')['src']
      print(imgpath)
   except :
      imgpath = None
   try:
      summary = " ".join([p.text for p in soup.find('div', attrs={'id':'article-body'}).find_all('p')])
      print(summary)
   except:
      summary = None
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }
'''
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
'''
if __name__ =="__main__":
   get_proxy()
   #soup = get_soup_html('https://asiancorrespondent.com/section/countries/india/')           
   #get_asiaCorr_news_links(soup,'lol')
   get_news_data('https://asiancorrespondent.com/2019/12/two-dead-in-india-as-police-fire-at-demo-against-citizenship-bill/')