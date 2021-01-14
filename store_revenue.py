#!/usr/bin/env python
# coding: utf-8

# In[1]:


#调包
import pandas as pd


# In[6]:


# 读取数据
store=pd.read_csv(r'/Users/muriellai/Downloads/w2_store_rev.csv' )


# In[7]:


store.describe()


# In[9]:


store.drop('Unnamed: 0', axis=1, inplace=True)


# In[10]:


store.describe()


# In[12]:


# 查看数据信息
store.info()


# In[13]:


# 统计数据空值
store.isnull().sum()


# In[14]:


store.head(10)


# In[15]:


#了解event的具体值
store.event.unique()


# In[16]:


#这些类别对应的revenue(销售额)是怎样的
store.groupby(['event'])['revenue'].describe()


# In[17]:


#这几个类别对应的local_tv（本地电视广告投入）是怎样的
store.groupby(['event'])['local_tv'].describe()


# In[18]:


#将类别变量转化为哑变量
store=pd.get_dummies(store)


# In[19]:


# 查看生成event的4个标签，每个标签取值0/1
store.head(10)


# In[20]:


#确认类别变量已经转换成数字变量
store.info()


# In[21]:


# 查看所有变量彼此间的相关性
store.corr()


# In[22]:


# 仅查看所有变量与revenue的相关性，同时根据相关性做降序排列展示
store.corr()[['revenue']].sort_values('revenue',ascending=False)


# In[23]:


import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[24]:


# 对local_tv变量进行线性关系可视化分析
sns.regplot('local_tv','revenue',store)


# In[25]:


# 对person变量进行线性关系可视化分析
sns.regplot('person','revenue',store)


# In[26]:


# 对instore变量进行线性关系可视化分析
sns.regplot('instore','revenue',store)


# In[28]:


sns.regplot('online','revenue',store)


# In[29]:


sns.regplot('reach','revenue',store)


# In[31]:


# 调用sklearn中的线性回归工具包
from sklearn.linear_model import LinearRegression
# LinearRegression()设置模型为线性回归
model=LinearRegression()
# 设定自变量和因变量
y=store['revenue']
x=store[['local_tv','person','instore']]


# In[38]:


# 缺失值填充
#store=store.fillna(0)
store=store.fillna(store.local_tv.mean())


# In[33]:


# 查看是否填充完毕
store.info()


# In[41]:


# 重新加载填充完的X变量
x=store[['local_tv','person','instore','online']]
# 重新训练模型
model.fit(x,y)


# In[42]:


# 查看自变量系数
model.coef_


# In[43]:


# 查看截距
model.intercept_


# In[37]:


#模型的评估,x为'local_tv','person','instore'
score=model.score(x,y)#x和y打分
predictions=model.predict(x)#计算y预测值
error=predictions-y#计算误差
rmse=(error**2).mean()**.5#计算rmse
mae=abs(error).mean()#计算mae
print(rmse)
print(mae)


# In[44]:


#模型的评估,x为'local_tv','person','instore'
score=model.score(x,y)#x和y打分
predictions=model.predict(x)#计算y预测值
error=predictions-y#计算误差
rmse=(error**2).mean()**.5#计算rmse
mae=abs(error).mean()#计算mae
print(rmse)
print(mae)


# In[45]:


# 查看标准的模型输出表
from statsmodels.formula.api import ols
x=store[['local_tv','person','instore']] 
y=store['revenue']
model=ols('y~x',store).fit()
print(model.summary())


# 

# In[ ]:





# In[ ]:




