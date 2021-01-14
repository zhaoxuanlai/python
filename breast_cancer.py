#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 导入pandas与numpy工具包。
import pandas as pd
import numpy as np
# 创建特征列表。
column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']
# 使用pandas.read_csv函数从互联网读取指定数据。
data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data', names = column_names )


# In[2]:


data.head()


# In[5]:


# 数据量和维度
data.shape


# In[6]:


# 将?替换为标准缺失值表示。
data = data.replace(to_replace='?', value=np.nan)

# 丢弃带有缺失值的数据（只要有一个维度有缺失）。
data = data.dropna(how='any')

# 输出data的数据量和维度。
data.shape


# In[7]:


data.shape
data[column_names[1:10]].head() # 只看第2到10列，省略了对第一列ID的查看


# In[10]:


# 随机采样25%的数据用于测试，剩下的75%用于构建训练集合。
X_train, X_test, y_train, y_test = train_test_split(data[column_names[1:10]], 
#特征：第0列id去掉,第10列分类结果去掉
  data[column_names[10]],#第10列的分类结果作为目标分类变量 
  test_size=0.25, 
  random_state=33)


# In[11]:


y_train.value_counts()


# In[12]:


y_test.value_counts()


# In[13]:


# 从sklearn.preprocessing里导入StandardScaler。
from sklearn.preprocessing import StandardScaler
# 从sklearn.linear_model里导入LogisticRegression
from sklearn.linear_model import LogisticRegression


# In[14]:


# 标准化数据，保证每个维度的特征数据方差为1，均值为0。使得预测结果不会被某些维度过大的特征值而主导。
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)


# In[15]:


#调用Lr中的fit模块训练型参数
lr = LogisticRegression()
lr.fit(X_train, y_train)
lr_y_predict = lr.predict(X_test)

#评估训练效果——从Sklearn导入分类报告；
from sklearn.metrics import classification_report
print(classification_report(y_test, lr_y_predict, target_names=['Benign', 'Malignant']))

#使用逻辑回归自带评分函数获得模型预测正确的百分比
print('Accuracy of LR Classifier:', lr.score(X_test, y_test))


# In[ ]:





# In[ ]:





# In[ ]:





# In[3]:


#原操作 会报错
# 使用sklearn.cross_valiation里的train_test_split模块用于分割数据。
from sklearn.cross_validation import train_test_split


# In[4]:


#新操作
# 使用sklearn.model_selection里的train_test_split模块用于分割数据。
from sklearn.model_selection import train_test_split

