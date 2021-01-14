#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


unique=pd.read_csv(r'/Users/muriellai/Downloads/zuoyeweek1.unique.csv')


# In[3]:


unique.info()


# In[4]:


unique.head()


# In[5]:


unique.describe()


# In[6]:


unique.drop('store_id', axis=1, inplace=True)


# In[7]:


unique.describe()


# In[8]:


unique.gender_group.value_counts()


# In[9]:


unique.age_group.value_counts()


# In[10]:


unique.revenue.value_counts()


# In[11]:


unique.revenue.describe()


# 问题一：整体销售情况随着时间的变化是怎样的？？

# In[12]:


unique=unique[unique['revenue']>=0]


# In[13]:


unique.revenue.value_counts()
unique.groupby(['wkd_ind'])['revenue'].describe()


# In[14]:


bins=[0,70,200,12538]
labels=['low','normal','high']
unique['revenue_new']=pd.cut(unique.revenue,bins,right=False,labels=labels)


# In[15]:


unique.groupby(['revenue_new'])['revenue'].describe()


# In[16]:


plt.figure(figsize=(10,8))
sns.countplot(y='wkd_ind', hue='revenue_new',data=unique)
plt.tick_params(labelsize=15)


# 问题二：不同产品的销售情况是怎样的？

# In[17]:


import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[18]:


unique=pd.read_csv(r'/Users/muriellai/Downloads/zuoyeweek1.unique.csv')


# In[19]:


bins=[0,70,200,12538]
labels=['low','normal','high']
unique['revenue_new']=pd.cut(unique.revenue,bins,right=False,labels=labels)


# In[29]:


plt.figure(figsize=(10,10))
sns.countplot(y='product', hue='revenue_new',data=unique, order=unique['product'].value_counts().index)
plt.rcParams['font.sans-serif']=['Arial Unicode MS']
plt.rcParams['axes.unicode_minus']=False
plt.tick_params(labelsize=15)


# 问题三：顾客偏爱哪一种购买方式？

# In[21]:


unique.channel.value_counts()


# In[22]:


unique.age_group.value_counts()


# In[24]:


plt.figure(figsize=(10,10))
sns.countplot(y='age_group', hue='channel',data=unique, order=unique['age_group'].value_counts().index)
plt.tick_params(labelsize=15)


# In[27]:


plt.figure(figsize=(8, 8))
sns.countplot(x='gender_group', hue='channel',data=unique, order=unique['gender_group'].value_counts().index)
plt.tick_params(labelsize=15)


# In[28]:


plt.figure(figsize=(8, 8))
sns.countplot(y='city', hue='channel',data=unique, order=unique['city'].value_counts().index)
plt.tick_params(labelsize=15)


# 问题四：销售额和产品成本之间的关系怎么样？

# In[31]:


unique['sales']=unique['unit_price']*unique['quant']


# In[35]:


unique['cost']=unique['unit_cost']*unique['quant']


# In[34]:


unique.sales.describe()


# In[36]:


unique.cost.describe()


# In[37]:


q=['sales','cost']
b=unique[q].corr()


# In[38]:


sns.heatmap(b.corr())

