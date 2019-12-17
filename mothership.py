from get_soup import get_soup_html
import pprint

def get_mothership_politics_news(soup=None):
   news = []
   for item in soup.find_all("div", attrs={"class": "ind-article"})[1:]:
      news.append({'link': item.find('a')['href']})
   
   for item in news:
      soup = get_soup_html(item['link'])

      imgpath = (soup.find("figure", attrs={"class" : "featured-image"})).find("img")['src'] #image path

      heading = (soup.find("div", attrs={"id": "article-original"})).find("h1").text #heading

      para = soup.find("div", attrs={"class": "content-article-wrap"})
      for f in para.find_all("p")
         summary = " ".join(f.text)

      item.update({
      'image': imgpath,
      'heading': heading
      })
  
   pprint.pprint(news)

if __name__ == "__main__":
   html = get_soup_html("https://mothership.sg/category/parliament/")
   get_mothership_politics_news(html)
