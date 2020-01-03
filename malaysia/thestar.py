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
CATEGORY = ['category/leisure/health/','home-sports/', 'category/business/local-business/']



def get_news_data(link):
   soup = get_soup_html(link)

   try:
      heading = (soup.find("div", attrs={"class":"headline story-pg"})).find('h1').text
   except:
      heading = None  
   try: 
      imgpath = soup.find('meta',{'itemprop':"image"})['content']
   except :
      imgpath = None  
   try:
      g = soup.find('div',attrs={'id':"story-body"})
      summary = " ".join(p.text for p in g.select_all('p'))
   except:
      summary = None
   print(summary)
   
if __name__ == "__main__":
   get_proxy()
   get_news_data('https://www.thestar.com.my/news/education/2019/12/21/numed-makes-a-difference?utm_medium=thestar&utm_source=secpmnewslisting&utm_campaign=20191221_Newcastle')
