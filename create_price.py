import pandas as pd

'''
不考虑滞后性的情况下，将指数整理成便于回测的二维列表
其中将每年按四个季度均匀切割
'''


def create_price(file_location, file_name):
    p_col = ['代码', '行业'] + ['201%d_%s' % (i, j) for i in range(9, -1, -1) for j in range(12, 0, -1)]  # 表示的是月初
    data = pd.read_excel('%s/%s.xlsx' % (file_location, file_name))
    data.columns = p_col
    data = data.drop(['代码'], axis=1)
    data_dict = data.iloc[0:29].to_dict()
    data_d = {}
    for i in range(29):
        lst, lst_new = [], []
        [lst.append(data_dict[j][i]) for j in p_col[2:]]
        lst.reverse()
        lst.append(1)  # 补一个2019年末的数据
        for k in range(40):
            lst_new.append([lst[3 * k], lst[3 * k + 1], lst[3 * k + 2], lst[3 * k + 3]])
        data_d[data_dict['行业'][i]] = lst_new

    return data_d


'''
因为正式财报的中报和年报有一定的滞后性，考虑滞后性后，产生对应的指数列表:
产生的每一个子列表代表一个观点持续的区间，滞后性导致区间变得不均匀。
数据被切为：
2010年：[1月~4月]
2010年~2018年：[5月~8月];[9月~10月];[11月~次年4月]
2019年：[9月~10月];[11月~12月]
'''


def create_price_lag(file_location, file_name):
    p_col = ['代码', '行业'] + ['201%d_%s' % (i, j) for i in range(9, -1, -1) for j in range(12, 0, -1)]  # 表示的是月初
    data = pd.read_excel('%s/%s.xlsx' % (file_location, file_name))
    data.columns = p_col
    data = data.drop(['代码'], axis=1)
    data_dict = data.iloc[0:29].to_dict()
    data_d = {}
    for i in range(29):
        lst = []
        [lst.append(data_dict[j][i]) for j in p_col[2:]]
        lst.reverse()
        lst.append(1)  # 补充2019年12月底的数据，方便处理
        lst_new = [lst[:5]]
        for k in range(9):
            lst_new.append([lst[12 * k + i] for i in range(4, 9)])
            lst_new.append([lst[12 * k + i] for i in range(8, 11)])
            lst_new.append([lst[12 * k + i] for i in range(10, 17)])
            lst_new.append([lst[12 * k + i] for i in range(10, 17)])
        lst_new.append([lst[-9], lst[-8], lst[-7], lst[-6], lst[-5]])
        lst_new.append([lst[-5], lst[-4], lst[-3]])
        lst_new.append([lst[-3], lst[-2], lst[-1]])
        data_d[data_dict['行业'][i]] = lst_new

    return data_d
