from get_soup import get_soup_html
import pprint
import string

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
   #pprint.pprint(news)
   for item in news:
      soup = get_soup_html(item['link'])
      heading = (soup.find("h1", attrs={"class": "ui header page__title"})).text

      p = soup.find("div", attrs={"class": "field field-name-field-image"})
      q = p.find("div", attrs={"class": "content"})
      r = q.find("img", attrs={"class": "img-responsive"})

      imgPath = r['src']  # image path

      k = ""
      g = soup.find("div", attrs={
         "class": "field field-name-body field--type-text-with-summary field--label-hidden field-item"})
      k = " ".join([p.text for p in g.find_all("p", limit=2)])
      # for item2 in g.find_all("p")[:2]:
      #    k = k + item2.text

      item.update({'imgPath': 'https://www.asiaone.com'+imgPath})
      item.update({'title': heading})
      item.update({'desc': k})
   pprint.pprint(news)


if __name__ == "__main__":
    html = get_soup_html("https://www.asiaone.com/showbiz")
    get_showbiz_news(html)


'''html_tags = soup.find_all('p')
for h in html_tags:
    print(h.text.strip())  
    '''