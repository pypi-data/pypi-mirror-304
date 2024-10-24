#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#基础特征提取库
#import tsfresh
#from tsfresh import extract_features, extract_relevant_features, select_features
#from tsfresh.utilities.dataframe_functions import impute
#from tsfresh.feature_extraction import ComprehensiveFCParameters

# 基础数据科学运算库
import numpy as np
import pandas as pd
import seaborn as sns


# 可视化库
#import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from pylab import rcParams
#import statsmodels.api as sm
from tqdm import tqdm

# 时间模块
import time

# sklearn库
# 数据预处理
from sklearn import preprocessing
from sklearn.compose import ColumnTransformer

# 实用函数
from sklearn.metrics import mean_absolute_error as MAE
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate, KFold

# 常用评估器
import xgboost as xgb
import lightgbm as lgb

# 网格搜索
from sklearn.model_selection import GridSearchCV

# re模块相关
import inspect, re

#内存清理库
import gc

#导入优化算法
import hyperopt
from hyperopt import hp, fmin, tpe, Trials, partial
#from hyperopt.early_stop import no_progress_loss
from datetime import date, timedelta

plt.rcParams['font.sans-serif'] = 'SimHei'  #显示中文
plt.rcParams['axes.unicode_minus'] = False  #显示负号

get_ipython().run_line_magic('matplotlib', 'inline')

import warnings
warnings.filterwarnings('ignore')
import sys
sys.setrecursionlimit(100000) #设置递归深度


# In[ ]:


pd.set_option('display.max_row', None)
pd.set_option('display.max_columns', None)


# In[ ]:


train = pd.read_csv('train.csv', index_col=False)
test = pd.read_csv('test.csv', index_col=False)


# In[ ]:


train.shape, test.shape


# In[ ]:


train.head()


# In[ ]:


def missing (df):
    """
    计算每一列的缺失值及占比
    """
    missing_number = df.isnull().sum().sort_values(ascending=False)              # 每一列的缺失值求和后降序排序                  
    missing_percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)          # 每一列缺失值占比
    missing_values = pd.concat([missing_number, missing_percent], axis=1, keys=['Missing_Number', 'Missing_Percent'])      # 合并为一个DataFrame
    return missing_values


# In[ ]:


missing(train)


# In[ ]:


missing(test)


# In[ ]:


def simple_fea_stats(data):
    data['time'] = pd.to_datetime(data['time'])
    #简单特征统计
    data['time'] = data['time'].values.astype('datetime64[s]') #format='%d/%m/%Y'
    #data['year'] = data['time'].dt.year
    data['month'] = data['time'].dt.month
    data['day'] = data['time'].dt.day
    data['hour'] = data['time'].dt.hour
    #data['minute'] = data['time'].dt.minute
    #data['quarte'] = data['time'].dt.quarter
    #data['weekofyear'] = data['time'].dt.isocalendar().week   #提取年当中的周数
    data['weekday'] = data['time'].dt.weekday + 1 #提取周几
    #data['weekend'] = (data['weekday'] > 5).astype(int) 
    data['hour_section'] = (data['hour'] // 6).astype(int)  #进一步创建小时所属每一天的周期，周期以6小时为划分依据：
    return data


# In[ ]:


train = simple_fea_stats(train)
test = simple_fea_stats(test)


# In[ ]:


train.head()


# In[ ]:





# In[ ]:


train.corr()['节能策略是否合理（0为不合理，1为合理）'].sort_values(ascending=False)


# In[ ]:


train.rename(columns={"节能策略是否合理（0为不合理，1为合理）": 'label'}, inplace=True)


# In[ ]:


train.to_csv('train_df.csv',index=False)
test.to_csv('test_df.csv',index=False)


# In[ ]:


train.columns


# In[ ]:


#特征标注
# 离散字段
category_cols = ['覆盖场景', '设备型号', 'month', 'day', 'hour',  'weekday', 'hour_section']

# 连续字段
numeric_cols = ['周边小区群RRC连接平均数_群1', '周边小区群RRC连接平均数_群2', '周边小区群RRC连接平均数_群3',
       '周边小区群RRC连接平均数_群4', '周边小区群RRC连接平均数_群5', '周边小区群RRC连接平均数_群6',
       '周边小区群RRC连接平均数_群7', '周边小区群RRC连接平均数_群8', '周边小区群RRC连接平均数_群9',
       '周边小区群RRC连接平均数_群10', 'RRC平均连接数_补偿小区', 'RRC连接最大数_补偿小区',
       '上行PRB平均利用率_补偿小区', '下行PRB平均利用率_补偿小区', 'PDCCH信道CCE占用率_补偿小区','周边小区群数量']

# 标签
target = 'label'
ID = 'CI'
time = 'time'
add_id = '补偿小区CI'

# 验证是否划分能完全
assert len(category_cols) + len(numeric_cols) + 5 == train.shape[1]


# In[ ]:


train.select_dtypes('object').columns


# In[ ]:


#查看不同的取值
for feature in train[category_cols]:
        print(f'{feature}: {train[feature].unique()}')


# In[ ]:


train[numeric_cols].describe()


# In[ ]:


train.columns


# In[ ]:


train['RRC连接最大数_补偿小区'].mean() + 3 * train['RRC连接最大数_补偿小区'].std()


# In[ ]:


train['RRC连接最大数_补偿小区'].mean() - 3 * train['RRC连接最大数_补偿小区'].std()


# In[ ]:


# RRC连接最大数_补偿小区上四分位数
Q3 = train[numeric_cols].describe()['RRC连接最大数_补偿小区']['75%']
Q3


# In[ ]:


# RRC连接最大数_补偿小区上四分位数
Q1 = train[numeric_cols].describe()['RRC连接最大数_补偿小区']['25%']
Q1


# In[ ]:


# # MonthlyCharges的四分位距
IQR = Q3 - Q1
IQR


# In[ ]:


# 异常值上界
Q3 + 1.5 * IQR


# In[ ]:


# 异常值下界
Q1 - 1.5 * IQR


# In[ ]:


train['RRC连接最大数_补偿小区'].min(), train['RRC连接最大数_补偿小区'].max()


# In[ ]:


test['RRC连接最大数_补偿小区'].min(), test['RRC连接最大数_补偿小区'].max()


# In[ ]:


'''
plt.figure(figsize=(16, 6), dpi=200)
plt.subplot(121)
sns.histplot(train['RRC连接最大数_补偿小区'], kde=True) 
plt.subplot(122)
sns.histplot(test['RRC连接最大数_补偿小区'], kde=True)
'''


# In[ ]:


'''
for i in numeric_cols:
    plt.figure(figsize=(16, 6), dpi=200)
    plt.subplot(121)
    sns.histplot(train['{}'.format(i)], kde=True) 
    plt.subplot(122)
    sns.histplot(test['{}'.format(i)], kde=True)
'''


# In[ ]:


col_1 = ['覆盖类型', '覆盖场景', '设备型号']

fig,axes=plt.subplots(nrows=2,ncols=2,figsize=(16,12), dpi=200)

for i, item in enumerate(col_1):
    plt.subplot(2,2,(i+1))
    ax=sns.countplot(x=item,hue="label",data=train,palette="Blues", dodge=False)
    plt.xlabel(item)
    plt.title("Churn by "+ item)


# In[ ]:


train.head()


# In[ ]:


'''
# 5、平均值进行填充，后续有需要再进行优化处理。
num = ['RRC平均连接数_补偿小区', 'RRC连接最大数_补偿小区','上行PRB平均利用率_补偿小区', 
       '下行PRB平均利用率_补偿小区', 'PDCCH信道CCE占用率_补偿小区']
for col in num:
    train[col] = train[col].fillna(train[col].mean())
    test[col] = test[col].fillna(test[col].mean())
'''


# In[ ]:


'''
cat = ['覆盖场景', '设备型号']
for col in cat:
    train[col] = train[col].fillna
    test[col] = test[col].fillna
'''


# In[ ]:


#train.drop(['覆盖类型'], axis=1, inplace=True)
#test.drop(['覆盖类型'], axis=1, inplace=True)


# In[ ]:


# 字典编码函数
def change_object_cols(se):
    value = se.unique().tolist()
    value.sort()
    return se.map(pd.Series(range(len(value)), index=value)).values


# In[ ]:


#train['覆盖场景'] = train['覆盖场景'].astype(str)


# In[ ]:


# 对首次活跃月份进行编码
#train['覆盖场景'] = change_object_cols(train['覆盖场景'])
#train['设备型号'] = se_map[:train.shape[0]]
#test['设备型号'] = se_map[train.shape[0]:]


# In[ ]:


#train.drop(['覆盖类型', '覆盖场景', '设备型号'], axis=1, inplace=True)
#test.drop(['覆盖类型','覆盖场景', '设备型号'], axis=1, inplace=True)


# In[ ]:


train.info()


# In[ ]:


train.head


# In[ ]:


train.head


# In[ ]:


test.info()


# In[ ]:


test.shape


# In[ ]:


train.to_csv('train_df.csv', index=False)
test.to_csv('test_df.csv', index=False)


# In[ ]:


test.to_csv('test_df.csv', index=False)


# In[ ]:




