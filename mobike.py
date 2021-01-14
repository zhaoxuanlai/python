#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
mobike=pd.read_csv(r'/Users/muriellai/Downloads/week4.mobike.csv')


# # 1 数据概况分析

# In[2]:


mobike.info()


# In[3]:


mobike.describe()


# In[4]:


mobike.head()


# # 2 单变量分析

# In[5]:


mobike.drop(['Unnamed: 0','user_id','from_station_id','to_station_id','bikeid'],inplace=True,axis=1)


# In[6]:


mobike.head()


# In[7]:


mobike.gender.value_counts()


# In[8]:


mobike.dropna(inplace=True)


# In[9]:


mobike.info()


# In[10]:


mobike.birthyear.describe()


# In[11]:


mobike=mobike[mobike['birthyear']>=1960]


# In[12]:


mobike['start_time']=pd.to_datetime(mobike['start_time'])
mobike.info()


# In[13]:


mobike['end_time']=pd.to_datetime(mobike['end_time'])
mobike.info()


# In[14]:


mobike.drop(mobike.select_dtypes(['datetime64']),inplace=True,axis=1)


# In[15]:


mobike=pd.get_dummies(mobike)


# In[16]:


mobike.info()


# In[17]:


mobike.head()


# # 3 聚类分析模型

# In[18]:


mobike.describe()


# In[19]:


mobike_5=mobike[['birthyear','timeduration','tripduration','gender_Male','from_station_name_900 W Harrison St']]


# In[20]:


from sklearn.preprocessing import scale
x=pd.DataFrame(scale(mobike_5))


# In[21]:


from sklearn import cluster
model=cluster.KMeans(n_clusters=3,random_state=10)
model.fit(x)


# In[22]:


mobike_5['cluster']=model.labels_
mobike_5.head(20)#查看模型前20行数据


# In[23]:


mobike_5.groupby(['cluster'])['birthyear'].describe()


# In[24]:


mobike_5.groupby(['cluster'])['tripduration'].describe()


# In[25]:


from sklearn import metrics
x_cluster=model.fit_predict(x)
score=metrics.silhouette_score(x,x_cluster)
print(score)


# In[26]:


#调整变量


# In[27]:


mobike_5=mobike[['birthyear','timeduration','tripduration','gender_Male','usertype_Subscriber']]


# In[28]:


from sklearn.preprocessing import scale
x=pd.DataFrame(scale(mobike_5))


# In[29]:


from sklearn import cluster
model=cluster.KMeans(n_clusters=3,random_state=10)
model.fit(x)


# In[30]:


mobike_5['cluster']=model.labels_
mobike_5.head(20)


# In[31]:


mobike_5.groupby(['cluster'])['tripduration'].describe()


# In[32]:


from sklearn import metrics
x_cluster=model.fit_predict(x)
score=metrics.silhouette_score(x,x_cluster)
print(score)


# In[33]:


#调整群数


# In[34]:


mobike_5=mobike[['birthyear','timeduration','tripduration','gender_Male','usertype_Subscriber']]


# In[35]:


from sklearn.preprocessing import scale
x=pd.DataFrame(scale(mobike_5))


# In[36]:


from sklearn import cluster
model=cluster.KMeans(n_clusters=2,random_state=10)
model.fit(x)


# In[37]:


mobike_5['cluster']=model.labels_


# In[38]:


mobike_5.groupby(['cluster'])['tripduration'].describe()


# In[39]:


from sklearn import metrics
x_cluster=model.fit_predict(x)
score=metrics.silhouette_score(x,x_cluster)
print(score)


# # 4 模型的业务解读

# In[40]:


centers=pd.DataFrame(model.cluster_centers_)
centers.to_csv(r'/Users/muriellai/Downloads/center_5.csv')


# In[ ]:


#一类为特别抗拒订阅下载摩拜用户
#另一类无显著特点

