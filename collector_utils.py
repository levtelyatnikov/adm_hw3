#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

def save_html(page, index):
    p = requests.get(str(page))
    with open( str(index) + ".html", "w" ) as fh:
        fh.write(p.text)
        
#path = "file:///Users/macbook/Desktop/Lev/Sapienza/ADM_Labs/HW3/data_html/article_9999.html"
def re_fr_dir(path):
    page = urlopen(path)
    movie_soup = BeautifulSoup(page.read().decode("utf-8"), 'html.parser')
    return movie_soup
#movie_soup = re_fr_dir(path)

