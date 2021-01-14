#!/usr/bin/env python
# coding: utf-8

# # 1 数据概况分析

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
red=pd.read_csv(r'/Users/muriellai/Downloads/week2.redbook.csv')


# In[2]:


red.info()


# In[3]:


red.head()


# In[4]:


red['gender']=red['gender'].fillna('unknown')


# In[5]:


red.age.describe()


# In[6]:


red['age']=red['age'].fillna(red.age.mean())


# In[7]:


red.engaged_last_30.describe()


# In[8]:


red['engaged_last_30']=red['engaged_last_30'].fillna(0)


# In[9]:


red.info()


# In[10]:


red=pd.get_dummies(red)


# In[11]:


red.head(10)


# In[12]:


red.info()


# # 2 单变量分析

# 数字型变量

# In[22]:


red.previous_order_amount.describe()


# In[23]:


red.age.describe()


# In[25]:


red.engaged_last_30.describe()


# In[35]:


#red. days_since_last_order .describe()


# In[36]:


red.groupby(['age'])['revenue'].describe()


# In[43]:


red.groupby(['3rd_party_stores'])['revenue'].describe()


# In[44]:


red.groupby(['lifecycle_A'])['revenue'].describe()


# In[45]:


red.groupby(['lifecycle_B'])['revenue'].describe()


# In[46]:


red.groupby(['lifecycle_C'])['revenue'].describe()


# # 3 相关与可视化分析

# In[13]:


red.corr()[['revenue']].sort_values('revenue',ascending=False)


# In[47]:


sns.regplot('previous_order_amount','revenue',red)


# In[48]:


sns.regplot('engaged_last_30','revenue',red)


# In[49]:


sns.regplot(' days_since_last_order ','revenue',red)


# # 4 线性回归模型建立

# In[50]:


# 调用sklearn中的线性回归工具包
from sklearn.linear_model import LinearRegression
# LinearRegression()设置模型为线性回归
model=LinearRegression()
# 设定自变量和因变量
y=red['revenue']
x=red[['previous_order_amount','engaged_last_30',' days_since_last_order ']]


# In[51]:


model.fit(x,y)


# In[52]:


model.coef_


# In[53]:


model.intercept_


# In[54]:


score=model.score(x,y)#x和y打分
predictions=model.predict(x)#计算y预测值
error=predictions-y#计算误差
rmse=(error**2).mean()**.5#计算rmse
mae=abs(error).mean()#计算mae
print(rmse)
print(mae)


# In[56]:


from statsmodels.formula.api import ols
x=red[['previous_order_amount','engaged_last_30',' days_since_last_order ']]
y=red['revenue']
model=ols('y~x',red).fit()
print(model.summary())


# # 5 线性回归模型优化

# In[67]:


from sklearn.linear_model import LinearRegression
model=LinearRegression()
y=red['revenue']
x=red[['previous_order_amount','engaged_last_30',' days_since_last_order ','age']]
model.fit(x,y)


# In[68]:


model.coef_


# In[69]:


model.intercept_


# In[70]:


score=model.score(x,y)#x和y打分
predictions=model.predict(x)#计算y预测值
error=predictions-y#计算误差
rmse=(error**2).mean()**.5#计算rmse
mae=abs(error).mean()#计算mae
print(rmse)
print(mae)


# In[71]:


from statsmodels.formula.api import ols
x=red[['previous_order_amount','engaged_last_30',' days_since_last_order ','age']]
y=red['revenue']
model=ols('y~x',red).fit()
print(model.summary())

