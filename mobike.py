
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
mobike=pd.read_csv(r'/Users/muriellai/Downloads/week4.mobike.csv')


# # 1 数据概况分析

mobike.info()

mobike.describe()

mobike.head()


# # 2 单变量分析

mobike.drop(['Unnamed: 0','user_id','from_station_id','to_station_id','bikeid'],inplace=True,axis=1)

mobike.head()

mobike.gender.value_counts()

mobike.dropna(inplace=True)

mobike.info()

mobike.birthyear.describe()

mobike=mobike[mobike['birthyear']>=1960]

mobike['start_time']=pd.to_datetime(mobike['start_time'])
mobike.info()

mobike['end_time']=pd.to_datetime(mobike['end_time'])
mobike.info()

mobike.drop(mobike.select_dtypes(['datetime64']),inplace=True,axis=1)

mobike=pd.get_dummies(mobike)

mobike.info()

mobike.head()


# # 3 聚类分析模型

mobike.describe()

mobike_5=mobike[['birthyear','timeduration','tripduration','gender_Male','from_station_name_900 W Harrison St']]

from sklearn.preprocessing import scale
x=pd.DataFrame(scale(mobike_5))


from sklearn import cluster
model=cluster.KMeans(n_clusters=3,random_state=10)
model.fit(x)

mobike_5['cluster']=model.labels_
mobike_5.head(20)#查看模型前20行数据

mobike_5.groupby(['cluster'])['birthyear'].describe()

mobike_5.groupby(['cluster'])['tripduration'].describe()

from sklearn import metrics
x_cluster=model.fit_predict(x)
score=metrics.silhouette_score(x,x_cluster)
print(score)


#调整变量

mobike_5=mobike[['birthyear','timeduration','tripduration','gender_Male','usertype_Subscriber']]

from sklearn.preprocessing import scale
x=pd.DataFrame(scale(mobike_5))

from sklearn import cluster
model=cluster.KMeans(n_clusters=3,random_state=10)
model.fit(x)

mobike_5['cluster']=model.labels_
mobike_5.head(20)

mobike_5.groupby(['cluster'])['tripduration'].describe()

from sklearn import metrics
x_cluster=model.fit_predict(x)
score=metrics.silhouette_score(x,x_cluster)
print(score)

#调整群数
mobike_5=mobike[['birthyear','timeduration','tripduration','gender_Male','usertype_Subscriber']]

from sklearn.preprocessing import scale
x=pd.DataFrame(scale(mobike_5))

from sklearn import cluster
model=cluster.KMeans(n_clusters=2,random_state=10)
model.fit(x)

mobike_5['cluster']=model.labels_

mobike_5.groupby(['cluster'])['tripduration'].describe()


from sklearn import metrics
x_cluster=model.fit_predict(x)
score=metrics.silhouette_score(x,x_cluster)
print(score)


# # 4 模型的业务解读

centers=pd.DataFrame(model.cluster_centers_)
centers.to_csv(r'/Users/muriellai/Downloads/center_5.csv')

#一类为特别抗拒订阅下载摩拜用户
#另一类无显著特点

