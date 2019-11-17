#!/usr/bin/env python
# coding: utf-8

# In[16]:


from collector_utils import *
from urllib.request import urlopen
import requests


# In[19]:


# get the list of html pages
pdir = '/Users/macbook/Desktop/Lev/Sapienza/ADM_Labs/HW3/data_html/'
movies = []
for d, dirs, files in os.walk(pdir):
    for f in files:
        movies.append("file:///Users/macbook/Desktop/Lev/Sapienza/ADM_Labs/HW3/data_html/" + f)


# In[3]:


movies_url = "https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html"
movies_response = requests.get(movies_url)

movies_soup = BeautifulSoup(movies_response.text, 'html.parser')
lst_movies = movies_soup.select("a")
lst_urls = []
for movie in range(0,len(lst_movies)):
    lst_urls.append(lst_movies[movie].get("href")) # get all links of the movies


# In[ ]:


# prepare the dict for scrapping all informations
d = {"title":"","intro":"","plot":"","film_name" : "","Directed by" : "","Produced by" : "","Written by" : "","Starring" : "" ,"Music by" : "", 
     "Release date" : "","Running time" : "","Country": "","Language" : "","Budget" : "","clean_intro":"",
    "clean_plot":"","url":""}
for key,value in d.items():
    if d[key] == "":
        d[key] = "NA"
# vocab = "" # during the extracting information i want to create the vocabulary
for path in movies:
    lost_pages = []
    try:
        movie_soup = re_fr_dir(path) # take the movie
        doc = info(movie_soup,d) # take information
    except:
        lost_pages.append(path) # catch the expectations
    for key,value in doc.items():
        doc[key] = re.sub(r'\n', r"",doc[key]) # from every info block i want to delete the \n and \t
        doc[key] = re.sub(r'\t', r"",doc[key]) # from every info block i want to delete the \n and \t
    doc["Release date"] = unicodedata.normalize("NFKD", doc["Release date"]) # normilize the time
    doc["clean_intro"] = remov_stop_w_and_p_stemm(doc["intro"]) # create the clean intro and plot
    doc["clean_plot"] = remov_stop_w_and_p_stemm(doc["plot"])
#     vocab = vocab + " " + doc["clean_intro"] + " " + doc["clean_plot"] # creating the vocabulary
    doc["url"] = str(lst_urls[int(re.findall(r'\d+',re.findall(r'article_.+',path)[0])[0])])
    file_name = "/Users/macbook/Desktop/Lev/Sapienza/ADM_Labs/HW3/data_tsv/" + re.findall(r'article_.+\.',path)[0] + "tsv"
    # save the tsv file
    with open(file_name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = list(doc.keys()), dialect = "excel-tab")
        writer.writeheader()
        f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % tuple(doc.values()))
        
    
    
    with open(file_name, "w",encoding="utf-8") as f: 
        f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % tuple(doc.values()))

   

