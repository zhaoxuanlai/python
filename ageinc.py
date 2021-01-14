#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
ageinc_df=pd.read_csv(r'/Users/muriellai/Downloads/w3_ageinc.csv')
ageinc_df.info()
ageinc_df.describe()


# In[5]:


#（收入-收入均值）/收入标准差
ageinc_df['z_income']=(ageinc_df['income']-ageinc_df['income'].mean())/ageinc_df['income'].std()
#（年龄-年龄均值）/年龄标准差
ageinc_df['z_age']=(ageinc_df['age']-ageinc_df['age'].mean())/ageinc_df['age'].std()
# 查看数据分布
ageinc_df.describe()


# In[6]:


#初步进行数据可视化
sns.scatterplot(x='income',y='age',data=ageinc_df)


# In[9]:


#导入sklearn中的cluster
from sklearn import cluster
#将群体分成3层
model=cluster.KMeans(n_clusters=2,random_state=10)
#用标准化的收入与年龄来拟合模型
model.fit(ageinc_df[['z_income','z_age']])
#为用户打上标签
ageinc_df['cluster']=model.labels_
#查看用户的分群情况
ageinc_df.head(50)


# In[10]:


sns.scatterplot(x='age',y='income',hue='cluster',data=ageinc_df)
#横轴为年龄，纵轴为收入，分类为用户分群标签


# In[11]:


#导入sklearn中的cluster
from sklearn import cluster
#将群体分成6层
model=cluster.KMeans(n_clusters=6,random_state=10)
#用标准化的收入与年龄来拟合模型
model.fit(ageinc_df[['z_income','z_age']])
#为用户打上标签
ageinc_df['cluster']=model.labels_
#分群效果可视化
sns.scatterplot(x='age',y='income',hue='cluster',data=ageinc_df)


# In[12]:


#使用groupby函数，将用户按照所在群分组，统计收入的数据
ageinc_df.groupby(['cluster'])['income'].describe()


# In[13]:


#使用groupby函数，将用户按照所在群分组，统计年龄的数据
ageinc_df.groupby(['cluster'])['age'].describe()


# In[ ]:





# In[ ]:





# In[ ]:




