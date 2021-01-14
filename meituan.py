#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
meituan=pd.read_csv(r'/Users/muriellai/Downloads/meituan.csv')
meituan.info()


# In[7]:


meituan.head()


# In[8]:


#数据清洗
meituan = meituan.dropna(subset=["price"])
meituan['rating']=meituan['rating'].fillna(3)
meituan['comment']=meituan['comment'].fillna(0)


# In[ ]:





# In[9]:


#数据相关性分析
cols=['rating','comment','price']
meituan[cols].corr()


# In[10]:


#散点图可视化price与rating相关性
plt.figure(figsize=(10,8)) 
sns.scatterplot(x="price", y="rating", data=meituan)


# In[11]:


#将rating分组
bins=[3,3.5,4,4.5,5]
labels=['<=3.5','<=4',"<=4.5","<=5"]
meituan['rating2']=pd.cut(meituan.rating,bins,right=True,labels=labels)


# In[12]:


#箱线图
plt.figure(figsize=(10,5))
sns.boxplot(x='rating',y='cat',palette=sns.color_palette('pastel'),data=meituan)
plt.tick_params(labelsize=20)


# In[13]:


#计数柱状图不同美食品类的评分情况
sns.countplot(x="cat",hue='rating2',data=meituan)


# In[14]:


#柱状图不同美食品类的点评数量
sns.barplot(x="cat",y="comment",hue="rating2",data=meituan)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




