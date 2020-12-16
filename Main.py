# coding:utf-8

import pandas
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#主函数，程序入口
if __name__ == '__main__':
    confirm_data = pandas.read_csv("time_series_covid19_confirmed_global(1).csv")
    death_data = pandas.read_csv("time_series_covid19_deaths_global(1).csv")

    country_confirm_data = confirm_data.groupby("Country/Region")["7/22/20"].sum()
    country_confirm_data = pandas.DataFrame({"country": country_confirm_data.index, "death": country_confirm_data.values})

    country_death_data = death_data.groupby("Country/Region")["7/22/20"].sum()
    country_death_data = pandas.DataFrame({"country": country_death_data.index, "death": country_death_data.values})

    country_data = pandas.merge(country_confirm_data, country_death_data, on="country")
    country_data.columns = ["country","confirm","death"]

    kmeans = KMeans(n_clusters=5)
    kmeans.fit(country_data[["confirm","death"]])
    country_data["cluster_label"] = kmeans.labels_.tolist()
    country_data.to_csv("cluster_results.csv", index=False)

    # 设置图片大小和清晰度
    plt.figure(figsize=(4, 2.5), dpi=300)
    # MAC下设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    # Windows下设置中文字体
    # 设置坐标轴文字大小
    plt.tick_params(labelsize=3)

    colors = ["red","green","blue","purple","#ff8020"]
    for type in range(5):
        data = country_data[country_data["cluster_label"] == type]
        plt.scatter(data["confirm"],data["death"], s=4, color=colors[type])
    # 添加标签
    countries = ["China", "US","Brazil","India","Russia","United Kingdom","Mexico","Italy","France","Spain","Netherlands","Belgium"]
    for country in countries:
        data = country_data[country_data["country"] == country]
        if country == "US":
            country = "USA"
        plt.annotate(country, xy=(data["confirm"],data["death"]), xytext=(data["confirm"]+1, data["death"]+1), fontsize=3)
    # 设置横坐标标题
    plt.xlabel("Confirmed", fontsize=4)
    # 设置纵坐标标题
    plt.ylabel("Deaths", fontsize=4)
    # 设置坐标轴不用科学计数法
    plt.ticklabel_format(axis='x', style='plain')
    # 添加标题
    plt.title("Confirmed and Deaths Kmeans Clustering", fontsize=7)
    # 保存图片
    plt.savefig("Confirmed and Deaths Kmeans Clustering.png")
    # 显示图形
    plt.show()