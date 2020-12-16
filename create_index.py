import pandas as pd

'''
提取.xlsx中的数据，并以此计算每个季度的数据，整理成列表以供回测
'''


def extract_mean(file_location, file_name):
    p_col = ['*', '**'] + ['201%d_%s' % (i, j) for i in range(10) for j in ['first', 'mid', 'third', 'final']]
    data = pd.read_excel('%s/%s.xlsx' % (file_location, file_name))
    data.columns = p_col
    target_line = data.shape[0] - 7
    mean_dict = data.iloc[[target_line]].to_dict()
    mean_d = {i: mean_dict[i][target_line] for i in p_col[2:]}

    return mean_d, p_col[2:]


def calculate(d, tl):
    out_list = []
    for i in range(0, 40, 4):
        first = d[tl[i + 0]]
        second = d[tl[i + 1]] - d[tl[i + 0]]
        third = d[tl[i + 2]] - d[tl[i + 1]]
        forth = d[tl[i + 3]] - d[tl[i + 2]]
        out_list += [first, second, third, forth]
    out_list.pop()

    return out_list


def create_index(index, industry):
    extract = extract_mean(index, industry)
    dic, time_list = extract[0], extract[1]
    index_list = calculate(dic, time_list)

    return index_list
