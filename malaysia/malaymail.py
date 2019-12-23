from proxy_get_soup import get_soup_html, get_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken
import pprint

CATEGORY = ['showbiz', 'sports', 'tech-gadgets', 'money', 'life']
MAX_WORKER = 5
news_links = {}
prepared_links = {}

def get_malaymail_news_link(soup, category):
   links = [item2.find('a')['href'] for item in soup.find_all("div", attrs={"class":"content"}) for item2 in item.find_all("li")]
   for index, item in enumerate(links):
      if item.find("https://www.malaymail.com"):
         print("Not found ", item) # find and replace with concatnation
         link = "https://www.malaymail.com{item}".format(item=item)
         links[index] = link
   news_links[category] = links
   
def get_news_data(link):
   soup = get_soup_html(link)
   heading = soup.find("h1").text #heading
   #print(heading)
   imgPath = soup.find("figure").find('img')['src'] # image path
   #print(imgPath)
   summary = " ".join([p.text for p in soup.find("div",attrs={"class":"col-12 col-md-7 col-lg-8 primary"}).select('article >p')]) 
   #print(summary)
   return {
      'image' : imgPath,
      'heading' : heading,
      'desc' : summary,
      'link' : link      
   }

def get_soup(category :None):
   return get_soup_html("https://www.malaymail.com/news/{link}".format(link=category))

@time_taken
def main():
   #threading
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      #submit to pool object 
      pool = [ executor.submit(get_malaymail_news_link, get_soup(value), value) for key,value in enumerate(CATEGORY) ]
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
   
   with open( 'proxy_asiaone_output.json', 'w') as f:           #the output at asiaone_output.json
      f.write(json.dumps(prepared_links))

if __name__ == "__main__":
    get_proxy()
    main()
      

   
