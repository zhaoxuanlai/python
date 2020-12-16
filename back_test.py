import create_index as ci
import create_price as cp
import create_price as cplag
import numpy as np
import math
import random

ind, t = 0, 0

'''
judge_position: 判断多空函数
    -依据不同的数据类型，对指标相对表现进行判断，并以此计算下一个时段如何调仓
'''


def judge_position(index_list, time, compare_type, r, d, m, high=1):
    global ind, t
    if compare_type == '同比增长率增速':
        ratio1 = index_list[time] / index_list[time - 4]
        ratio0 = index_list[time - 4] / index_list[time - 8]
        ind = ratio1 - ratio0
        t = math.sqrt(2 * (r * d / m) * (r * d / m))
    elif compare_type == '环比增量':
        ind = index_list[time] - index_list[time - 1]
        t = r * d
    elif compare_type == '同比增量':
        ind = index_list[time] - index_list[time - 4]
        t = r * d
    pos = 1 * high if ind > t else -1 * high if ind < -t else 0

    return pos, t


'''
imitation: 模拟运行函数
    -参数avoid_down: 选定后，如果在当前月发现出现大于10%的亏损，下一个月按照相反的观点调仓。
    -参数start, end: 执行模拟的年份区间
    -参数weight: 一个字典，记录每个行业的初始资金权重
    -参数random_judge: 是否随机调仓，=False为不随机调仓，=True为随机调仓
'''


def imitation(industry_name, index_list, price_list, compare_type, start, end, weight, r, d, m, high=1, avoid_down=1,
              lag=0, random_judge=False, details=0):
    principal = weight[industry_name]
    principal_list = [principal]
    piece = 3 if lag == 1 else 4
    win_ratio = []
    threshold = 0
    longevity = 6
    x = 0.08
    begin = start + 2 if compare_type == '同比增长率增速' else start + 1
    for i in range(begin, end):
        k = piece - 1 if i == 9 else piece
        for j in range(k):
            if details == 1:
                period = '5月~8月' if j == 0 else '9月~10月' if j == 1 else '11月~4月'
                r_now = (principal_list[-1] / principal_list[0]) - 1
                print('正在回测：201%d年%s\t行业：%s\t目前收益：%f' % (i, period, industry_name, r_now))
            position, threshold = judge_position(index_list, 4 * i + j, compare_type, r, d, m, high=high)
            if random_judge:
                position = random.choice([-1, 0, 1])
            big_down = False
            for k in range(min(len(price_list[4 * i + j + 1]) - 1, longevity)):
                if big_down:
                    position = -position
                price_ratio = price_list[4 * i + j + 1][k + 1] / price_list[4 * i + j + 1][k]
                if avoid_down == 1:
                    if (price_ratio < 1 - x and position == 1) or (price_ratio > 1 + x and position == -1):
                        big_down = True
                    else:
                        big_down = False
                up = 1 if price_ratio > 1 else -1 if price_ratio < 1 else 0
                win = 0 if position == 0 else 1 if up == position else -1
                win_ratio.append(win)
                if position == 1:
                    principal = principal * price_ratio
                elif position == -1:
                    principal = principal / price_ratio
                principal_list.append(principal)
            if len(price_list[4 * i + j + 1]) > longevity + 1:
                [principal_list.append(principal) for i in range(len(price_list[4 * i + j + 1]) - longevity - 1)]
    principal_list.pop()  # 去掉2019年末的无效值
    win_ratio.pop()

    return principal_list, win_ratio, threshold


# 打印每次回测的一些详细信息
def show_details(index_name, industry_name, result, stat):
    print('定期业绩指标名称：', index_name)
    print('行业名称：', industry_name)
    print('%s行业%s平均值：' % (industry_name, index_name), stat[0])
    print('%s行业%s标准差：' % (industry_name, index_name), stat[1])
    print('行业最终收益：', (result[0][-1] - 1) * 100, '%')
    if result[1].count(1) + result[1].count(-1) != 0:
        print('多空胜率：', result[1].count(1) / (result[1].count(1) + result[1].count(-1)))
    else:
        print('该行业%s指标缺失' % index_name)
    print('\n' * 1)


'''
back_test: 回测函数
    -按指标调仓和随机调仓各模拟以此，返回需要的回测结果
'''


def back_test(industry_name, index_name, start, end, weight, high=1, r=0, lag=0, details=0, ad=0):
    # 数据准备
    index_list = ci.create_index(index_name, industry_name)
    index_mean, index_std = np.mean(index_list), np.std(index_list)
    diff_std = math.sqrt(2 * index_std * index_std)
    stat = [index_mean, index_std]
    index_list += [index_mean]
    compare_type = '同比增量' if index_name in ['资产负债率'] else '同比增长率增速' if index_name in ['营业收入', '归母净利润', '净利润',
                                                                                      '利润总额'] else '环比增量'
    if lag == 0:
        price_list = cp.create_price('中信一级行业指数', '中信证券一级行业指数')[industry_name]
    else:
        price_list = cplag.create_price_lag('中信一级行业指数', '中信证券一级行业指数')[industry_name]

    # 进行回测
    result = imitation(industry_name, index_list, price_list, compare_type, start, end, weight, r, diff_std, index_mean,
                       high=high, avoid_down=ad, lag=lag, details=details)
    random_result = imitation(industry_name, index_list, price_list, compare_type, start, end, weight, r, diff_std,
                              index_mean, high=high, avoid_down=ad, lag=lag, random_judge=True, details=0)

    # 输出结果
    if details == 1:
        show_details(index_name, industry_name, result, stat)

    return result[0], compare_type, random_result[0], result[1]
