from get_soup import get_soup_html
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken

CATEGORY = ['parliament/', 'tech/', 'lifestyle/', 'lifestyle/celebrity/']
MAX_WORKER = 5
news_links = {}
prepared_links = {}

# categorise links
def get_mothership_news_links(soup, category):
   links = [item.find('a')['href'] for item in soup.find_all("div", attrs={"class": "ind-article"})[1:]]
   news_links[category]=links

def get_news_data(link):
   soup = get_soup_html(link)
   imgpath = (soup.find("figure", attrs={
               "class": "featured-image"})).find("img")['src']  # image path
   # heading
   heading = (
         soup.find("div", attrs={"id": "article-original"})).find("h1").text
   summary = " ".join(p.text for p in soup.select('div.content-article-wrap > p'))
   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return get_soup_html("https://mothership.sg/category/{link}".format(link=category))

@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_mothership_news_links, get_soup(value), value) for key,value in enumerate(CATEGORY) ]
      # on complete
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
   
   with open('mothership_output.json', 'w') as f:          #the output at mothership_output.json
      f.write(json.dumps(prepared_links))     
   

if __name__ == "__main__":
   main()
