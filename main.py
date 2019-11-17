#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
import json
import pandas as pd
import re
import numpy as np
import heapq 
import json
from utils import *
# functions for 1-st engine
def jsonKeys2int(x):
    if isinstance(x, dict):
            return {int(k):v for k,v in x.items()}
    return x
def query_upload():
    stop_words = set(stopwords.words("english"))
    tok = RegexpTokenizer(r"\w+")
    porter = PorterStemmer()
    query = tok.tokenize(input()) # take the query and we need to split and stemm it as we sptlited vocab
    query_words = list(map(porter.stem,query)) 
    words = filter(lambda x: x not in string.punctuation, query_words)
    cleaned_query = filter(lambda x: x not in stop_words, words)
    return cleaned_query
def term_query(words,vocabulary):
    res = []
    for i in range(len(words)):
        res.append(int(vocabulary[words[i]]))
    return res
def output_search_engine_1(paths):
    if len(paths) > 1:
        return pd.concat([pd.read_csv(path,sep = "\t", index_col = False,encoding='utf-8')[["title","intro","url"]] for path in paths]).reset_index(drop = True)
    else:
        return pd.concat([pd.read_csv(path,sep = "\t", index_col = False,encoding='utf-8')[["title","intro","url"]] for path in paths[:1]]).reset_index(drop = True)
    return res
def Seqrch_Engine1(query,inver_in):
    docs = []
    for term in query:
        docs.append(inver_in[term])
    for i in range(len(docs)): # from list to sets
        docs[i] = set(docs[i])
    res  = docs[0].intersection(*[i for i in docs[:]])
    if len(res) != 0 :
        paths = []
        for i in res:
            paths.append("/Users/macbook/Desktop/Lev/Sapienza/ADM_Labs/HW3/data_tsv/article_" + str(i) + ".tsv")
        output = output_search_engine_1(paths)
        
        return output_search_engine_1(paths)
            
    else:
        return print("There is not any movie with ALL whis words")
    return res

#functions for 2-nd engine

def quiery_tdidf(q,idf):
    q_td_idf = {}
    # idf = log2(number of document / number of doc consists the term key )
    for term in q:
        q_td_idf[term] = idf[term]/len(q) # quiery tdidf (td = 1/len(document))
    return q_td_idf 

def Search_engine_2_all_docs(query,vocabulary,idf,inv_in,doc_lenght):
    t_query = term_query(query,vocabulary) # take the words and create the string
    lenght_q = count_length(t_query,idf,len(t_query))
    q_td_idf = quiery_tdidf(t_query,term_idf)
    terms_in_docs = []
    cossim = {}
    d = {}
    for term in t_query:
        terms_in_docs.append((term,inv_in[term]))
    
    for info in terms_in_docs:
        term = info[0]
        for doc_tdidf in info[1]:
            if doc_tdidf[0] in d.keys(): 
                d[doc_tdidf[0]].append(doc_tdidf[1] * q_td_idf[term])
            elif doc_tdidf[0] not in d.keys():
                d[doc_tdidf[0]] = []
                d[doc_tdidf[0]].append(doc_tdidf[1] * q_td_idf[term])
        for num_doc in d.keys():
            cossim[str(num_doc)] = sum(d[num_doc])/(doc_lenght[num_doc]*lenght_q ) # count the cosSim

    return cossim

# this function works like first search engine but the output is the list of documents which conteins all words from the quaery
def find_all_docs_consist_all_quiery(query,inver_in):
    docs = []
    for term in query:
        docs.append(inver_in[term])
    #print(docs)
    for i in range(len(docs)): # from list to sets
        docs[i] = set(docs[i])
    res  = docs[0].intersection(*[i for i in docs[:]])
    if len(res) != 0 :
        paths = []
        for i in res:
            paths.append("/Users/macbook/Desktop/Lev/Sapienza/ADM_Labs/HW3/data_tsv/article_" + str(i) + ".tsv")
        return paths
            
    else:
        return [] # if there if not such documents
    return res
