from get_soup import get_soup_html
from threading import Thread
import pprint

def get_mothership_news_links(soup=None):
   news = []
   for item in soup.find_all("div", attrs={"class": "ind-article"})[1:]:
      news.append({'link': item.find('a')['href']})
   #get_mothership_news(news)
   t2 = Thread(target=get_mothership_news, args=(news,)) 
   t2.start()
   t2.join()
   print(news)
 
def get_mothership_news(news=None):
   for item in news:
      soup = get_soup_html(item['link'])

      imgpath = (soup.find("figure", attrs={"class" : "featured-image"})).find("img")['src'] #image path

      heading = (soup.find("div", attrs={"id": "article-original"})).find("h1").text #heading
     
      summary = " ".join(p.text for p in soup.select('div.content-article-wrap > p')) #summary
   
      item.update({
      'image': imgpath,
      'heading': heading,
      'desc' : summary
      })

if __name__ == "__main__":
   categorys_on_mothership = ['parliament/', 'tech/', 'lifestyle/', 'lifestyle/celebrity/']
   for category in categorys_on_mothership:
      html = get_soup_html("https://mothership.sg/category/{link}".format(link=category))
      #get_mothership_news_links(html)
      t1 = Thread(target=get_mothership_news_links, args=(html,)) 
      t1.start() 
   