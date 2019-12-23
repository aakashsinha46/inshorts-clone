from proxy_get_soup import get_soup_html,get_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken

MAX_WORKER = 5
news_links = {}
prepared_links = {}
CATEGORY = ['sports', 'news/business','lifestyle/fashion']

# categorise links
def get_tnp_news_links(soup, category):
   links = [item.find('a')['href'] for item in soup.find_all("h2", attrs={"class": "card-title"})]
   news_links[category]=links
   
def get_news_data(link):
   soup = get_soup_html(link)
   #print((soup.find('figure')).find('a')['href'])
   #imgpath = (soup.select('figure >a'))['href']
   if soup.find('figure',attrs={'class':'group-media-frame field-group-html-element'})is not None:
      imgpath = (soup.find('figure',attrs={'class':'group-media-frame field-group-html-element'})).find('img')['src']
   else:
      imgpath = None

   #imgpath = soup.select('figure > a')['href']  # image path
   # heading
   heading = (soup.find("h1", attrs={'class':'story-headline'})).text
   
   summary =  " ".join(p.text for p in soup.select('div.body-copy > p'))

   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }
   
def get_soup(category:None):
   return get_soup_html("https://www.tnp.sg/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_tnp_news_links, get_soup(value), value) for key,value in enumerate(CATEGORY) ]
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
   
   with open('tnp_output.json', 'w') as f:          #the output at independent_output.json
      f.write(json.dumps(prepared_links))     
   

if __name__ == "__main__":
   get_proxy()
   main()