# Search engine 2
def Search_engine_2(query,vocabulary,idf,inv_in,paths_doc,doc_lenght):
    terms_in_docs = []
    cossim = {}
    d = {}
    for key in paths_doc:
        d[int(re.findall(r'\d+',re.findall(r'article_.+',key)[0])[0])] = [] #prepare the dict of the documents which contains all words from the query
    # prepare the query    
    t_query = term_query(query,vocabulary) # take the words and create the string
    lenght_q = count_length(t_query,idf,len(t_query)) # count the norm of the query
    q_td_idf = quiery_tdidf(t_query,term_idf) # return tdidf query
    #prepare
    for term in t_query:
        terms_in_docs.append((term,inv_in[term])) #take the inverted index only for that terms which is in the query
    # take the term
    for info in terms_in_docs:
        term = info[0] # take the term
        for doc_tdidf in info[1]: #take the number of document
            if doc_tdidf[0] in d.keys(): # if the number of doc in the prepared list of documents which consists all words from the query
                d[doc_tdidf[0]].append(doc_tdidf[1] * q_td_idf[term]) # count the numerator cosine similarity

    for num_doc in d.keys():
        cossim[str(num_doc)] = sum(d[num_doc])/(doc_lenght[num_doc]*lenght_q ) # count the cosine simimilarity

    return cossim
# this function printing creating the top k movies
def output_search_engine(paths,top_k):
    if len(paths) > 1:
        a = pd.concat([pd.read_csv(path,sep = "\t", index_col = False)[["title","intro","url"]] for path in paths]).reset_index(drop = True)
        a['Similarity'] = top_k
        return a
    else:
        a = pd.concat([pd.read_csv(path,sep = "\t", index_col = False)[["title","intro","url"]] for path in paths]).reset_index(drop = True)
        a['Similarity'] = top_k
        return a
# this function use the HEAP structure to find the top k movies
def top_k(k,cossim):
    heap = [(value, key) for key,value in cossim.items()] # to do a heap from the dict we need as key the score of movies
    largest = heapq.nlargest(k, heap) #get top k movies 
    paths = []
    # take the paths of top k movies
    paths = ["/Users/macbook/Desktop/Lev/Sapienza/ADM_Labs/HW3/data_tsv/article_" + str(num_doc[1]) + ".tsv" for num_doc in largest]
    # print(paths)
    return output_search_engine(paths,[i for i,j in largest]) # print the top k movies
def count_length(terms,idf_ls,len_document):
    lenght = 0
    for term in terms:
        lenght += (idf_ls[term]/len_document)**2
    
    return np.sqrt(lenght)
def idf_3(Inv_in,number_of_documents):
    term_idf = {}
    # idf = log2(number of document / number of doc consists the term key )
    lost_words = []
    for key,values in Inv_in.items(): 
        try:
            term_idf[key] = math.log(1 + (number_of_documents/len(values)),10) # smoothing the tdidf score
        except:
            lost_words.append(key)
    return lost_words,term_idf





# In[ ]:


print("Choose the search engine (1,2,3)")
print("1 - will find all movies which contain the all words from the query")
print("2 - will find all movies which contain the all words from the query and will ranked ir in top 5 movies")
print("3 - will find all movies which contain the all words from the query and will ranked ir in top 5 movies with the 'smooth cosine similarity' and also include the title to the search parametr")
seqrch_engine = int(input())


# In[ ]:


if seqrch_engine == 1:
    vocabulary = {}
    with open('vocabulary.txt') as file:
        for line in file:
            value,key = line.split(":")
            vocabulary[key.strip("\n")] = value
    Inv_in = json.load(open('Inverted_index.json')) # as we can see now all key are str
    Inv_in = jsonKeys2int(Inv_in) # this finction solved the problem with string key
    print("Input the query")
    p = 0
    while p == 0:
        try:
            query = list(query_upload())
            t_query = term_query(query,vocabulary)
            p = 1 
        except: 
            print("Some words is not in the cocabulary, try again")
            print("For example try: space future world")
    print(Seqrch_Engine1(t_query,Inv_in).to_string())


# In[ ]:


