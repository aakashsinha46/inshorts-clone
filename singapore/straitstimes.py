import sys
sys.path.insert(0,'../')
from proxy_get_soup import get_soup_html, get_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken
import pprint

MAX_WORKER = 5
news_links = {}
prepared_links = {}
CATEGORY = {"politics":'politics/latest', "business":'business/latest', "lifestyle":'lifestyle/latest', "entertainment":'lifestyle/entertainment', "sports":'sport/latest', "technology":'tech/latest'}

def get_straitstimes_link(soup, category):
   main = soup.find("div", {"class": "panel-pane"})
   heads = main.find_all('div', {'class':'media'})
   links = [ format_article(head) for head in heads]
   news_links[category] = set(links)
   links.clear()
   
def format_article(head):
   #title = head.find('h3', {'class':'story-title'}).text.strip()
   link = head.find('a')['href']
   link = 'https://www.straitstimes.com{link}'.format(link=link)
   return link

def get_news_data(link):
   soup = get_soup_html(link)
   try:
      title = soup.find('h1',attrs={'class':"headline node-title"}).text
   except:
      title = None
   try:
      imgpath = soup.find('img',{'class':'img-responsive'})['src']  
   except:
      imgpath = "None"
   try:
      path = soup.find('div',{'class':'odd field-item'})
      summary = " ".join(p.text for p in path.find_all('p'))
   except:
      summary = "None"
   return {
      'heading' : title,
      'image' : imgpath,
      'desc' : summary,
      'link' : link     
   }

def get_soup(category :None):
   soup = get_soup_html("https://www.straitstimes.com/{link}".format(link=category))
   return soup

@time_taken
def main():
   #threading
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      #submit to pool object 
      pool = [ executor.submit(get_straitstimes_link, get_soup(value), key) for key,value in CATEGORY.items() ]
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
   
   with open( 'straitstimes.json', 'w') as f:           #the output at asiaone_output.json
      f.write(json.dumps(prepared_links))

if __name__ == "__main__":
   get_proxy()
   main()
