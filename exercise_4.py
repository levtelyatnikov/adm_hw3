#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import itertools
def MaxLengthPalindrome(S):
    combosList  = list(itertools.chain.from_iterable([list(itertools.combinations(S,i)) for i in range(1,len(S))])) #list form
    combosString = [''.join(c) for c in combosList]  #string form of every possibile subsequence 
    chk=0
    longest=0
    for sub in combosString:     #for every subsequence
            for k in range(len(sub)):   
                if(sub[k]==sub[len(sub)-1-k]): #we test if first element is equal to last element(second with second-last and so on)
                    chk+=1
                    if(chk==len(sub)):  #if true we found a palindrome
                        if(len(sub)>longest): 
                            longest=len(sub)   #we save the longest
                else:
                    chk=0
                    break
    return print('The longest Palindrome subsequence is %s ' %longest)


# In[ ]:


print("Input string")
s = input().lower()
MaxLengthPalindrome(s)


# In[ ]:




