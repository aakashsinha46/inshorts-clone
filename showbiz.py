from get_soup import get_soup_html
import pprint

def get_showbiz_news(soup=None):
   news = []
   for item in soup.find_all("div", attrs={"class": "content overlay"}):
      for link in item.find_all('a', href=True):
         news.append({
            'link':link['href'],
            'title':link.string
         })

   for item in soup.find_all("div", attrs={"class": "card col-xs-12 col-sm-4"}):
      for link in item.find_all("div", attrs={"class": "content"}):
         for innerlink in link.find_all('a', href=True):
            news.append({
               'link':innerlink['href'],
               'title':innerlink.string
            })
   for n in news[{'link'}]:
      print(n)
   pprint.pprint(news)

if __name__ == "__main__":
    html = get_soup_html("https://www.asiaone.com/showbiz")
    get_showbiz_news(html)