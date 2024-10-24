#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Qi Zhang
@Software: PyCharm
@Time:2020/3/10 14:23
@File: preprocessing.py
@Function:
@Change: 2020/4/15 10:52
"""

import pandas as pd
import json


# ================================ 分割数据 ================================
def splitData(df, ratio=0.3, random_seed=2333):
    """split csv file.

        Arguments:
            df {dataframe} -- dataframe object
            ratio {float} -- the ratio of df_1/df
            random_seed {int} -- keep same random seed
        Returns:
            df_1 {dataframe} -- dataframe object
            df_2 {dataframe} -- dataframe object

    """
    # df_1, df_2 = train_test_split(df, test_size=(1-ratio),random_state=random_seed)
    lenth = len(df)

    df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)

    index = int(round(lenth * ratio))
    df_1 = df[0:index].reset_index(drop=True)
    df_2 = df[index:lenth].reset_index(drop=True)
    return df_1, df_2


# ================================ 填补空值 ================================
def fillNanList(df, fill_char=None, cols=None, method="median"):
    """fill nan

        Arguments:
            df {dataframe} -- dataframe object
            cols {list of str} -- name list that need to fill nan
            method {str} -- 填充方式，包含中位数，众数，自定义
            fill {str/int/float} -- 自定义填充时,填充的变量
        Returns:
            df {dataframe} -- dataframe object

    """
    if cols is None:
        cols = []
    if not cols:
        # 如果用户没有输入，则填充全部
        cols = df.columns.tolist()
    if method == "median":
        for name in cols:
            if df[name].dtype != 'object':
                # 中位数插补，适用于偏态分布或者有离群点的分布
                df[name].fillna(df[name].dropna().median(), inplace=True)
    elif method == "mode":
        for name in cols:
            # 众数插补，可用于str，int，float
            df[name].fillna(df[name].dropna().mode().iloc[0], inplace=True)
    elif method == 'other' and fill_char:
        for name in cols:
            # 众数插补，可用于str，int，float
            df[name].fillna(fill_char, inplace=True)
    elif method == 'del':
        df.dropna(axis=0, how='any', subset=cols, inplace=True)
    else:
        return IOError
    return df


# ================================ 随机采样 ================================
def samplingData(df, method="number", spl_number=None, spl_ratio=None, replacement=False, random_seed=None):
    """sampling data

            Arguments:
                df {dataframe} -- dataframe object
                number {int} -- Number of items from axis to return. Cannot be used with frac.
                ratio {float} -- Sampling rate
                replace { boolean} -- Sample with or without replacement. Default = False.
                random_state {int/numpy} -- Seed for the random number generator (if int), or numpy RandomState object.
            Returns:
                df {dataframe} -- new dataframe object

    """
    # print(method)
    # print(df)

    if method == "ratio":
        df_1 = df.sample(frac=spl_ratio, replace=replacement, random_state=random_seed).reset_index(drop=True)
    elif method == "number":
        df_1 = df.sample(n=spl_number, replace=replacement, random_state=random_seed).reset_index(drop=True)
    else:
        df_1 = df
    return df_1


# ================================ 根据表达式过滤数据 ================================
def filterData(df, param_json):
    """
    :param df: 传入数据
    :param param_json: 传入参数
    :return:返回数据
    """

    columnName = param_json["columnName"] if "columnName" in param_json else None
    operator = param_json["operator"] if "operator" in param_json else None
    value = param_json["value"] if "value" in param_json else None
    if columnName is not None and operator is not None and value is not None:
        functionChar = "df = df[df[columnName]" + operator + str(value) + "].reset_index(drop=True)"

        scop = {"columnName": columnName,
                "operator": operator,
                "value": value,
                "df": df}
        exec(functionChar, scop)
        df = scop["df"]

    return df


# ================================ 重复数据删除 ================================
def dropDuplicate(df):
    """
    drop duplicated data
               Arguments:
                   df {dataframe} -- dataframe object
               Returns:
                   df_1 {dataframe} -- new dataframe object
     """

    df_1 = df.drop_duplicates().reset_index(drop=True)
    return df_1


# ================================ 异常值检测 ================================

def handleOutlier(df, cols=None, detect="value", method="median"):
    if not cols:
        # 如果用户没有输入，则填充全部
        cols = df.columns.tolist()
    if detect == "value":
        if method == "median":
            for name in cols:
                if df[name].dtype != 'object':
                    # 中位数插补，适用于偏态分布或者有离群点的分布
                    med = df[name].median()
                    mean = df[name].mean()
                    std = df[name].std()

                    df[name] = df[name].map(lambda x: med if abs(x - mean) > 3 * std else x)
        elif method == "mode":
            for name in cols:
                # 众数插补，可用于str，int，float
                if df[name].dtype != 'object':
                    mode = df[name].mode()[0]
                    mean = df[name].mean()
                    std = df[name].std()

                    df[name] = df[name].map(lambda x: mode if abs(x - mean) > 3 * std else x)
        else:
            return IOError
    elif detect == "frequency":
        # 根据数据出现频率检测异常值
        # 待添加
        return df
    return df


def dataDescribe(df):
    """
    数据描述信息
    """
    cols = df.dtypes
    cols_object = cols.loc[cols.map(lambda x: x == object)].index.tolist()
    cols = cols.loc[cols.map(lambda x: x != object)].index.tolist()
    dfNew = pd.DataFrame(columns=cols)
    for col in cols:
        dfNew[col] = pd.Series([df[col].sum(), df[col].count(),
                                df[col].min(), df[col].idxmin(),
                                df[col].max(), df[col].idxmax(),
                                df[col].median(), df[col].mean(),
                                df[col].var(), df[col].std(),
                                df[col].mad(), df[col].skew(), df[col].kurt(),
                                df[col].quantile(.25), df[col].quantile(.50), df[col].quantile(.75)
                                ],
                               )
    for col in cols_object:
        dfNew[col] = pd.Series([df[col].count(), df[col].count(),
                                df[col].value_counts().max(), df[col].value_counts().idxmax(),
                                df[col].value_counts().min(), df[col].value_counts().idxmin(),
                                'Nan', 'Nan',
                                'Nan', 'Nan', 'Nan',
                                'Nan', 'Nan', 'Nan']
                               )
    dfName = pd.DataFrame({"name": ['sum', 'counts',
                                    'min', 'minIndex',
                                    'max', 'maxIndex',
                                    'median', 'mean',
                                    'var', 'std',
                                    'mad', 'skew', 'kurt',
                                    '25', '50', '75', ]})
    #     name=['数据和', '非空元素总数',
    #              '最小值', '最小值的位置',
    #              '最大值', '最大值的位置',
    #              '中位数', '均值',
    #              '方差', '标准差',
    #              '平均绝对偏差', '偏度', '峰度',
    #              '四分之一分位数', '四分之二分位数', '四分之三分位数',
    #                                    ]
    dfNew = pd.concat([dfName, dfNew], axis=1)

    return dfNew


def delData(df, cols=None):
    """
    按列名cols里，进行删除

    :param df:
    :param cols: list,列名得集合
    :return:
    """

    if cols is None:
        cols = []
    df = df.drop(cols, axis=1)

    return df


# ================================ 归一化 ================================
def minMaxScale(df, cols, new_min=0, new_max=1):
    """Scale the element of df into an interval [new_min, new_max].
        the default

       Arguments:
           df {dataframe} -- dataframe object
           cols {list}  --
           new_max {int/float} -- upper limit of new interval
           new_min {int/float} -- lower limit of new interval

       Returns:
           dataframe -- dataframe object
       """

    for col in cols:
        if df[col].max() != df[col].min():
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) * (
                    new_max - new_min) + new_min
        else:
            df[col] = 0

    return df


# ================================ 标准化 ================================
def standardizeData(df, cols):
    """Scale the element of df as standardize function.

        Arguments:
           df {dataframe} -- dataframe object


       Returns:
           dataframe -- dataframe object
        """
    for col in cols:
        if df[col].std() != 0:
            df[col] = (df[col] - df[col].mean()) / df[col].std()
        else:
            df[col] = 0
    return df


# ================================ 文字改为数字代替 ================================
# 读取训练时，保存的数值映射关系
def cate2Num(data, _categorical_path):
    # files = glob.glob(_categorical_path+'*.txt') #得到文件夹下的所有文件名称
    # noinspection PyBroadException
    try:
        with open(_categorical_path, "r", encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        for k, v in json_data.items():
            # print(k,v)
            if k in data:
                data[k] = data[k].map(lambda x: x if x in v else -1)
                data[k] = data[k].astype(object)
                data[k] = data[k].replace(v, list(range(len(v))))
    except Exception:
        pass
    return data


# ================================ 数字函数变换 ================================
# 很多数字函数对于x的值，有域的要求
# 其中log，sqrt都需要x>0，针对这些函数，小于0的直接赋值为0
def tran_math_function(df, name_function, cols=None):
    """
    @param df: 数据集
    @param name_function: 函数名字
    @param cols: 需要处理的列
    @return:
    """
    if cols is None:
        cols = []
    import math
    math_relation = {
        "sin": math.sin,
        "cos": math.cos,
        "log": math.log,
        "sqrt": math.sqrt,
        "exp": math.exp,
        "round": round,
        "abs": abs
    }
    if name_function == "log" or "sqrt":
        # 针对log与sqrt，需要单独处理
        for col in cols:
            df[col] = df[col][df[col] > 0].apply(math_relation[name_function])
            df[col].fillna(0, inplace=True)
    else:
        for col in cols:
            df[col] = df[col].apply(math_relation[name_function])
    return df


def discrete(data, _dsct_path):
    """
    如果是不在范围的修改为-1
    数据离散化通用
    @param data: 数据集
    @param _dsct_path: 区间地址
    @return:
    """
    # noinspection PyBroadException
    try:
        with open(_dsct_path, "r", encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        old_col = json_data["old_col"]
        new_col = json_data["new_col"]
        group = json_data["group"]
        types = json_data["types"]
        if types == 1:
            data[new_col] = data[old_col]
            group_chain = []
            list(map(group_chain.extend, group))
            data[new_col] = data[new_col].map(lambda x: str(-1) if x not in group_chain else x)
            for i in range(len(group)):
                data[new_col].replace(group[i], str(i), inplace=True)  # 如果碰到是字符1,2,3这种的替换,会出问题,需要优化

        elif types == 2:
            data[new_col] = pd.cut(data[old_col], bins=group, labels=False, right=True, include_lowest=False)
        elif types == 3:
            data[new_col] = data[old_col]
        data[new_col] = data[new_col].fillna(-1)
        data[new_col] = data[new_col].map(lambda x: int(x))
    except Exception:
        pass
    return data


def onehot_map(data, _onehot_path):
    """
    onehot 处理函数
    如果不在历史数据中的值,不会生成新列,而是作为缺失值填充nan列
    @param data: 数据集
    @param _onehot_path: onehot 数据地址
    @return:
    """
    # noinspection PyBroadException
    try:
        with open(_onehot_path, "r", encoding='utf-8') as json_file:
            one_hot_relation = json.load(json_file)

        for column, values in one_hot_relation.items():
            for name in values:
                data[column + "_" + name] = data[column].map(lambda x: 1 if x == name else 0)
            data[column + "_nan"] = data[column].map(lambda x: 1 if str(x) not in values else 0)
    except Exception:
        pass
    return data


def binary_map(data, cols, threshold):
    """
    二值化编码
    @param data:
    @param cols:
    @param threshold:
    @return:
    """
    for col in cols:
        data[col + "_binary"] = data[col].apply(lambda x: 1 if x >= threshold else 0)
    return data


def map_func(x, map_data):
    """
    apply 使用的函数
    如果数据在map_data中,则进行修改,否则不修改
    @param x: 传入的数据
    @param map_data:
    @return:
    """
    x = map_data[x] if x in map_data else x
    return x


def map_dict_tran(data, col, map_data, map_type=0, custom_value=-1, replaced=False):
    """
    字典映射
    @param data:
    @param col:
    @param map_data:
    @param map_type: 0:默认零,表示对于不存在与字典数据中的不做处理.
                        1:表示对于不存在于字典数据中的赋值为custom_value
    @param custom_value:
    @param replaced: 是否替代原先的列,如果否,则生成新的列,名字为  col+"_map"
    @return:
    """

    new_col = col + "_map"
    if replaced:
        new_col = col
    if map_type == 0:
        # apply 中args为传入数据,
        data[new_col] = data[col].apply(map_func, args=(map_data,))
    elif map_type == 1:
        data[new_col] = data[col].map(map_data)
        data[new_col].fillna(custom_value)
    return data


def deal_data(df, label, cols, number):
    """
    针对数据做一些处理
    @param df:
    @param label:
    @param cols:
    @param number:
    @return:
    """
    # 如果目标列是描述变量，转换为数字进行计算
    df_label = df[label].copy()
    if df[label].dtype == "object":
        # 如果是描述变量，则转换
        data_col = pd.factorize(df[label])
        data_col_df = pd.DataFrame(data_col[0], columns=[label])
        del df[label]  # 删除原来的列
        df = pd.concat([data_col_df, df], axis=1)

    cols_dict = df[cols].dtypes
    # 字符型不能计算得分，因此需要分开
    cols_object = cols_dict.loc[cols_dict.map(lambda x: x == object)].index.tolist()
    cols_number = cols_dict.loc[cols_dict.map(lambda x: x != object)].index.tolist()
    # 判断选择保留列数量-number是否大于选择列的个数
    number = len(cols_number) if number > len(cols_number) else number
    df[cols_number] = df[cols_number].fillna(0)
    df[label] = df[label].fillna(0)
    return df, df_label, number, cols_object, cols_number


def pca_selection(data, select_cols, labels, numbers, pca_path):
    """
    pca降维
    pca降维只支持数值化数据的计算,如果是字符数据,会出现问题
    @param data:
    @param select_cols:
    @param labels:
    @param numbers:
    @param pca_path: pca模型的路径
    @return:
    """

    import joblib
    pca = joblib.load(pca_path)
    df, df_label, number, cols_object, cols_number = deal_data(data, labels, select_cols, numbers)
    df_select = pd.DataFrame(pca.transform(df[cols_number]))
    df_select = df_select.add_suffix("_pca")
    df_all = pd.concat([df[cols_object], df_select, df_label], axis=1)
    return df_all


def get_data(es, data, cols, data_id, name="root"):
    """

    @param es:
    @param data:
    @param cols:
    @param data_id:
    @param name:
    @return:
    """
    data_part = data[cols]
    data_part.drop_duplicates(keep='last', inplace=True)
    flag = data_part[data_id].duplicated()
    if flag.any():
        es = es.entity_from_dataframe(entity_id=name, dataframe=data_part,
                                      make_index=True, index=name + "_id")

    else:
        es = es.entity_from_dataframe(entity_id=name, dataframe=data_part,
                                      index=data_id)
    return es, data


def dfs_feature(data, root_cols, sub_cols, root_id, sub_id, relation_col):
    """

    @param data:
    @param root_cols:
    @param sub_cols:
    @param root_id:
    @param sub_id:
    @param relation_col:
    @return:
    """
    import featuretools as ft

    es = ft.EntitySet(id='dfs')
    es, root_data = get_data(es, data, root_cols, root_id, "root")
    es, sub_data = get_data(es, data, sub_cols, sub_id, "sub")
    r_client_previous = ft.Relationship(es['root'][relation_col],
                                        es['sub'][relation_col])
    es = es.add_relationship(r_client_previous)

    # Perform deep feature synthesis without specifying primitives
    data, feature_names = ft.dfs(entityset=es, target_entity='root', max_depth=2)
    data = data.reset_index()
    return data


def discrete_time(data, time_col):
    """

    @param data:
    @param time_col:
    @return:
    """
    data[time_col] = pd.to_datetime(data[time_col])
    data['Year'] = data[time_col].apply(lambda d: d.year)
    data['Month'] = data[time_col].apply(lambda d: d.month)
    data['Day'] = data[time_col].apply(lambda d: d.day)
    data['DayOfWeek'] = data[time_col].apply(lambda d: d.dayofweek)
    data['DayName'] = data[time_col].apply(lambda d: d.day_name())
    data['DayOfYear'] = data[time_col].apply(lambda d: d.dayofyear)
    data['WeekOfYear'] = data[time_col].apply(lambda d: d.weekofyear)
    # data['Quarter'] = data[time_col].apply(lambda d: d.quarter)
    data['Hour'] = data[time_col].apply(lambda d: d.hour)
    data['Minute'] = data[time_col].apply(lambda d: d.minute)
    data['Second'] = data[time_col].apply(lambda d: d.second)
    data['MU_second'] = data[time_col].apply(lambda d: d.microsecond)  # 毫秒
    # data['UTC_offset'] = data[time_col].apply(lambda d: d.utcoffset())  # UTC时间位移
    # hour_bins = [-1, 5, 11, 16, 21, 23]
    # bin_names = ['Late Night', 'Morning', 'Afternoon', 'Evening', 'Night']
    # data['Hour'] = data[time_col].apply(lambda d: d.hour)
    # data['TimeOfDayBin'] = pd.cut(data['Hour'], bins=hour_bins, labels=bin_names)
    data[time_col] = data[time_col].map(lambda x: str(x))
    return data


def statistics_time(data, time_col, id_col):
    """

    @param data:
    @param time_col: 时间标识列
    @param id_col: 数据id
    @return:
    """
    from tsfresh import extract_features

    extract_data = extract_features(data, column_id=id_col, column_sort=time_col)
    return extract_data


def merge_data(data, data_part, time_col, value_col, name):
    """
    合并数据
    @param data:
    @param data_part:
    @param time_col:
    @param value_col:
    @param name:
    @return:
    """
    data_part.columns = [time_col, value_col + name]
    data_part[time_col] = data_part[time_col].map(lambda x: str(x))
    data = pd.merge(data, data_part, how='left', on=time_col)
    return data


def continue_time(data, time_col, value_col):
    """

    @param data:
    @param time_col: 时间标识列
    @param value_col: 数据列
    @return:
    """

    from statsmodels.tsa.seasonal import seasonal_decompose
    # 数据按时间排序
    data[time_col] = pd.to_datetime(data[time_col])
    data = data.sort_values(by='TravelDate')
    data_value = data[value_col]
    data_value = data.set_index(time_col)
    # 分解数据
    decomposition = seasonal_decompose(data_value)
    # 合并数据集
    data[time_col] = data[time_col].map(lambda x: str(x))
    trend = decomposition.trend.reset_index()
    data = merge_data(data, trend, time_col, value_col, "_trend")
    seasonal = decomposition.seasonal.reset_index()
    data = merge_data(data, seasonal, time_col, value_col, "_seasonal")
    residual = decomposition.resid.reset_index()
    data = merge_data(data, residual, time_col, value_col, "_residual")
    # data[time_col] = pd.to_datetime(data[time_col])
    return data

