from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from urllib.error import HTTPError, URLError
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup as bs
import time
import logging
from socket import timeout
import requests

ua = UserAgent()
proxies = []
proxy_index = 0
proxies_deleted = 0

def get_proxy():
   # Retrieve latest proxies
   proxies_req = Request('https://www.sslproxies.org/')
   proxies_req.add_header('User-Agent', ua.random)
   proxies_doc = urlopen(proxies_req).read().decode('utf8')
   soup = bs(proxies_doc, 'html.parser')
   proxies_table = soup.find(id='proxylisttable')
   # Save proxies in the array
   for row in proxies_table.tbody.find_all('tr'):
      proxies.append({
       'ip':   row.find_all('td')[0].string,
       'port': row.find_all('td')[1].string
      })
   #Choose a random proxy
def random_proxy():
    proxy_index = random.randint(0, len(proxies) - 1)
    return proxy_index


def get_soup_html(url=None):
    if url is not None:
        while(True):
            try:
                req = requests.get(url,headers={'User-Agent': 'Mozilla/ 5.0'},proxies=proxies[proxy_index], timeout=5)
                soup = bs(req.content, 'html.parser')
                print('good')
                return soup
            except requests.exceptions.Timeout as error:
                print(error)
                print("bad")
                random_proxy()
                proxy = proxies[proxy_index]
                del proxies[proxy_index]
                global proxies_deleted
                proxies_deleted = proxies_deleted + 1
                print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
                random_proxy()
                proxy = proxies[proxy_index]

                if proxies_deleted == 40:
                    print("recalling of get_proxy to get new ip and ports")
                    get_proxy()

