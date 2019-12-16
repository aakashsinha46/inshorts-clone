import requests
from bs4 import BeautifulSoup as bs

asiaone = "https://www.asiaone.com/showbiz"
r = requests.get(asiaone)
#print(r.content)
soup = bs(r.content, 'html.parser')
#print(soup.prettify())


for item in soup.find_all("div", attrs={"class": "content overlay"}):
    for link in item.find_all('a', href=True):
        print(link['href'])


for item in soup.find_all("div", attrs={"class": "card col-xs-12 col-sm-4"}):
    for link in item.find_all("div", attrs={"class": "content"}):
        for innerlink in link.find_all('a', href=True):
            print(innerlink['href'])