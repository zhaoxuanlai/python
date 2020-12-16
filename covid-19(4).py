# -*- coding: utf-8 -*-

__author__ = 'yuzhengxing'
__date__ = '2020/7/8 23:18'

import numpy as np
import pandas as pd
import pycountry_convert as pc
import pyecharts.options as opts
from pyecharts.charts import Scatter3D, Line, Polar

# Retriving Dataset
df_confirmed = pd.read_csv("time_series_covid19_confirmed_global.csv")
df_deaths = pd.read_csv("time_series_covid19_deaths_global.csv")

# Depricated
df_covid19 = pd.read_csv("cases_country.csv")
df_table = pd.read_csv("cases_time.csv",
                       parse_dates=['Last_Update'])

# new dataset
df_covid19 = df_covid19.drop(["People_Tested", "People_Hospitalized", "UID", "ISO3", "Mortality_Rate"], axis=1)
df_covid19.head(2)

df_confirmed = df_confirmed.rename(columns={"Province/State": "state", "Country/Region": "country"})
df_deaths = df_deaths.rename(columns={"Province/State": "state", "Country/Region": "country"})
df_covid19 = df_covid19.rename(columns={"Country_Region": "country"})
df_covid19["Active"] = df_covid19["Confirmed"] - df_covid19["Recovered"] - df_covid19["Deaths"]

# Changing the conuntry names as required by pycountry_convert Lib
df_confirmed.loc[df_confirmed['country'] == "US", "country"] = "USA"
df_deaths.loc[df_deaths['country'] == "US", "country"] = "USA"
df_covid19.loc[df_covid19['country'] == "US", "country"] = "USA"
df_table.loc[df_table['Country_Region'] == "US", "Country_Region"] = "USA"

df_confirmed.loc[df_confirmed['country'] == 'Korea, South', "country"] = 'South Korea'
df_deaths.loc[df_deaths['country'] == 'Korea, South', "country"] = 'South Korea'
df_covid19.loc[df_covid19['country'] == "Korea, South", "country"] = "South Korea"
df_table.loc[df_table['Country_Region'] == "Korea, South", "Country_Region"] = "South Korea"
df_confirmed.loc[df_confirmed['country'] == 'Taiwan*', "country"] = 'Taiwan'
df_deaths.loc[df_deaths['country'] == 'Taiwan*', "country"] = 'Taiwan'
df_covid19.loc[df_covid19['country'] == "Taiwan*", "country"] = "Taiwan"
df_table.loc[df_table['Country_Region'] == "Taiwan*", "Country_Region"] = "Taiwan"

df_confirmed.loc[df_confirmed['country'] == 'Congo (Kinshasa)', "country"] = 'Democratic Republic of the Congo'
df_deaths.loc[df_deaths['country'] == 'Congo (Kinshasa)', "country"] = 'Democratic Republic of the Congo'
df_covid19.loc[df_covid19['country'] == "Congo (Kinshasa)", "country"] = "Democratic Republic of the Congo"
df_table.loc[df_table['Country_Region'] == "Congo (Kinshasa)", "Country_Region"] = "Democratic Republic of the Congo"

df_confirmed.loc[df_confirmed['country'] == "Cote d'Ivoire", "country"] = "Côte d'Ivoire"
df_deaths.loc[df_deaths['country'] == "Cote d'Ivoire", "country"] = "Côte d'Ivoire"
df_covid19.loc[df_covid19['country'] == "Cote d'Ivoire", "country"] = "Côte d'Ivoire"
df_table.loc[df_table['Country_Region'] == "Cote d'Ivoire", "Country_Region"] = "Côte d'Ivoire"

df_confirmed.loc[df_confirmed['country'] == "Reunion", "country"] = "Réunion"
df_deaths.loc[df_deaths['country'] == "Reunion", "country"] = "Réunion"
df_covid19.loc[df_covid19['country'] == "Reunion", "country"] = "Réunion"
df_table.loc[df_table['Country_Region'] == "Reunion", "Country_Region"] = "Réunion"

df_confirmed.loc[df_confirmed['country'] == 'Congo (Brazzaville)', "country"] = 'Republic of the Congo'
df_deaths.loc[df_deaths['country'] == 'Congo (Brazzaville)', "country"] = 'Republic of the Congo'
df_covid19.loc[df_covid19['country'] == "Congo (Brazzaville)", "country"] = "Republic of the Congo"
df_table.loc[df_table['Country_Region'] == "Congo (Brazzaville)", "Country_Region"] = "Republic of the Congo"

df_confirmed.loc[df_confirmed['country'] == 'Bahamas, The', "country"] = 'Bahamas'
df_deaths.loc[df_deaths['country'] == 'Bahamas, The', "country"] = 'Bahamas'
df_covid19.loc[df_covid19['country'] == "Bahamas, The", "country"] = "Bahamas"
df_table.loc[df_table['Country_Region'] == "Bahamas, The", "Country_Region"] = "Bahamas"

df_confirmed.loc[df_confirmed['country'] == 'Gambia, The', "country"] = 'Gambia'
df_deaths.loc[df_deaths['country'] == 'Gambia, The', "country"] = 'Gambia'
df_covid19.loc[df_covid19['country'] == "Gambia, The", "country"] = "Gambia"
df_table.loc[df_table['Country_Region'] == "Gambia", "Country_Region"] = "Gambia"

# getting all countries
countries = np.asarray(df_confirmed["country"])
countries1 = np.asarray(df_covid19["country"])

# Continent_code to Continent_names
continents = {
    'NA': 'North America',
    'SA': 'South America',
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe',
    'na': 'Others'
}


# Defininng Function for getting continent code for country.
def country_to_continent_code(country):
    try:
        return pc.country_alpha2_to_continent_code(pc.country_name_to_country_alpha2(country))
    except:
        return 'na'


# Collecting Continent Information
df_confirmed.insert(2, "continent", [continents[country_to_continent_code(country)] for country in countries[:]])
df_deaths.insert(2, "continent", [continents[country_to_continent_code(country)] for country in countries[:]])
df_covid19.insert(1, "continent", [continents[country_to_continent_code(country)] for country in countries1[:]])
df_table.insert(1, "continent",
                [continents[country_to_continent_code(country)] for country in df_table["Country_Region"].values])

df_countries_cases = df_covid19.copy().drop(['Lat', 'Long_', 'continent', 'Last_Update'], axis=1)
df_countries_cases.index = df_countries_cases["country"]
df_countries_cases = df_countries_cases.drop(['country'], axis=1)

df_continents_cases = df_covid19.copy().drop(['Lat', 'Long_', 'country', 'Last_Update'], axis=1)
df_continents_cases = df_continents_cases.groupby(["continent"]).sum()

df_countries_cases.fillna(0, inplace=True)
df_continents_cases.fillna(0, inplace=True)

df_continents_cases["Mortality Rate (per 100)"] = np.round(
    100 * df_continents_cases["Deaths"] / df_continents_cases["Confirmed"], 2)
df_continents_cases.style.background_gradient(cmap='Blues', subset=["Confirmed"]) \
    .background_gradient(cmap='Reds', subset=["Deaths"]) \
    .background_gradient(cmap='Greens', subset=["Recovered"]) \
    .background_gradient(cmap='Purples', subset=["Active"]) \
    .background_gradient(cmap='Pastel1_r', subset=["Incident_Rate"]) \
    .background_gradient(cmap='YlOrBr', subset=["Mortality Rate (per 100)"]) \
    .format("{:.2f}") \
    .format("{:.0f}", subset=["Confirmed", "Deaths", "Recovered", "Active"])
continents = {
    'NA': 'North America',
    'SA': 'South America',
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe',
    'na': 'Others'
}

ds = df_confirmed._stat_axis.values.tolist()  # 行名称
dc = df_confirmed.columns.values.tolist()[5:167]  # 列名称

# Confirmed
Confirmed = [int(confirmed) for confirmed in df_continents_cases['Confirmed'].tolist()]
Confirmed = sorted(Confirmed, reverse=False)
print(Confirmed)
sum_Confirmed = sum(Confirmed)
# Deaths
Deaths = [int(Deaths) for Deaths in df_continents_cases['Deaths'].tolist()]
# Deaths = [(d / c) * 100000 for d, c in zip(Deaths, Confirmed)]
Deaths = sorted(Deaths, reverse=False)
# print(Deaths)
sum_Deaths = sum(Deaths)

# Recovered
Recovered = [int(Recovered) for Recovered in df_continents_cases['Recovered'].tolist()]
# Recovered = [(r / c) * 1000 for r, c in zip(Recovered, Confirmed)]
Recovered = sorted(Recovered, reverse=False)
# print(Recovered)
sum_Recovered = sum(Recovered)

dcc = []
# 北美洲
dcc_NA = df_continents_cases.loc['North America'][:3]
dcc_na = [np.random.randint(int(d)) for d in dcc_NA.values]
North_America_x, North_America_y, North_America_z = dcc_na[0], dcc_na[1], dcc_na[2]
dcc.append([int(d) for d in dcc_NA.values])
# print(dcc_NA)
# 南美洲
dcc_SA = df_continents_cases.loc['South America'][:3]
dcc_sa = [np.random.randint(int(d)) for d in dcc_SA.values]
South_America_x, South_America_y, South_America_z = dcc_sa[0], dcc_sa[1], dcc_sa[2]
dcc.append([int(d) for d in dcc_SA.values])
# print(dcc_SA)
# 亚洲
dcc_AS = df_continents_cases.loc['Asia'][:3]
dcc_as = [np.random.randint(int(d)) for d in dcc_AS.values]
Asia_x, Asia_y, Asia_z = dcc_as[0], dcc_as[1], dcc_as[2]
dcc.append([int(d) for d in dcc_AS.values])
# print(dcc_AS)
# 澳洲
dcc_AU = df_continents_cases.loc['Australia'][:3]
dcc_au = [np.random.randint(int(d)) for d in dcc_AU.values]
Australia_x, Australia_y, Australia_z = dcc_au[0], dcc_au[1], dcc_au[2]
dcc.append([int(d) for d in dcc_AU.values])
# print(dcc_AU)
# 非洲
dcc_AF = df_continents_cases.loc['Africa'][:3]
dcc_af = [np.random.randint(int(d)) for d in dcc_AF.values]
Africa_x, Africa_y, Africa_z = dcc_af[0], dcc_af[1], dcc_af[2]
dcc.append([int(d) for d in dcc_AF.values])
# print(dcc_AF)
# 欧洲
dcc_EU = df_continents_cases.loc['Europe'][:3]
dcc_eu = [np.random.randint(int(d)) for d in dcc_EU.values]
Europe_x, Europe_y, Europe_z = dcc_eu[0], dcc_eu[1], dcc_eu[2]
dcc.append([int(d) for d in dcc_EU.values])
# print(dcc_EU)
# 其他洲
dcc_OT = df_continents_cases.loc['Others'][:3]
dcc_ot = [np.random.randint(int(d)) for d in dcc_OT.values]
Others_x, Others_y, Others_z = dcc_ot[0], dcc_ot[1], dcc_ot[2]
dcc.append([int(d) for d in dcc_OT.values])
# print(dcc_OT)

# 获取北美洲所有确诊数据行索引
dfc_North_America = df_confirmed[df_confirmed['continent'].str.contains('North America')]
# 获取确诊行索引
dic_list = []
dc_list = []
dc_new = []
na_list = []
for i in dfc_North_America.index:
    dic = {}
    na_list.append(df_confirmed.loc[i][5:].tolist())
    dic['one'] = sum(df_confirmed.loc[i][5:15])
    dic['two'] = sum(df_confirmed.loc[i][15:44])
    dic['three'] = sum(df_confirmed.loc[i][44:75])
    dic['four'] = sum(df_confirmed.loc[i][75:105])
    dic['five'] = sum(df_confirmed.loc[i][105:136])
    dic['six'] = sum(df_confirmed.loc[i][136:166])
    dic['seven'] = sum(df_confirmed.loc[i][166:])
    # 统计计算每天各大洲确诊病例数
    dic_list.append(df_confirmed.loc[i][5:].tolist())
dic_list = np.array(dic_list)
for i in range(168):
    dc_list.append(sum(dic_list[:, i]))
for i in range(167):
    dc_new.append(dc_list[i + 1] - dc_list[i])
# print('na', dc_list)
print('na', dc_new)
# dk = [i.keys() for i in dic_list][0]
# ds_North_America = [(k, sum([x[k] for x in dic_list])) for k in dk]
# ds_North_America = [v for v in dict(ds_North_America).values()]
# print("North_America", ds_North_America)

# 获取南美洲所有确诊数据行索引
dfc_South_America = df_confirmed[df_confirmed['continent'].str.contains('South America')]
# 获取确诊行索引
dic_list = []
dc_list = []
dc_new = []
sa_list = []
for i in dfc_South_America.index:
    dic = {}
    sa_list.append(df_confirmed.loc[i][5:].tolist())
    dic['one'] = sum(df_confirmed.loc[i][5:15])
    dic['two'] = sum(df_confirmed.loc[i][15:44])
    dic['three'] = sum(df_confirmed.loc[i][44:75])
    dic['four'] = sum(df_confirmed.loc[i][75:105])
    dic['five'] = sum(df_confirmed.loc[i][105:136])
    dic['six'] = sum(df_confirmed.loc[i][136:166])
    dic['seven'] = sum(df_confirmed.loc[i][166:])
    # 统计计算每天各大洲确诊病例数
    dic_list.append(df_confirmed.loc[i][5:].tolist())
dic_list = np.array(dic_list)
for i in range(167):
    dc_list.append(sum(dic_list[:, i]))
for i in range(166):
    dc_new.append(dc_list[i + 1] - dc_list[i])
# print('sa', dc_list)
print('sa', dc_new)

# dk = [i.keys() for i in dic_list][0]
# ds_South_America = [(k, sum([x[k] for x in dic_list])) for k in dk]
# ds_South_America = [v for v in dict(ds_South_America).values()]
# print("South_America", ds_South_America)

# 获取亚洲所有确诊数据行索引
dfc_Asia = df_confirmed[df_confirmed['continent'].str.contains('Asia')]
# 获取确诊行索引
dic_list = []
dc_list = []
dc_new = []
as_list = []
for i in dfc_Asia.index:
    dic = {}
    as_list.append(df_confirmed.loc[i][5:].tolist())
    dic['one'] = sum(df_confirmed.loc[i][5:15])
    dic['two'] = sum(df_confirmed.loc[i][15:44])
    dic['three'] = sum(df_confirmed.loc[i][44:75])
    dic['four'] = sum(df_confirmed.loc[i][75:105])
    dic['five'] = sum(df_confirmed.loc[i][105:136])
    dic['six'] = sum(df_confirmed.loc[i][136:166])
    dic['seven'] = sum(df_confirmed.loc[i][166:])
    # 统计计算每天各大洲确诊病例数
    dic_list.append(df_confirmed.loc[i][5:].tolist())
dic_list = np.array(dic_list)
for i in range(167):
    dc_list.append(sum(dic_list[:, i]))
for i in range(166):
    dc_new.append(dc_list[i + 1] - dc_list[i])
# print('as', dc_list)
print('as', dc_new)

# dk = [i.keys() for i in dic_list][0]
# ds_Asia = [(k, sum([x[k] for x in dic_list])) for k in dk]
# ds_Asia = [v for v in dict(ds_Asia).values()]
# print("Asia", ds_Asia)

# 获取澳洲所有确诊数据行索引
dfc_Australia = df_confirmed[df_confirmed['continent'].str.contains('Australia')]
# 获取确诊行索引
dic_list = []
dc_list = []
dc_new = []
au_list = []
for i in dfc_Australia.index:
    dic = {}
    au_list.append(df_confirmed.loc[i][5:].tolist())
    dic['one'] = sum(df_confirmed.loc[i][5:15])
    dic['two'] = sum(df_confirmed.loc[i][15:44])
    dic['three'] = sum(df_confirmed.loc[i][44:75])
    dic['four'] = sum(df_confirmed.loc[i][75:105])
    dic['five'] = sum(df_confirmed.loc[i][105:136])
    dic['six'] = sum(df_confirmed.loc[i][136:166])
    dic['seven'] = sum(df_confirmed.loc[i][166:])
    # 统计计算每天各大洲确诊病例数
    dic_list.append(df_confirmed.loc[i][5:].tolist())
dic_list = np.array(dic_list)
for i in range(167):
    dc_list.append(sum(dic_list[:, i]))
for i in range(166):
    dc_new.append(dc_list[i + 1] - dc_list[i])
# print('au', dc_list)
print('au', dc_new)

# dk = [i.keys() for i in dic_list][0]
# ds_Australia = [(k, sum([x[k] for x in dic_list])) for k in dk]
# ds_Australia = [v for v in dict(ds_Australia).values()]
# print("Australia", ds_Australia)

# 获取非洲所有确诊数据行索引
dfc_Africa = df_confirmed[df_confirmed['continent'].str.contains('Africa')]
# 获取确诊行索引
dic_list = []
dc_list = []
dc_new = []
af_list = []
for i in dfc_Africa.index:
    dic = {}
    af_list.append(df_confirmed.loc[i][5:].tolist())
    dic['one'] = sum(df_confirmed.loc[i][5:15])
    dic['two'] = sum(df_confirmed.loc[i][15:44])
    dic['three'] = sum(df_confirmed.loc[i][44:75])
    dic['four'] = sum(df_confirmed.loc[i][75:105])
    dic['five'] = sum(df_confirmed.loc[i][105:136])
    dic['six'] = sum(df_confirmed.loc[i][136:166])
    dic['seven'] = sum(df_confirmed.loc[i][166:])
    # 统计计算每天各大洲确诊病例数
    dic_list.append(df_confirmed.loc[i][5:].tolist())
dic_list = np.array(dic_list)
for i in range(167):
    dc_list.append(sum(dic_list[:, i]))
for i in range(166):
    dc_new.append(dc_list[i + 1] - dc_list[i])
# print('af', dc_list)
print('af', dc_new)

# dk = [i.keys() for i in dic_list][0]
# ds_Africa = [(k, sum([x[k] for x in dic_list])) for k in dk]
# ds_Africa = [v for v in dict(ds_Africa).values()]
# print("Africa", ds_Africa)

# 获取欧洲所有确诊数据行索引
dfc_Europe = df_confirmed[df_confirmed['continent'].str.contains('Europe')]
# 获取确诊行索引
dic_list = []
dc_list = []
dc_new = []
eu_list = []
for i in dfc_Europe.index:
    dic = {}
    eu_list.append(df_confirmed.loc[i][5:].tolist())
    dic['one'] = sum(df_confirmed.loc[i][5:15])
    dic['two'] = sum(df_confirmed.loc[i][15:44])
    dic['three'] = sum(df_confirmed.loc[i][44:75])
    dic['four'] = sum(df_confirmed.loc[i][75:105])
    dic['five'] = sum(df_confirmed.loc[i][105:136])
    dic['six'] = sum(df_confirmed.loc[i][136:166])
    dic['seven'] = sum(df_confirmed.loc[i][166:])
    # 统计计算每天各大洲确诊病例数
    dic_list.append(df_confirmed.loc[i][5:].tolist())
dic_list = np.array(dic_list)
for i in range(167):
    dc_list.append(sum(dic_list[:, i]))
for i in range(166):
    dc_new.append(dc_list[i + 1] - dc_list[i])
# print('eu', dc_list)
print('eu', dc_new)

# dk = [i.keys() for i in dic_list][0]
# ds_Europe = [(k, sum([x[k] for x in dic_list])) for k in dk]
# ds_Europe = [v for v in dict(ds_Europe).values()]
# print("Europe", ds_Europe)

# 获取其他洲所有确诊数据行索引
dfc_Others = df_confirmed[df_confirmed['continent'].str.contains('Others')]
# 获取确诊行索引
dic_list = []
dc_list = []
ot_list = []
dc_new = []
for i in dfc_Others.index:
    dic = {}
    ot_list.append(df_confirmed.loc[i][5:].tolist())
    dic['one'] = sum(df_confirmed.loc[i][5:15])
    dic['two'] = sum(df_confirmed.loc[i][15:44])
    dic['three'] = sum(df_confirmed.loc[i][44:75])
    dic['four'] = sum(df_confirmed.loc[i][75:105])
    dic['five'] = sum(df_confirmed.loc[i][105:136])
    dic['six'] = sum(df_confirmed.loc[i][136:166])
    dic['seven'] = sum(df_confirmed.loc[i][166:])
    # 统计计算每天各大洲确诊病例数
    dic_list.append(df_confirmed.loc[i][5:].tolist())
dic_list = np.array(dic_list)
for i in range(168):
    dc_list.append(sum(dic_list[:, i]))
for i in range(167):
    dc_new.append(dc_list[i + 1] - dc_list[i])

# print('ot', dc_list)
print('ot', dc_new)

# dk = [i.keys() for i in dic_list][0]
# ds_Others = [(k, sum([x[k] for x in dic_list])) for k in dk]
# ds_Others = [v for v in dict(ds_Others).values()]
# print("Others", ds_Others)

# TODO 极坐标柱状图, 条形图为层叠模式
# fig = plt.figure(figsize=(10, 6), dpi=100)
# # 极坐标图绘制
# ax = plt.subplot(111, projection='polar')
# # 顺时针
# ax.set_theta_direction(-1)
# # 正上方为0度
# ax.set_theta_zero_location('N')
# ax.set_title('covid-19')  # 设置标题
# # 设置极坐标角度网格线(即将圆盘分为几个扇形)显示及标签，标签默认显示为角度
# ax.set_thetagrids(
#     np.arange(10, 360, 50),
#     ['North America', 'South America', 'Asia', 'Australia', 'Africa', 'Europe', 'Others']
# )
#
# NA = np.array([int(d) for d in dcc_NA.values])
# SA = np.array([int(d) for d in dcc_SA.values])
# AS = np.array([int(d) for d in dcc_AS.values])
# AU = np.array([int(d) for d in dcc_AU.values])
# AF = np.array([int(d) for d in dcc_AF.values])
# EU = np.array([int(d) for d in dcc_EU.values])
# OT = np.array([int(d) for d in dcc_OT.values])
# dcc_country = np.vstack((NA, SA, AS, AU, AF, EU, OT))
# Confirmed = dcc_country[:, 0]
# Deaths = dcc_country[:, 1]
# Recovered = dcc_country[:, 2]
#
# N = 7
# theta = np.linspace(0, 2 * np.pi, N, endpoint=False)  # 均分角度
# width = np.pi / 4 * np.random.rand(N)  # 随机宽度
# radii = 10 * np.random.rand(N)
#
# bars = ax.bar(theta, Confirmed, width=width, bottom=0.0, color='#8da0cb')  # 哪个角度画，长度，扇形角度,从距离圆心0的地方开始画
# bars = ax.bar(theta, Deaths, width=width, bottom=0.0, color='#fc8d62')  # 哪个角度画，长度，扇形角度,从距离圆心0的地方开始画
# bars = ax.bar(theta, Recovered, width=width, bottom=0.0, color='#66c2a5')  # 哪个角度画，长度，扇形角度,从距离圆心0的地方开始画
#
# plt.show()

# TODO 绘制散点图
# ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
# ax.scatter(North_America_x, North_America_y, North_America_z, c="#8da0cb")  # 绘制数据点
# ax.scatter(South_America_x, South_America_y, South_America_z, c="#fc8d62")
# ax.scatter(Asia_x, Asia_y, Asia_z, c="#66c2a5")
# ax.scatter(Africa_x, Africa_y, Africa_z, c="#000000")
# ax.scatter(Australia_x, Australia_y, Australia_z, c="#0000FF")
# ax.scatter(Europe_x, Europe_y, Europe_z, c="#FF0000")
# ax.scatter(Others_x, Others_y, Others_z, c="#00FFFF")
#
# # 添加坐标轴(顺序是Z, Y, X)
# ax.set_zlabel('Recovered', fontdict={'size': 15, 'color': 'red'})
# ax.set_ylabel('Deaths', fontdict={'size': 15, 'color': 'red'})
# ax.set_xlabel('Confirmed', fontdict={'size': 15, 'color': 'red'})
# plt.legend(loc="upper left", labels=['Recovered', 'Deaths', 'Confirmed'])
# plt.show()

# TODO 折线堆叠图
# plt.rcParams["font.sans-serif"] = ["SimHei"]
# plt.rcParams["axes.unicode_minus"] = False
# x = ['一月', '二月', '三月', '四月', '五月', '六月', '七月']
# labels = ['North America', 'South America', 'Asia', 'Australia', 'Africa', 'Europe', 'Others']
# colors = ["#8da0cb", "#fc8d62", "#66c2a5", "#000000", "#0000FF", "#FF0000", "#00FFFF"]
#
# plt.stackplot(x, ds_North_America, ds_South_America, ds_Asia, ds_Australia, ds_Africa, ds_Europe, ds_Others,
#               labels=labels,
#               colors=colors)
# plt.legend(loc="upper left")
# plt.show()

# TODO 极坐标-堆叠柱状图
# z = ['North America', 'Asia', 'South America', 'Europe ', 'Africa', 'Australia', 'Others']
z = ['Others', 'Australia', 'Africa', 'Europe', 'South America', 'Asia', 'North America']
c = (
    Polar()
        .add_schema(angleaxis_opts=opts.AngleAxisOpts(data=z, type_="category"))
        .add("Deaths", Deaths, type_="bar", stack="stack0")
        .add("Recovered", Recovered, type_="bar", stack="stack0")
        .add("Confirmed", Confirmed, type_="bar", stack="stack0")
        .set_global_opts(title_opts=opts.TitleOpts(title="Polar-AngleAxis"))
        .render("polar_angleaxis.html")
)

# TODO 3D散点图
# async def get_json_data(url: str) -> dict:
#     async with ClientSession(connector=TCPConnector(ssl=False)) as session:
#         async with session.get(url=url) as response:
#             return await response.json()
#
#
# data = asyncio.run(
#     get_json_data(
#         url="https://echarts.baidu.com/examples/data/asset/data/nutrients.json"
#     )
# )
# print(data)
# 列名映射
# field_indices = {
#     "calcium": 3,
#     "calories": 12,
#     "carbohydrate": 8,
#     "fat": 10,
#     "Deaths": 5,
#     "group": 1,
#     "id": 16,
#     "monounsat": 14,
#     "name": 0,
#     "polyunsat": 15,
#     "potassium": 7,
#     "Recovered": 2,
#     "saturated": 13,
#     "Confirmed": 4,
#     "sugars": 9,
#     "vitaminc": 6,
#     "water": 11,
# }

# 配置 config
config_xAxis3D = "Recovered"
config_yAxis3D = "Deaths"
config_zAxis3D = "Confirmed"
config_color = "Deaths"
config_symbolSize = "vitaminc"

#  构造数据
# data = [
#     [
#         item[field_indices[config_xAxis3D]],
#         item[field_indices[config_yAxis3D]],
#         item[field_indices[config_zAxis3D]],
#         item[field_indices[config_color]],
#         item[field_indices[config_symbolSize]],
#         index,
#     ]
#     for index, item in enumerate(data)
# ]
# print(data)
dcc = sorted(dcc, reverse=False)
# print(dcc)
(
    Scatter3D(
        init_opts=opts.InitOpts(width="1440px", height="720px")
    )  # bg_color="black"
        .add(
        series_name="",
        data=dcc,
        xaxis3d_opts=opts.Axis3DOpts(
            name=config_xAxis3D,
            type_="value",
            # textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        yaxis3d_opts=opts.Axis3DOpts(
            name=config_yAxis3D,
            type_="value",
            # textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        zaxis3d_opts=opts.Axis3DOpts(
            name=config_zAxis3D,
            type_="value",
            # textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
    )
        .set_global_opts(
        visualmap_opts=[
            opts.VisualMapOpts(
                type_="color",
                is_calculable=True,
                dimension=3,
                pos_top="10",
                max_=79 / 2,
                range_color=[
                    "#ff8007",
                    "#fa1e33",
                    "#f5ff09",
                    "#7a0f6e",
                    "#034019",
                    "#221aff",
                    "#000000"
                ],
            ),
            opts.VisualMapOpts(
                type_="size",
                is_calculable=True,
                dimension=4,
                pos_bottom="10",
                max_=2.4 / 2,
                range_size=[10, 40],
            ),
            opts.VisualMapOpts(
                is_piecewise=True,  # 设置是否为分段显示
                # 自定义的每一段的范围，以及每一段的文字，以及每一段的特别的样式。例如：
                pieces=[
                    {"max": 3542762, "min": 1276624, "label": 'North America', "color": "#ff8007"},
                    {"max": 2701212, "min": 2603675, "label": 'Asia', "color": "#fa1e33"},
                    {"max": 2603674, "min": 2507999, "label": 'South America', "color": "#f5ff09"},
                    {"max": 1907998, "min": 1000659, "label": 'Europe', "color": "#7a0f6e"},
                    {"max": 508700, "min": 10456, "label": 'Africa', "color": "#034019"},
                    {"max": 10455, "min": 9006, "label": 'Australia', "color": "#221aff"},
                    {"max": 3437, "min": 123, "label": 'Others', "color": "#000000"},
                ],
            ),
        ]
    )
        .render("scatter3d.html")
)

# TODO 折线堆叠图
x_data = dc
# y_data = [0, 227668, 1171922, 4057470, 7894973, 17156669, 75144172]
labels = ['North_America', 'Asia', 'South_America', 'Africa', 'Europe', 'Australia', 'Others']
(
    Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
        series_name=labels[6],
        stack="总量",
        y_axis=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 61, 61, 64, 135, 135, 175, 175, 218, 285, 355, 454, 542,
                621, 634, 634, 634, 691, 691, 691, 705, 705, 705, 705, 705, 705, 706, 706, 710, 714, 723, 723, 726, 733,
                737, 737, 738, 742, 745, 745, 746, 754, 757, 760, 761, 766, 773, 776, 776, 872, 902, 918, 934, 945, 967,
                1002, 1035, 1069, 1102, 1136, 1154, 1186, 1203, 1204, 1279, 1324, 1332, 1357, 1475, 1495, 1581, 1628,
                1674, 1745, 1804, 1813, 1847, 1903, 1947, 1979, 2011, 2028, 2044, 2054, 2063, 2072, 2089, 2121, 2140,
                2150, 2154, 2175, 2176, 2178, 2188, 2202, 2237, 2238, 2263, 2264, 2265, 2283, 2297, 2336, 2349, 2388,
                2389, 2412, 2422, 2430, 2439, 2453, 2466, 2467, 2501, 2502, 2507, 2513, 2598, 2608, 2608, 2612, 2622,
                2746, 2756, 2797, 2839, 2842, 2953, 2956, 3019, 3028, 3069, 3138, 3213, 3323, 3375, 4228, 4397, 4557,
                4611, 4786, 5047, 5225, 5928, 6372, 6819, 7215, 7471, 7979, 8713, 8932],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[5],
        stack="总量",
        y_axis=[0, 0, 0, 0, 4, 5, 5, 6, 9, 9, 12, 12, 12, 13, 13, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
                15, 15, 15, 15, 15, 15, 15, 15, 15, 16, 26, 28, 31, 40, 55, 58, 64, 68, 81, 96, 112, 133, 133, 205, 256,
                305, 385, 464, 588, 710, 832, 1125, 1654, 1788, 2204, 2575, 3099, 3517, 4097, 4504, 4956, 5212, 5576,
                5921, 6206, 6513, 6739, 6919, 7072, 7237, 7364, 7516, 7633, 7663, 7718, 7799, 7844, 7887, 7955, 8014,
                8065, 8088, 8115, 8129, 8144, 8164, 8190, 8209, 8219, 8244, 8254, 8271, 8289, 8312, 8335, 8359, 8389,
                8409, 8429, 8436, 8459, 8471, 8493, 8503, 8512, 8543, 8559, 8569, 8579, 8593, 8601, 8610, 8625, 8629,
                8644, 8644, 8656, 8669, 8680, 8695, 8714, 8722, 8732, 8751, 8759, 8770, 8777, 8782, 8789, 8795, 8797,
                8804, 8815, 8819, 8824, 8850, 8865, 8879, 8902, 8924, 8942, 8946, 8998, 9013, 9034, 9064, 9105, 9143,
                9152, 9241, 9321, 9391, 9477, 9560, 9625, 9819, 10005, 10147, 10323],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[4],
        stack="总量",
        y_axis=[0, 0, 2, 3, 3, 4, 8, 10, 10, 18, 23, 25, 33, 34, 35, 35, 37, 46, 49, 49, 52, 53, 54, 55, 56, 56, 57, 57,
                58, 60, 78, 120, 218, 294, 402, 565, 834, 1130, 1504, 2261, 2824, 3497, 4501, 5921, 7726, 9882, 12413,
                15294, 18896, 24294, 28170, 39774, 47993, 56824, 67805, 79305, 93283, 112658, 133142, 154785, 174633,
                201481, 226099, 257073, 292994, 328940, 365839, 395718, 428359, 465086, 502267, 538529, 576146, 609979,
                637529, 666169, 697024, 731199, 765093, 799302, 828174, 879138, 904737, 929812, 961608, 1005561,
                1037715, 1061386, 1095438, 1118888, 1146198, 1171717, 1201259, 1216227, 1241108, 1263242, 1287139,
                1310922, 1331313, 1354079, 1376301, 1399163, 1420377, 1441434, 1463851, 1490277, 1515271, 1539372,
                1560264, 1580210, 1604044, 1626003, 1645702, 1666026, 1686394, 1703726, 1720289, 1736897, 1755958,
                1774207, 1791746, 1810351, 1826727, 1841425, 1855652, 1871273, 1886275, 1906565, 1923104, 1939950,
                1954709, 1968935, 1982720, 1999197, 2015392, 2031783, 2047872, 2062982, 2077747, 2092768, 2107661,
                2124050, 2141075, 2156982, 2171973, 2186066, 2201225, 2216861, 2233654, 2250233, 2264605, 2277702,
                2290669, 2306110, 2320785, 2335502, 2351427, 2364060, 2374974, 2391040, 2403797, 2417334, 2431115,
                2445046, 2456966, 2468470, 2483679]
        ,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[3],
        stack="总量",
        y_axis=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                2, 2, 3, 3, 4, 8, 11, 21, 24, 43, 43, 83, 91, 104, 118, 134, 177, 254, 313, 400, 484, 601, 781, 969,
                1172, 1437, 1818, 2250, 2773, 3326, 3885, 4225, 4786, 5196, 5781, 6380, 7032, 7913, 8592, 9298, 9999,
                10632, 11436, 12249, 12913, 13627, 14491, 15275, 16238, 17192, 18360, 19767, 21072, 22281, 23454, 24509,
                25911, 27361, 29068, 30299, 31833, 33167, 34794, 36807, 38820, 40570, 42766, 44301, 46959, 48997, 51543,
                54033, 57838, 60560, 63287, 66313, 69447, 72385, 75346, 78274, 81602, 84590, 88258, 91407, 95062, 99754,
                103869, 107741, 111803, 115883, 119445, 124724, 129443, 135366, 141590, 146785, 152491, 157366, 162505,
                169637, 176769, 183428, 189550, 196359, 202855, 209371, 216766, 224844, 232924, 241776, 251399, 259102,
                267809, 275783, 285905, 297103, 306381, 315370, 324514, 335781, 347826, 359581, 371590, 382180, 393222,
                404786, 418201, 432321, 447454, 463065, 476627, 490471]
        ,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[2],
        stack="总量",
        y_axis=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                1, 1, 1, 2, 8, 8, 11, 16, 22, 34, 40, 62, 69, 91, 124, 143, 297, 360, 425, 658, 941, 1184, 1658, 2275,
                2989, 4125, 4937, 5773, 6596, 7709, 8892, 10173, 11202, 12190, 14386, 16763, 19063, 21084, 23412, 25324,
                27334, 30200, 35276, 39382, 44754, 47582, 50458, 54532, 57592, 62787, 67138, 72430, 77539, 82054, 86259,
                91036, 96389, 103805, 121198, 131250, 138131, 145073, 155454, 166066, 178556, 190180, 200428, 212500,
                224588, 237541, 254005, 267716, 283208, 297971, 310032, 320686, 336212, 356272, 377483, 403143, 424955,
                440234, 461149, 487775, 518498, 547796, 578305, 605010, 631440, 654475, 682683, 717006, 755859, 795481,
                843490, 875658, 901751, 938290, 984442, 1027545, 1072078, 1111719, 1144762, 1172493, 1215125, 1262696,
                1308713, 1346585, 1385472, 1422818, 1458641, 1505699, 1582698, 1619064, 1690651, 1740062, 1773951,
                1810157, 1863497, 1917839, 1974836, 2038144, 2093769, 2143324, 2178001, 2225846, 2287092, 2350921,
                2410077, 2463633, 2505479, 2540006],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[1],
        stack="总量",
        y_axis=[554, 653, 937, 1429, 2105, 2912, 5558, 6143, 8208, 9889, 11991, 16738, 19827, 23836, 27578, 30736,
                34266, 36990, 40015, 42551, 44588, 44966, 60112, 66585, 68662, 70786, 72720, 74510, 74934, 75479, 76081,
                77792, 78028, 78516, 79257, 80056, 81147, 82220, 83717, 85317, 86694, 88559, 89793, 91071, 93110, 94848,
                96069, 96951, 98132, 99886, 101188, 103035, 104966, 106964, 108611, 110593, 112681, 114938, 117481,
                120028, 123262, 126351, 130067, 135495, 140994, 147987, 155312, 162663, 169754, 178498, 187151, 196368,
                204848, 213976, 223550, 233838, 243271, 252840, 263135, 274583, 286367, 298079, 309957, 321279, 332701,
                344993, 358289, 370316, 382657, 396213, 409802, 422308, 435574, 448703, 460787, 472354, 483969, 495200,
                508109, 521193, 534330, 546359, 559141, 573403, 588663, 603941, 619733, 636574, 651953, 669959, 686556,
                703609, 720857, 741456, 758951, 778882, 799714, 820508, 842484, 865021, 889227, 913477, 937877, 961753,
                983578, 1003745, 1027647, 1053363, 1082183, 1109812, 1139015, 1166977, 1197542, 1230922, 1263199,
                1296080, 1330620, 1365171, 1396313, 1430223, 1466673, 1504525, 1537257, 1576201, 1621098, 1658330,
                1696815, 1737814, 1778804, 1821582, 1863517, 1903189, 1943543, 1985730, 2029433, 2073560, 2119679,
                2165903, 2212644, 2256838, 2303267, 2369758, 2419657, 2470148, 2523711, 2579359, 2629126],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[0],
        stack="总量",
        y_axis=[1, 1, 2, 2, 6, 6, 7, 7, 7, 11, 12, 12, 15, 15, 16, 16, 18, 18, 18, 18, 19, 19, 20, 20, 20, 20, 21, 21,
                21, 21, 24, 24, 24, 25, 26, 26, 29, 31, 48, 60, 86, 109, 143, 217, 280, 400, 532, 617, 812, 1254, 1735,
                2446, 3202, 3378, 4989, 6886, 9898, 15403, 21016, 27930, 36375, 47256, 58366, 71081, 90313, 109551,
                130745, 151073, 174025, 201744, 228701, 261327, 294949, 329168, 360533, 391649, 424427, 458212, 495417,
                531382, 563516, 594065, 621566, 650645, 681939, 716721, 752782, 783830, 812433, 842962, 871310, 903359,
                941051, 980806, 1016691, 1047462, 1072908, 1100427, 1131359, 1164758, 1202989, 1236164, 1266248,
                1292250, 1319581, 1348764, 1380948, 1412229, 1442056, 1465585, 1487712, 1513392, 1538455, 1570382,
                1600294, 1629673, 1652516, 1678774, 1704373, 1731995, 1762742, 1792224, 1819814, 1846037, 1869823,
                1894777, 1918848, 1947208, 1977394, 2007069, 2032842, 2055081, 2081856, 2107947, 2135925, 2167624,
                2196490, 2220088, 2242954, 2267861, 2296159, 2326648, 2359919, 2392063, 2419089, 2444026, 2475168,
                2508656, 2545321, 2585110, 2626296, 2661196, 2699665, 2744701, 2788149, 2838130, 2891840, 2942813,
                2989973, 3039090, 3094334, 3155404, 3221072, 3286071, 3343755, 3403401, 3457559],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="各大洲确诊图"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
        .render("stacked_area_chart.html")
)

# North_America
na_list = np.array(na_list)
na_sum = []
for i in range(na_list.shape[1]):
    na_sum.append(sum(na_list[:, i]))
# print(na_sum)
# Asia
as_list = np.array(as_list)
as_sum = []
for i in range(as_list.shape[1]):
    as_sum.append(sum(as_list[:, i]))
# print(as_sum)
# South_America
sa_list = np.array(sa_list)
sa_sum = []
for i in range(sa_list.shape[1]):
    sa_sum.append(sum(sa_list[:, i]))
# print(sa_sum)
# Africa
af_list = np.array(af_list)
af_sum = []
for i in range(af_list.shape[1]):
    af_sum.append(sum(af_list[:, i]))
# print(af_sum)
# Europe
eu_list = np.array(eu_list)
eu_sum = []
for i in range(eu_list.shape[1]):
    eu_sum.append(sum(eu_list[:, i]))
# print(eu_sum)
# Australia
au_list = np.array(au_list)
au_sum = []
for i in range(au_list.shape[1]):
    au_sum.append(sum(au_list[:, i]))
# print(au_sum)
# Others
ot_list = np.array(ot_list)
ot_sum = []
for i in range(ot_list.shape[1]):
    ot_sum.append(sum(ot_list[:, i]))
# print(ot_sum)
# TODO 折线图
x_data = dc
# print(dc)
y_data = [820, 9329, 9099991, 9349999, 129009, 133099, 13209999]

