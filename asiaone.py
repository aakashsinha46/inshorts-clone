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
            
   for item in news:
      soup = get_soup_html(item['link'])
      heading = soup.find("h1", attrs={"class": "ui header page__title"}).text  #heading
      p = soup.find("div", attrs={"class": "field field-name-field-image"})
      q = p.find("div", attrs={"class": "content"})
      r = q.find("img", attrs={"class": "img-responsive"})
      imgPath = r['src']  # image path
      g = soup.find("div", attrs={
      "class": "field field-name-body field--type-text-with-summary field--label-hidden field-item"})
      summary = " ".join([p.text for p in g.find_all("p", limit=2)])  #summary
      item.update({
         'title' : heading,
         'desc' : summary,
         'image' : 'https://www.asiaone.com{image}'.format(image=imgPath)
      })
     
   print(news)  # mai debug kiya hai


if __name__ == "__main__":
    html = get_soup_html("https://www.asiaone.com/showbiz")
    get_showbiz_news(html)

