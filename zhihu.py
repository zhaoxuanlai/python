#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
zhihu=pd.read_csv(r'/Users/muriellai/Downloads/zhihu.csv')
zhihu.info()


# In[2]:


zhihu.head()


# In[3]:


#数据清洗
zhihu = zhihu.dropna(subset=["agreement"])
zhihu['comment']=zhihu['comment'].fillna(0)
zhihu['introduction']=zhihu['introduction'].fillna('null')


# In[4]:


zhihu['agreement'].apply(lambda x: float(x))


# In[5]:


zhihu['comment'].apply(lambda x: float(x))


# In[6]:


zhihu.head()


# In[7]:


zhihu['introduction']=pd.get_dummies(zhihu['introduction'])


# In[8]:


zhihu.head()


# In[9]:


#数据相关性
cols=['agreement','comment','introduction']
zhihu[cols].corr()


# In[10]:


plt.figure(figsize=(5,4)) 
sns.scatterplot(x="comment", y="agreement", data=zhihu)


# In[11]:


#结论：用户回答获得点赞数与评论数存在一定的正相关关系，即用户回答的评论数越多，点赞数越高


# In[12]:


sns.barplot(x="comment", y="agreement",hue="introduction",data=zhihu)


# In[13]:


#结论：自我介绍与数码相关的用户获得评论及点赞更多

