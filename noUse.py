from showbiz import news
from get_soup import get_soup_html
n = news
print(n)

'''
r = requests.get(url)
soup = bs(r.content, 'html.parser')

heading = (soup.find("h1", attrs={"class": "ui header page__title"})).text  #mainheading

p = soup.find("div", attrs={"class": "field field-name-field-image"})
q = p.find("div", attrs={"class": "content"})
r = q.find("img", attrs={"class": "img-responsive"})

imgPath = r['src'] #image path

g = soup.find("div", attrs={"class": "field field-name-body field--type-text-with-summary field--label-hidden field-item"})
for item in g.find_all("p"):
	print(item.text)  # description
'''