if seqrch_engine == 2:
    vocabulary = {}
    with open('vocabulary.txt') as file:
        for line in file:
            value,key = line.split(":")
            vocabulary[key.strip("\n")] = value
    inv_ind2 = json.load(open('Inverted_index_2_1.json')) # as we can see now all key are str
    inv_ind2 = jsonKeys2int(inv_ind2) # this finction solved the problem with string key
    Inv_in = json.load(open('Inverted_index.json')) # as we can see now all key are str
    Inv_in = jsonKeys2int(Inv_in) # this finction solved the problem with string key
    for key in inv_ind2.keys(): # after uploading json all tuples became lists 
        for i in range(len(inv_ind2[key])):
            inv_ind2[key][i] = tuple(inv_ind2[key][i]) # turn back from lists to tuples
    for key in inv_ind2.keys():
        for i in range(len(inv_ind2[key])):
            inv_ind2[key][i] = tuple(inv_ind2[key][i])
    doc_lenght = json.load(open('doc_lenght.json')) # as we can see now all key are str
    doc_lenght = jsonKeys2int(doc_lenght)
    term_idf = json.load(open('idf_2_1.json'))
    term_idf = jsonKeys2int(term_idf)

    print("Input the query")
    p = 0
    while p == 0:
        try:
            query = list(query_upload()) #take the string and create the words
            t_query = term_query(query,vocabulary)
            p = 1
        except:
            print("Some words is not in the cocabulary, try again")
            print("For example try: film studio america first motion pictur industri base begin 20th centuri")
    paths_doc = find_all_docs_consist_all_quiery(t_query,Inv_in) # i use first search engine to find all documents which consist all quaery
    if len(paths_doc) == 0: # if there is not documents which contains all words from the query
        cossim = Search_engine_2_all_docs(query,vocabulary,term_idf,inv_ind2,doc_lenght) # this function will count the cossine similarity for all documents which consists at least one wod from the query
    else:
        cossim = Search_engine_2(query,vocabulary,term_idf,inv_ind2,paths_doc,doc_lenght)
    print("How many movies do you want to see (sorted by cosine similarity) : ")    
    k = int(input())
    print(top_k(k,cossim).to_string())


# In[ ]:


if seqrch_engine == 3:
    vocabulary = {}
    with open('vocabulary_search3.txt') as file:
        for line in file:
            value,key = line.split(":")
            vocabulary[key.strip("\n")] = value

    Inv_in = json.load(open('Inverted_index_3_1.json')) # as we can see now all key are str
    Inv_in = jsonKeys2int(Inv_in) # this finction solved the problem with string key
    term_idf = json.load(open('idf_3.json'))
    term_idf = jsonKeys2int(term_idf)
    inv_ind3 = json.load(open('Inverted_index_3.json')) # as we can see now all key are str
    inv_ind3 = jsonKeys2int(inv_ind2) # this finction solved the problem with string key
    for key in inv_ind3.keys(): # after uploading json all tuples became lists 
        for i in range(len(inv_ind3[key])):
            inv_ind3[key][i] = tuple(inv_ind3[key][i]) # turn back from lists to tuples
    for key in inv_ind3.keys():
        for i in range(len(inv_ind3[key])):
            inv_ind2[key][i] = tuple(inv_ind2[key][i])
    doc_lenght = json.load(open('doc_lenght_3.json')) # as we can see now all key are str
    doc_lenght = jsonKeys2int(doc_lenght)


    p = 0
    while p == 0:
        try:
            query = list(query_upload()) #take the string and create the words
            t_query = term_query(query,vocabulary)
            p = 1
        except:
            print("Some words is not in the cocabulary, try again")
            print("For example try: film studio america first motion pictur industri base begin 20th centuri")
    paths_doc = find_all_docs_consist_all_quiery(t_query,Inv_in) # i use first search engine to find all documents which consist all quaery
    if len(paths_doc) == 0: # if there is not documents which contains all words from the query
        cossim = Search_engine_2_all_docs(query,vocabulary,term_idf,inv_ind3,doc_lenght) # this function will count the cossine similarity for all documents which consists at least one wod from the query
    else:
        cossim = Search_engine_2(query,vocabulary,term_idf,inv_ind3,paths_doc,doc_lenght)


    print("How many movies do you want to see (sorted by cosine similarity) : ")    
    k = int(input())
    print(top_k(k,cossim).to_string())


# In[ ]:





# In[ ]:





# In[ ]:




