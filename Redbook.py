# 1 数据概况分析

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
red=pd.read_csv(r'/Users/muriellai/Downloads/week2.redbook.csv')

red.info()

red.head()

red['gender']=red['gender'].fillna('unknown')

red.age.describe()

red['age']=red['age'].fillna(red.age.mean())

red.engaged_last_30.describe()

red['engaged_last_30']=red['engaged_last_30'].fillna(0)

red.info()

red=pd.get_dummies(red)

red.head(10)

# # 2 单变量分析
# 数字型变量

red.previous_order_amount.describe()

red.age.describe()

red.engaged_last_30.describe()

#red. days_since_last_order .describe()

red.groupby(['age'])['revenue'].describe()

red.groupby(['3rd_party_stores'])['revenue'].describe()

red.groupby(['lifecycle_A'])['revenue'].describe()

red.groupby(['lifecycle_B'])['revenue'].describe()

red.groupby(['lifecycle_C'])['revenue'].describe()


# # 3 相关与可视化分析
red.corr()[['revenue']].sort_values('revenue',ascending=False)

sns.regplot('previous_order_amount','revenue',red)

sns.regplot('engaged_last_30','revenue',red)

sns.regplot(' days_since_last_order ','revenue',red)

# # 4 线性回归模型建立

# 调用sklearn中的线性回归工具包
from sklearn.linear_model import LinearRegression
# LinearRegression()设置模型为线性回归
model=LinearRegression()
# 设定自变量和因变量
y=red['revenue']
x=red[['previous_order_amount','engaged_last_30',' days_since_last_order ']]

model.fit(x,y)

model.coef_

model.intercept_

score=model.score(x,y)#x和y打分
predictions=model.predict(x)#计算y预测值
error=predictions-y#计算误差
rmse=(error**2).mean()**.5#计算rmse
mae=abs(error).mean()#计算mae
print(rmse)
print(mae)

from statsmodels.formula.api import ols
x=red[['previous_order_amount','engaged_last_30',' days_since_last_order ']]
y=red['revenue']
model=ols('y~x',red).fit()
print(model.summary())

# # 5 线性回归模型优化

from sklearn.linear_model import LinearRegression
model=LinearRegression()
y=red['revenue']
x=red[['previous_order_amount','engaged_last_30',' days_since_last_order ','age']]
model.fit(x,y)

model.coef_

model.intercept_

score=model.score(x,y)#x和y打分
predictions=model.predict(x)#计算y预测值
error=predictions-y#计算误差
rmse=(error**2).mean()**.5#计算rmse
mae=abs(error).mean()#计算mae
print(rmse)
print(mae)

from statsmodels.formula.api import ols
x=red[['previous_order_amount','engaged_last_30',' days_since_last_order ','age']]
y=red['revenue']
model=ols('y~x',red).fit()
print(model.summary())
