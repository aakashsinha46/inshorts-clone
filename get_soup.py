import requests
from bs4 import BeautifulSoup as bs

def get_soup_html(url=None):
        if url is not None:
                url_response = requests.get(url)
                soup = bs(url_response.content, 'html.parser')
                return soup