(
    Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
        # yaxis_index=y_data,
        series_name=labels[6],
        stack="总量",
        y_axis=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 61, 0, 3, 71, 0, 40, 0, 43, 67, 70, 99, 88, 79, 13, 0, 0,
                57, 0, 0, 14, 0, 0, 0, 0, 0, 1, 0, 4, 4, 9, 0, 3, 7, 4, 0, 1, 4, 3, 0, 1, 8, 3, 3, 1, 5, 7, 3, 0, 96,
                30, 16, 16, 11, 22, 35, 33, 34, 33, 34, 18, 32, 17, 1, 75, 45, 8, 25, 118, 20, 86, 47, 46, 71, 59, 9,
                34, 56, 44, 32, 32, 17, 16, 10, 9, 9, 17, 32, 19, 10, 4, 21, 1, 2, 10, 14, 35, 1, 25, 1, 1, 18, 14, 39,
                13, 39, 1, 23, 10, 8, 9, 14, 13, 1, 34, 1, 5, 6, 85, 10, 0, 4, 10, 124, 10, 41, 42, 3, 111, 3, 63, 9,
                41, 69, 75, 110, 52, 853, 169, 160, 54, 175, 261, 178, 703, 444, 447, 396, 256, 508, 734, 219, 501]

        ,
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[5],
        stack="总量",
        y_axis=[0, 0, 0, 4, 1, 0, 1, 3, 0, 3, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 1, 10, 2, 3, 9, 15, 3, 6, 4, 13, 15, 16, 21, 0, 72, 51, 49, 80, 79, 124, 122, 122, 293, 529, 134,
                416, 371, 524, 418, 580, 407, 452, 256, 364, 345, 285, 307, 226, 180, 153, 165, 127, 152, 117, 30, 55,
                81, 45, 43, 68, 59, 51, 23, 27, 14, 15, 20, 26, 19, 10, 25, 10, 17, 18, 23, 23, 24, 30, 20, 20, 7, 23,
                12, 22, 10, 9, 31, 16, 10, 10, 14, 8, 9, 15, 4, 15, 0, 12, 13, 11, 15, 19, 8, 10, 19, 8, 11, 7, 5, 7, 6,
                2, 7, 11, 4, 5, 26, 15, 14, 23, 22, 18, 4, 52, 15, 21, 30, 41, 38, 9, 89, 80, 70, 86, 83, 65, 194, 186,
                142, 176]

        ,
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[4],
        stack="总量",
        y_axis=[0, 2, 1, 0, 1, 4, 2, 0, 8, 5, 2, 8, 1, 1, 0, 2, 9, 3, 0, 3, 1, 1, 1, 1, 0, 1, 0, 1, 2, 18, 42, 98, 76,
                108, 163, 269, 296, 374, 757, 563, 673, 1004, 1420, 1805, 2156, 2531, 2881, 3602, 5398, 3876, 11604,
                8219, 8831, 10981, 11500, 13978, 19375, 20484, 21643, 19848, 26848, 24618, 30974, 35921, 35946, 36899,
                29879, 32641, 36727, 37181, 36262, 37617, 33833, 27550, 28640, 30855, 34175, 33894, 34209, 28872, 50964,
                25599, 25075, 31796, 43953, 32154, 23671, 34052, 23450, 27310, 25519, 29542, 14968, 24881, 22134, 23897,
                23783, 20391, 22766, 22222, 22862, 21214, 21057, 22417, 26426, 24994, 24101, 20892, 19946, 23834, 21959,
                19699, 20324, 20368, 17332, 16563, 16608, 19061, 18249, 17539, 18605, 16376, 14698, 14227, 15621, 15002,
                20290, 16539, 16846, 14759, 14226, 13785, 16477, 16195, 16391, 16089, 15110, 14765, 15021, 14893, 16389,
                17025, 15907, 14991, 14093, 15159, 15636, 16793, 16579, 14372, 13097, 12967, 15441, 14675, 14717, 15925,
                12633, 10914, 16066, 12757, 13537, 13781, 13931, 11920, 11504, 15209]

        ,
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[3],
        stack="总量",
        y_axis=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                0, 1, 0, 1, 4, 3, 10, 3, 19, 0, 40, 8, 13, 14, 16, 43, 77, 59, 87, 84, 117, 180, 188, 203, 265, 381,
                432, 523, 553, 559, 340, 561, 410, 585, 599, 652, 881, 679, 706, 701, 633, 804, 813, 664, 714, 864, 784,
                963, 954, 1168, 1407, 1305, 1209, 1173, 1055, 1402, 1450, 1707, 1231, 1534, 1334, 1627, 2013, 2013,
                1750, 2196, 1535, 2658, 2038, 2546, 2490, 3805, 2722, 2727, 3026, 3134, 2938, 2961, 2928, 3328, 2988,
                3668, 3149, 3655, 4692, 4115, 3872, 4062, 4080, 3562, 5279, 4719, 5923, 6224, 5195, 5706, 4875, 5139,
                7132, 7132, 6659, 6122, 6809, 6496, 6516, 7395, 8078, 8080, 8852, 9623, 7703, 8707, 7974, 10122, 11198,
                9278, 8989, 9144, 11267, 12045, 11755, 12009, 10590, 11042, 11564, 13415, 14120, 15133, 15611, 13562,
                13844]

        ,
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[2],
        stack="总量",
        y_axis=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 1, 6, 0, 3, 5, 6, 12, 6, 22, 7, 22, 33, 19, 154, 63, 65, 233, 283, 243, 474, 617, 714, 1136, 812,
                836, 823, 1113, 1183, 1281, 1029, 988, 2196, 2377, 2300, 2021, 2328, 1912, 2010, 2866, 5076, 4106, 5372,
                2828, 2876, 4074, 3060, 5195, 4351, 5292, 5109, 4515, 4205, 4777, 5353, 7416, 17393, 10052, 6881, 6942,
                10381, 10612, 12490, 11624, 10248, 12072, 12088, 12953, 16464, 13711, 15492, 14763, 12061, 10654, 15526,
                20060, 21211, 25660, 21812, 15279, 20915, 26626, 30723, 29298, 30509, 26705, 26430, 23035, 28208, 34323,
                38853, 39622, 48009, 32168, 26093, 36539, 46152, 43103, 44533, 39641, 33043, 27731, 42632, 47571, 46017,
                37872, 38887, 37346, 35823, 47058, 76999, 36366, 71587, 49411, 33889, 36206, 53340, 54342, 56997, 63308,
                55625, 49555, 34677, 47845, 61246, 63829, 59156, 53556, 41846, 34527]
        ,
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[1],
        stack="总量",
        y_axis=[99, 284, 492, 676, 807, 2646, 585, 2065, 1681, 2102, 4747, 3089, 4009, 3742, 3158, 3530, 2724, 3025,
                2536, 2037, 378, 15146, 6473, 2077, 2124, 1934, 1790, 424, 545, 602, 1711, 236, 488, 741, 799, 1091,
                1073, 1497, 1600, 1377, 1865, 1234, 1278, 2039, 1738, 1221, 882, 1181, 1754, 1302, 1847, 1931, 1998,
                1647, 1982, 2088, 2257, 2543, 2547, 3234, 3089, 3716, 5428, 5499, 6993, 7325, 7351, 7091, 8744, 8653,
                9217, 8480, 9128, 9574, 10288, 9433, 9569, 10295, 11448, 11784, 11712, 11878, 11322, 11422, 12292,
                13296, 12027, 12341, 13556, 13589, 12506, 13266, 13129, 12084, 11567, 11615, 11231, 12909, 13084, 13137,
                12029, 12782, 14262, 15260, 15278, 15792, 16841, 15379, 18006, 16597, 17053, 17248, 20599, 17495, 19931,
                20832, 20794, 21976, 22537, 24206, 24250, 24400, 23876, 21825, 20167, 23902, 25716, 28820, 27629, 29203,
                27962, 30565, 33380, 32277, 32881, 34540, 34551, 31142, 33910, 36450, 37852, 32732, 38944, 44897, 37232,
                38485, 40999, 40990, 42778, 41935, 39672, 40354, 42187, 43703, 44127, 46119, 46224, 46741, 44194, 46429,
                66491, 49899, 50491, 53563, 55648, 49767]
        ,
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .add_yaxis(
        series_name=labels[0],
        stack="总量",
        y_axis=[0, 1, 0, 4, 0, 1, 0, 0, 4, 1, 0, 3, 0, 1, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 1, 1, 0,
                3, 2, 17, 12, 26, 23, 34, 74, 63, 120, 132, 85, 195, 442, 481, 711, 756, 176, 1611, 1897, 3012, 5505,
                5613, 6914, 8445, 10881, 11110, 12715, 19232, 19238, 21194, 20328, 22952, 27719, 26957, 32626, 33622,
                34219, 31365, 31116, 32778, 33785, 37205, 35965, 32134, 30549, 27501, 29079, 31294, 34782, 36061, 31048,
                28603, 30529, 28348, 32049, 37692, 39755, 35885, 30771, 25446, 27519, 30932, 33399, 38231, 33175, 30084,
                26002, 27331, 29183, 32184, 31281, 29827, 23529, 22127, 25680, 25063, 31927, 29912, 29379, 22843, 26258,
                25599, 27622, 30747, 29482, 27590, 26223, 23786, 24954, 24071, 28360, 30186, 29675, 25773, 22239, 26775,
                26091, 27978, 31699, 28866, 23598, 22866, 24907, 28298, 30489, 33271, 32144, 27026, 24937, 31142, 33488,
                36665, 39789, 41186, 34900, 38469, 45036, 43448, 49981, 53710, 50973, 47160, 49117, 55244, 61070, 65668,
                64999, 57684, 59646, 54158, 70260]
        ,
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="Daily new confirmed cases", padding=25),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
        .render("stacked_line_chart.html")
)
