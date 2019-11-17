#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collector_utils import *

movies_url = "https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html"
movies_response = requests.get(movies_url)

movies_soup = BeautifulSoup(movies_response.text, 'html.parser')
lst_movies = movies_soup.select("a")
lst_urls = []
for movie in range(0,len(lst_movies)):
    lst_urls.append(lst_movies[movie].get("href")) # get all links of the movies


# In[ ]:


# save the pages
for i in range(len(lst_urls)) :
    save_html(lst_urls[i],"/Users/macbook/Desktop/Lev/Sapienza/ADM_Labs/HW3/data_html/" + "article_" + str(i))
    if i%10 == 0:
        time.sleep(int(rm.uniform(1, 5)))    

