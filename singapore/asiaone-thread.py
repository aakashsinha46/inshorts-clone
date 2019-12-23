from get_soup import get_soup_html
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import sleep
from decorators import time_taken

CATEGORY = ['showbiz', 'digital', 'lifestyle', 'health']
MAX_WORKER = 5
news_links = {}
prepared_links = {}

def get_asiaone_news_link(soup, category):
   link1 =[link['href']for item in soup.find_all("div", attrs={"class": "content overlay"})  for link in item.find_all('a', href=True) ]
      
   link2 = [innerlink['href'] for item in soup.find_all("div", attrs={"class": "card col-xs-12 col-sm-4"}) for link in item.find_all("div", attrs={"class": "content"}) for innerlink in link.find_all('a', href=True) ]

   links = link1 + link2
   news_links[category] = links

def get_news_data(link):
   soup = get_soup_html(link)
   heading = soup.find("h1", attrs={"class": "ui header page__title"}).text #heading
   
   p = soup.find("div", attrs={"class": "field field-name-field-image"})
   q = p.find("div", attrs={"class": "content"})
   r = q.find("img", attrs={"class": "img-responsive"})
   imgPath = r['src']  # image path

   g = soup.find("div", attrs={"class": "field field-name-body field--type-text-with-summary field--label-hidden field-item"})
   summary = " ".join([p.text for p in g.select('p')])  #summary
   return {
      'image' : 'https://www.asiaone.com{image}'.format(image=imgPath),
      'heading' : heading,
      'desc' : summary,
      'link' : link      
   }
     
def get_soup(category:None):
   return get_soup_html("https://www.asiaone.com/{link}".format(link=category))

@time_taken
def main():
   #threading
   
   with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
      #submit to pool object 
      pool = [ executor.submit(get_asiaone_news_link, get_soup(value), value) for key,value in enumerate(CATEGORY) ]
      #on complete
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
   
   with open( 'asiaone_output.json', 'w') as f:           #the output at asiaone_output.json
      f.write(json.dumps(prepared_links))
   
if __name__ == "__main__":
   main()
      

   
