import requests
from bs4 import BeautifulSoup as bs

url = "https://www.asiaone.com/entertainment/tamara-ecclestone-has-had-75-million-worth-jewellery-stolen"
r = requests.get(url)
soup = bs(r.content, 'html.parser')

heading = (soup.find("h1", attrs={"class": "ui header page__title"})).text  #mainheading

p = soup.find("div", attrs={"class": "field field-name-field-image"})
q = p.find("div", attrs={"class": "content"})
r = q.find("img", attrs={"class": "img-responsive"})

imgPath = r['src'] #image path

g = soup.find("div", attrs={"class": "field field-name-body field--type-text-with-summary field--label-hidden field-item"})
print(g)

