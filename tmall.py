#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
tmall=pd.read_csv(r'/Users/muriellai/Downloads/week3.tmall.csv')


# # 1 数据概况分析

# In[2]:


tmall.info()


# In[3]:


tmall.head()


# In[4]:


tmall=pd.get_dummies(tmall)
tmall.head()


# In[5]:


tmall.drop(['default_no','returned_no','loan_no','ID'],axis=1,inplace=True)
tmall.head()


# In[6]:


tmall=tmall.rename(columns={'coupon_ind':'flag'})
tmall.head(10)


# 
# # 2 单变量分析

# In[7]:


tmall.flag.value_counts(1)


# In[8]:


summary=tmall.groupby('flag')
summary.mean()


# In[9]:


sns.countplot(y='coupon_used_in_last_month', hue='flag', data=tmall)


# In[10]:


sns.countplot(y='returned_yes', hue='flag', data=tmall)


# In[11]:


sns.countplot(y='loan_yes', hue='flag', data=tmall)


# # 3 相关与可视化

# In[12]:


tmall.corr()[['flag']].sort_values('flag',ascending=False)


# In[36]:


q1=['flag','coupon_used_in_last_month','job_retired','returned_yes']
sns.heatmap(tmall[q1].corr())


# # 4 逻辑回归模型

# In[37]:


y=tmall['flag']
x=tmall[['coupon_used_in_last_month','job_retired','marital_single']]


# In[38]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=100)


# In[39]:


from sklearn import linear_model
lr=linear_model.LogisticRegression()
lr.fit(x_train,y_train)


# In[40]:


lr.intercept_


# In[41]:


lr.coef_


# In[42]:


y_pred_train=lr.predict(x_train)
y_pred_test=lr.predict(x_test)
print(y_pred_train)


# In[43]:


import sklearn.metrics as metrics
metrics.confusion_matrix(y_train,y_pred_train)
metrics.accuracy_score(y_train,y_pred_train)


# In[44]:


metrics.confusion_matrix(y_test,y_pred_test)
metrics.accuracy_score(y_test,y_pred_test)


# In[45]:


from sklearn.metrics import classification_report
print(classification_report(y_train, y_pred_train))


# In[46]:


from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred_test))


# 4.1 调整参数-优化模型

# In[47]:


y=tmall['flag']
x=tmall[['coupon_used_in_last_month','job_retired','marital_single']]


# In[48]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.5,random_state=100)


# In[49]:


from sklearn import linear_model
lr=linear_model.LogisticRegression()
lr.fit(x_train,y_train)


# In[50]:


lr.intercept_


# In[51]:


lr.coef_


# In[52]:


y_pred_train=lr.predict(x_train)
y_pred_test=lr.predict(x_test)
print(y_pred_train)


# In[53]:


import sklearn.metrics as metrics
metrics.confusion_matrix(y_train,y_pred_train)
metrics.accuracy_score(y_train,y_pred_train)


# In[54]:


metrics.confusion_matrix(y_test,y_pred_test)
metrics.accuracy_score(y_test,y_pred_test)


# 4.2 调整变量-优化模型

# In[55]:


y=tmall['flag']
x=tmall[['coupon_used_in_last_month','job_retired','returned_yes']]


# In[69]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.5,random_state=100)


# In[70]:


from sklearn import linear_model
lr=linear_model.LogisticRegression()
lr.fit(x_train,y_train)


# In[71]:


metrics.confusion_matrix(y_test,y_pred_test)
metrics.accuracy_score(y_test,y_pred_test)


# In[72]:


import sklearn.metrics as metrics
metrics.confusion_matrix(y_train,y_pred_train)
metrics.accuracy_score(y_train,y_pred_train)


# # 5 对模型系数的业务解读

# In[73]:


#coupon_used_in_last_month: 上个月使用了优惠劵再次使用优惠券的概率是上个月没使用优惠券的1.41倍


# In[74]:


#job_retired：退休的客户使用优惠券的概率是其他工作客户的2.96倍


# In[ ]:


#marital_single：单身的客户使用优惠券的概率是结婚、离婚客户的1.47倍

