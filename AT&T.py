#!/usr/bin/env python
# coding: utf-8
# 导入工具包
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# 加载数据
churn=pd.read_csv(r'/Users/muriellai/Downloads/w4_churn.csv')
churn.info()
churn.head()

# 将数据集中的类别变量转化为数字型变量
churn=pd.get_dummies(churn)
#查看前5行数据
churn.head()

#数据整理，将churn_yes保留，将female保留,drop不需要的数据
churn.drop(['Churn_No','gender_Male'],axis=1,inplace=True)
#查看数据
churn.head()

#统一大小写 
churn.columns=churn.columns.str.lower()
#修改字段名 
churn=churn.rename(columns={'churn_yes':'flag'})
#查看数据
churn.head()

churn.head(10)
churn.flag.value_counts()
churn.flag.value_counts(1)

summary=churn.groupby('flag') # 赋值summary为以flag进行分组分析的数据
summary.mean() # 查看各变量在flag的0/1分组下所占的比例的差别

sns.countplot(y='contract_month',hue='flag',data=churn) # y设置为需要查看的变量
sns.countplot(y='internet_other',hue='flag',data=churn)
sns.countplot(y='gender_female',hue='flag',data=churn)

churn.corr()[['flag']].sort_values('flag',ascending=False)

#拓展学习：用热力图呈现各自变量与flag的相关关系
q1=['flag','contract_month','internet_other','totalcharges']
sns.heatmap(churn[q1].corr())

y=churn['flag']
x=churn[['contract_month','internet_other','paymentelectronic']]

# 加载数据切分工具包
from sklearn.model_selection import train_test_split
# 切分训练集和测试集
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.5,random_state=100)

from sklearn import linear_model
lr=linear_model.LogisticRegression()
lr.fit(x_train,y_train)

lr.intercept_

lr.coef_

#基于模型的结果，对训练集与测试集中x的真实值预测对应的y
y_pred_train=lr.predict(x_train)
y_pred_test=lr.predict(x_test)
print(y_pred_train)

#搭建训练集混淆矩阵
import sklearn.metrics as metrics
metrics.confusion_matrix(y_train,y_pred_train)
#计算训练集准确率
metrics.accuracy_score(y_train,y_pred_train)

#搭建测试集混淆矩阵
metrics.confusion_matrix(y_test,y_pred_test)
#计算测试集准确率
metrics.accuracy_score(y_test,y_pred_test)

#训练集模型评估
from sklearn.metrics import classification_report
print(classification_report(y_train, y_pred_train))

#测试集模型评估
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred_test))
