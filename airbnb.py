#!/usr/bin/env python
# coding: utf-8

# In[1]:


#调包
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
#数据导入
airbnb=pd.read_csv(r'/Users/muriellai/Downloads/w3_airbnb.csv')


# In[2]:


#查看数据类型
airbnb.info()
#用户数据具体情况
airbnb.head()


# In[3]:


airbnb.describe()


# In[4]:


#把年龄限制在18到80岁之间
airbnb=airbnb[airbnb['age']<=80]
airbnb=airbnb[airbnb['age']>=18]
airbnb.age.describe()#查看年龄的描述性指标


# In[5]:


# 生成衍生变量 - 用户注册至今的时间
# 第一步，将注册日期转变为日期时间格式
airbnb['date_account_created']=pd.to_datetime(airbnb['date_account_created'])
airbnb.info()
#发现data_account_created变量格式从object转变为datetime64
#第二步，将年份从中提取出来，将2019-注册日期的年份，并生成一个新的变量year_since_account_created
airbnb['year_since_account_created']=airbnb['date_account_created'].apply(lambda x:2019-x.year)
#发现注册时间最短的是5年，最长的是9年
airbnb.year_since_account_created.describe()


# In[6]:


# 生成衍生变量 - 用户第一次预定至今的时间
#第一步将用户第一次预定时间转变为日期时间格式
airbnb['date_first_booking']=pd.to_datetime(airbnb['date_first_booking'])
#第二步，将年份从中提取出来，将2019-第一次注册的年份，并生成一个新的变量year_since_first_booking  
airbnb['year_since_first_booking']=airbnb['date_first_booking'].apply(lambda x:2019-x.year)
#发现距离第一次预定时间最短的是4年，最长的是9年
airbnb.year_since_first_booking.describe()


# In[7]:


#删除两个日期变量，可以根据数据格式来进行drop
airbnb.drop(airbnb.select_dtypes(['datetime64']),inplace=True,axis=1)


# In[8]:


#将类别型型转化成哑变量
airbnb=pd.get_dummies(airbnb)


# In[9]:


airbnb.info()


# In[11]:


airbnb.head()


# In[12]:


airbnb.describe()


# In[22]:


airbnb_5=airbnb[['year_since_first_booking','web','moweb','ios','android']]


# In[23]:


from sklearn.preprocessing import scale
x=pd.DataFrame(scale(airbnb_5))


# In[30]:


from sklearn import cluster
model=cluster.KMeans(n_clusters=5,random_state=10)
model.fit(x)


# In[31]:


airbnb_5['cluster']=model.labels_
airbnb_5.head(20)#查看模型前20行数据


# In[32]:


airbnb_5.groupby(['cluster'])['year_since_first_booking'].describe()#查看age的分群效果


# In[33]:


airbnb_5.groupby(['cluster'])['ios'].describe()#查看ios的分群效果


# In[34]:


from sklearn import metrics#调用sklearn的metrics库
x_cluster=model.fit_predict(x)#个体与群的距离
score=metrics.silhouette_score(x,x_cluster)#评分越高，个体与群越近；评分越低，个体与群越远
print(score)


# In[38]:


#导出结果到csv文件，以分为3组为例
centers=pd.DataFrame(model.cluster_centers_)
centers.to_csv(r'/Users/muriellai/Downloads/center_3.csv')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




