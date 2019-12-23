from get_soup_with_js import return_soup
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken

MAX_WORKER = 5
news_links = {}
prepared_links = {}
CATEGORY = ['sport', 'lifestyle']

# categorise links
def get_straitstimes_news_links(soup, category):
   links = [item['href'] for item in soup.find_all('a', attrs={"class" : "block-link"})]
   final_link = [ "https://www.straitstimes.com{link}".format(link=item) for item in links]
   news_links[category] = final_link
   get_news_data(news_links)
   #print(news_links)
   #print(news_links)

def get_news_data(link):
   soup = return_soup(l for l in link)
   #print((soup.find('figure')).find('a')['href'])
   #imgpath = (soup.select('figure >a'))['href']
   if soup.find_all('picture', attrs={'class': 'img-responsive'}) is not None:
      imgpath = ((soup.find('img'))['href'])
   else:
      imgpath = None

   #imgpath = soup.select('figure > a')['href']  # image path
   # heading
   heading = (soup.find("h1", attrs={"class":"tdb-title-text"})).text
   
   summary =  " ".join(p.text for items in soup.find_all("div", attrs={"class" : "tdb-block-inner td-fix-index"}) for p in items.find_all("p"))

   return {
          'image': imgpath,
          'heading': heading,
          'desc': summary,
          'link':link
   }

def get_soup(category:None):
   return return_soup("https://www.straitstimes.com/{link}".format(link=category))

def main():
   r = get_soup('sport')

   get_straitstimes_news_links(r, 'sport')
   s = get_soup('lifestyle')
   get_straitstimes_news_links(s, 'lifestyle')
   #print("pop")
'''
@time_taken
def main():
   # threadpool
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      # submit to pool object
      pool = [ executor.submit(get_straitstimes_news_links, get_soup(value), value) for key,value in enumerate(CATEGORY) ]
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
   print(prepared_links)
   with open('the_straitstimes_output.json', 'w') as f:          #the output at straitstimes_output.json
      f.write(json.dumps(prepared_links))     
   
'''
if __name__ == "__main__":
   #get_proxy()
   main()
