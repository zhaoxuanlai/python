import back_test as bt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd

# 设置中文字体（用于输出）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

industries = ['石油石化', '煤炭', '有色金属', '电力及公用事业', '钢铁', '基础化工', '建筑', '建材', '轻工制造', '机械', '电力设备', '国防军工', '汽车', '商贸零售',
              '餐饮旅游', '家电', '纺织服装', '医药', '食品饮料', '农林牧渔', '银行', '非银行金融', '房地产', '交通运输', '电子元器件', '通信', '计算机', '传媒',
              '综合']
indexes = ['销售净利率', '销售毛利率', '净资产收益率', '总资产净利率', '营业收入', '归母净利润', '净利润', '利润总额', '总资产周转率', '资产负债率']
weight_even = {industry: 1 for industry in industries}
weight_new = weight_even

'''
weight: 调整权重函数
    -用前t年的数据对各行业进行预测试，判断各行业在相应指标预测下的效果
    -调整各行业资金权重，将4/5的资金用于利好行业，剩余1/5的资金投资剩余行业
    -参数x: 当前t期的最终资金大于初始资金的x倍时，认为该行业对该指标是利好的
           （如果没有一个行业表现利好，则降低标准为(x-0.1)倍再次进行测试
    -参数weight_d: 初始设定的资金权重字典，默认为None(平均分配)
'''


def weight(index, t_start, t_end, x, h=1, r=0, l=0, d=0, weight_d=None):
    global weight_new
    if weight_d is None:
        weight_d = weight_even
    lst = []
    up_count = 0
    for industry in industries:
        end_money = bt.back_test(industry, index, t_start, t_end, weight_d, high=h, r=r, lag=l, details=0)[0][-1]
        revenue1 = (end_money / weight_d[industry] - 1) * 100
        if d == 1:
            print('--正在根据%s指标调整权重--' % index)
            print('%s行业测试收益率为%d%s' % (industry, revenue1, '%'))
        lst.append((industry, end_money))
        up_count += 1 if end_money / weight_d[industry] > x else 0
        if up_count != 0:
            principal_new_up = (4 / 5 * len(industries)) / up_count
            principal_new_down = (1 / 5 * len(industries)) / (len(industries) - up_count)
            weight_new = {i[0]: principal_new_up if i[1] > x else principal_new_down for i in lst}
        else:
            weight_new = weight(index, t_start, t_end, x - 0.1, h, r, l, 0, weight_d)

    return weight_new


'''
get_result：计算出资金变化曲线、相关收益指标、并作图
    -先用weight调整资金比例，再进行回测（参数ow可以控制是否采用实现调整的策略）
    -参数avoid_down: 当遇到较大亏损的时候，是否在下一期改变策略，=1为改变，=0为不执行这个操作
    -参数high: high=1表示指标越高，预测情况越好；high=-1表示指标越高，预测情况越差
'''


def get_result(ind, t, x, r=0, high=1, ow=1, avoid_down=0, l=0, d=0):
    p_list = []
    win = [0, 0, 0]
    weight_dict = weight(ind, 0, t, x, high, r, l, d) if ow == 1 else weight_even
    if d == 1:
        s1 = '\n————<调整资金权重完成>————\n' if ow == 1 else '\n————<无须调整权重>————\n'
        print('%s' % s1)
        print('当前资金权重：')
        [print('%s行业：%f单位资金' % (industry, weight_dict[industry])) for industry in industries]
        print('\n' * 2)
        print('\n————<开始回测>————\n')
    for industry in industries:
        p = bt.back_test(industry, ind, t - 1, 10, weight_dict, high=high, ad=avoid_down, r=r, lag=l, details=d)
        p_list.append(p)
        win[0] += p[3].count(1)
        win[1] += p[3].count(0)
        win[2] += p[3].count(-1)

    '''
    制作资金变化列表
        -money: 按指标策略选股；
        -random_money: 随机选择看多/看空/空仓
    '''
    money = []
    random_money = []
    year = 0
    for time in range(len(p_list[0][0])):
        money_t, random_money_t = 0, 0
        for i in p_list:
            money_t += i[0][time]
            random_money_t += i[2][time]
            year = 8 - t if i[1] == '同比增长率增速' else 9 - t
        money.append(money_t)
        random_money.append(random_money_t)

    '''
    计算相关的评价指标
        -revenue: 年化收益率 =（末年资金总量/起始资金总量-1）*100% / 回测时间长度
        -volatility: 年华波动率，假设市场价格变动本身呈三次曲线状，拟合一条三次曲线，计算价格变动相对这条曲线的标准差， 
                     相当于月标准差，在乘sqrt(12)后作为年化波动率
        -sharp_ratio: 夏普比 = 年化收益率 / 年华波动率
        -worst_ratio: 最大回撤 = （指数最低时资金总量/起始资金总量-1）*100%
        -win_ratio: 多空胜率 = n(指标预测和价格相符的时间点) / n(所有做出多空判断的时间点) * 100%
    '''
    revenue = (money[-1] - 29) / (29 * (year + 0.5))
    x1 = [i for i in range(len(money))]
    x1_a, money_a = np.array(x1), np.array(money)
    f1 = np.polyfit(x1_a, money_a, 3)
    p1 = np.poly1d(f1)
    diff_money_even = [money[i] - p1[i] for i in range(len(money))]
    volatility = np.std(diff_money_even) / np.mean(money) * np.sqrt(12)
    sharp_ratio = revenue / volatility
    worst_ratio = min(money) / money[0] - 1
    y_s_start = (2010 + t, 2) if year == 9 - t else (2010 + t + 1, 2)

    '''
    资金曲线作图，便于观察和研究
        -红色实线：依据定期业绩指标得到的资金变动曲线
        -黑色虚线：随机选择买多/卖空/空仓得到的资金变动曲线(用于对比)
    '''
    x = ['%d年%d月底' % (y_s_start[0], 4 + m) for m in range(9)] + \
        ['%d年%d月底' % (y_s_start[0] + y, 1 + m) for y in range(1, year) for m in range(12)] + \
        ['%d年%d月底' % (y_s_start[0] + year, 1 + m) for m in range(9)]
    y = money
    y_random = random_money
    fig = plt.figure(figsize=(15, 9), facecolor='pink')
    plt.style.use('seaborn-bright')
    plt.title('根据%s指标调仓时的收益情况' % ind, size=18, weight='bold')
    plt.grid()
    ax = plt.gca()
    plt.plot(x, y, color='red', label='根据%s指标调仓时的资金曲线' % ind, linewidth=4.0)
    plt.plot(x, y_random, color='black', label='随机调仓时的资金曲线', linewidth=3.0, linestyle=':')
    plt.xlabel("时间", size=16, weight='semibold')
    plt.ylabel("资金量（假设刚开始有29单位）", size=16, weight='semibold')
    ax.xaxis.set_major_locator(MultipleLocator(12))
    ax.xaxis.set_minor_locator(MultipleLocator(3))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.legend(loc='upper left', fontsize=16)
    plt.savefig('./根据%s指标调仓时的收益情况.jpg' % ind, facecolor=fig.get_facecolor(), edgecolor='none')

    return revenue, volatility, sharp_ratio, worst_ratio, win[0] / (win[0] + win[2])


'''
review: 遍历所有的指标，得到每个指标的收益数据，以字典形式返回
    -参数opt_weight: 确定是否对资金比例进行调整权重，=1为调整，=0为不执行此操作
    -参数t: 进行权重调整时，0~t为测试部分，用于确定最终的资金权重
    -参数x: 进行权重调整时，判断是否重点投资一个行业的阈值
    -参数lag: 确定定期业绩指标的披露是否滞后(实际上，本研究中指标的披露都是滞后的)，=1为滞后，=0为不滞后
    -参数details: 确定是否打印详细信息，=1为打印详细信息，=0为不打印详细信息
'''


def review(t=2, x=1.0, opt_weight=0, lag=0, details=0):
    global r
    result, result_d = [], {i: [] for i in range(6)}
    for index in indexes:
        print('\n' + '——————<使用%s作为判断指标>——————' % index + '\n')
        if details == 0:
            print('拼命计算中......')
        if index in ['销售净利率', '销售毛利率', '净资产收益率', '总资产净利率', '总资产周转率']:
            r = get_result(index, t=t, x=x, ow=opt_weight, avoid_down=1, l=lag, d=details)
        elif index in ['归母净利润', '净利润', '利润总额', '营业收入']:
            r = get_result(index, t=t, x=x, ow=opt_weight, l=lag, d=details)
        elif index == '资产负债率':
            r = get_result(index, t=t, x=x, high=-1, ow=opt_weight, l=lag, d=details)
        result += [[index] + ['%.2f' % (r[i] * 100) + '%' for i in range(5)]]
    [result_d[i].append(result[j][i]) for i in range(6) for j in range(len(indexes))]

    return result_d


# 执行回测，并将回测结果保存为.xlsx文件
result_d = review(t=4, x=0.8, opt_weight=1, lag=1, details=1)
print('\n————————<最终结果>————————\n')
p_col = ['指标', '年化收益率', '年化波动率', '夏普比', '最大回撤', '多空胜率']
result_df = pd.DataFrame(result_d)
result_df.columns = p_col
print(result_df)
result_df.to_excel('./结果和相关数据表.xlsx')
