
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

unique=pd.read_csv(r'/Users/muriellai/Downloads/zuoyeweek1.unique.csv')

unique.info()

unique.head()

unique.describe()

unique.drop('store_id', axis=1, inplace=True)

unique.describe()

unique.gender_group.value_counts()

unique.age_group.value_counts()

unique.revenue.value_counts()

unique.revenue.describe()


# 问题一：整体销售情况随着时间的变化是怎样的？？
unique=unique[unique['revenue']>=0]

unique.revenue.value_counts()
unique.groupby(['wkd_ind'])['revenue'].describe()

bins=[0,70,200,12538]
labels=['low','normal','high']
unique['revenue_new']=pd.cut(unique.revenue,bins,right=False,labels=labels)

unique.groupby(['revenue_new'])['revenue'].describe()

plt.figure(figsize=(10,8))
sns.countplot(y='wkd_ind', hue='revenue_new',data=unique)
plt.tick_params(labelsize=15)


# 问题二：不同产品的销售情况是怎样的？

import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

unique=pd.read_csv(r'/Users/muriellai/Downloads/zuoyeweek1.unique.csv')

bins=[0,70,200,12538]
labels=['low','normal','high']
unique['revenue_new']=pd.cut(unique.revenue,bins,right=False,labels=labels)

plt.figure(figsize=(10,10))
sns.countplot(y='product', hue='revenue_new',data=unique, order=unique['product'].value_counts().index)
plt.rcParams['font.sans-serif']=['Arial Unicode MS']
plt.rcParams['axes.unicode_minus']=False
plt.tick_params(labelsize=15)


# 问题三：顾客偏爱哪一种购买方式？

unique.channel.value_counts()

unique.age_group.value_counts()

plt.figure(figsize=(10,10))
sns.countplot(y='age_group', hue='channel',data=unique, order=unique['age_group'].value_counts().index)
plt.tick_params(labelsize=15)

plt.figure(figsize=(8, 8))
sns.countplot(x='gender_group', hue='channel',data=unique, order=unique['gender_group'].value_counts().index)
plt.tick_params(labelsize=15)

plt.figure(figsize=(8, 8))
sns.countplot(y='city', hue='channel',data=unique, order=unique['city'].value_counts().index)
plt.tick_params(labelsize=15)


# 问题四：销售额和产品成本之间的关系怎么样？

unique['sales']=unique['unit_price']*unique['quant']

unique['cost']=unique['unit_cost']*unique['quant']

unique.sales.describe()

unique.cost.describe()

q=['sales','cost']
b=unique[q].corr()

sns.heatmap(b.corr())
