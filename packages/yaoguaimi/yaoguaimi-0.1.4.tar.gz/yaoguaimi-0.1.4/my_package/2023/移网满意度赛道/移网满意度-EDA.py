#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.decomposition import PCA #主成分分析法
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.ensemble import GradientBoostingClassifier
#from yellowbrick.features import FeatureImportances
from sklearn.linear_model import LogisticRegression
#from yellowbrick.features import ParallelCoordinates
from sklearn.model_selection import train_test_split
#from yellowbrick.features import parallel_coordinates,PCADecomposition
#from yellowbrick.classifier import classification_report
from sklearn.linear_model import Ridge
#from yellowbrick.regressor import PredictionError
import os
import math
import time
import random
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras as K
from tensorflow.keras import Sequential, utils, regularizers, Model, Input
from tensorflow.keras.layers import Flatten, Dense, Conv1D, MaxPool1D, Dropout, AvgPool1D
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import KFold
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import roc_auc_score
import json
import warnings
from sklearn import preprocessing
import lightgbm as lgb  
import pickle  
from sklearn.model_selection import train_test_split  
from preprocessing import filterData, delData, fillNanList, dropDuplicate,\
    handleOutlier, minMaxScale, cate2Num,standardizeData,\
    discrete, tran_math_function, minMaxScale, standardizeData,\
    onehot_map, map_dict_tran, binary_map, pca_selection,dfs_feature,\
    continue_time, discrete_time, statistics_time

from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from catboost import CatBoostRegressor
pd.set_option('display.max_columns',None)
warnings.filterwarnings("ignore")


# ## 一、导入数据

# In[ ]:


# 导入数据  
print("Loading Data ... ")  
train_data = pd.read_csv('train_data.csv')
test_data = pd.read_csv('test_data.csv')



# ## 二、初步探索

# ### 1、 基本描述

# In[ ]:


train_data.describe()


# In[ ]:


train_data.head(1)


# In[ ]:


train_data.shape


# In[ ]:


train_data.info(verbose=True, null_counts=True)


# In[ ]:


# 设置显示的最大列、宽等参数，消掉打印不完全中间的省略号

# pd.set_option('display.max_columns', 1000)

pd.set_option('display.width', 1000)#加了这一行那表格的一行就不会分段出现了

# pd.set_option('display.max_colwidth', 1000)

# pd.set_option('display.height', 1000)

#显示所有列

pd.set_option('display.max_columns', None)

#显示所有行

pd.set_option('display.max_rows', None)


# ### 2、 nuique、缺失值统计

# In[ ]:


stats = []
for col in train_data.columns:
    stats.append((col,train_data[col].nunique(),
                  train_data[col].isnull().sum()*100 / train_data.shape[0],
                  train_data[col].value_counts(normalize=True,
                  dropna=False).values[0]*100,train_data[col].dtype))
    stats_df = pd.DataFrame(stats,columns=['Feature','Unique_values',
                            'Percentage of missing values',
                            'Percentage of values in the biggest category','type'])
stats_df.sort_values('Percentage of missing values',ascending=False)[:113]


# In[ ]:


##########################train集统计和可视化缺失值##########################
missing=train_data.isnull().sum().reset_index().rename(columns={0:'missNum'})
missing['missRate']=missing['missNum']/train_data.shape[0]
# 按照缺失率排序显示
miss_analy=missing[missing.missRate>0].sort_values(by='missRate',ascending=False)
fig = plt.figure(figsize=(30,10))
plt.bar(np.arange(miss_analy.shape[0]), list(miss_analy.missRate.values), align = 'center',color=['red','green','yellow','steelblue']) 
plt.title('Histogram of missing value of variables')
plt.xlabel('variables names')
plt.ylabel('missing rate')
# 添加x轴标签，并旋转90度
plt.xticks(np.arange(miss_analy.shape[0]),list(miss_analy['index']))
plt.xticks(rotation=90)
# 添加数值显示
for x,y in enumerate(list(miss_analy.missRate.values)):
    plt.text(x,y+0.12,'{:.2%}'.format(y),ha='center',rotation=90)    
plt.ylim([0,1.2])
plt.show()


# ##  三、变量分析

# ### 1、单变量分析

# #### 1.1 标签

# In[ ]:


#基本信息
train_data['score'].describe()


# In[ ]:


#标签分布
plt.figure(figsize=(9,8))
sns.distplot(train_data['score'],color='g',bins=100,hist_kws={'alpha':0.4})


# In[ ]:


#对数转换
plt.figure(figsize=(9,8))
sns.distplot(np.log(train_data['score']),color='g',bins=100,hist_kws={'alpha':0.4})


# #### 1.2 连续值变量

# In[ ]:


####分布情况
df_num = train_data.select_dtypes(include = ['float64'])
df_num = df_num[df_num.columns.tolist()[1:10]]
df_num.hist(figsize=(16,20),bins=50,xlabelsize=8,ylabelsize=8)


# In[ ]:


####相关性分析
corrmat = train_data.corr()
f,ax = plt.subplots(figsize=(100,17))
sns.heatmap(corrmat,vmax=0.8,square=True)


# #### 1.3 类别型变量

# In[ ]:


####分布情况
df_num = train_data.select_dtypes(include = ['object','int64'])
df_num = df_num[df_num.columns.tolist()[1:10]]
df_num.hist(figsize=(16,20),bins=50,xlabelsize=8,ylabelsize=8)


# ### 2、多变量分析

# In[ ]:


# 检查缺失情况
train_data.isnull().sum()


# In[ ]:


test_data.isnull().sum()


# In[ ]:


# 以first_active_month为例分析训练集与测试集的差异
features = test_data.columns.values.tolist() 
train_count = train_data.shape[0]
test_count = test_data.shape[0]
for feature in features:
    train_data[feature].value_counts().sort_index().plot()
    test_data[feature].value_counts().sort_index().plot()
    plt.xlabel(feature)
    plt.legend(['train','test'])
    plt.ylabel('count')
    plt.show()
#结论：训练集与测试集在所有单变量上的绝对数量分布形状极其相似，需要进一步查看相对占比分布


# In[ ]:


# 为了查看多变量的联合分布，通常来说可以使用散点图，但这里的四个特征均是离散特征，因此散点图不太适合
# 继续延续上面画单变量图的思想，参赛者可以通过将两个变量拼到一起转变为单变量的分布
def combine_feature(df):
    cols = df.columns
    feature1 = df[cols[0]].astype(str).values.tolist()
    feature2 = df[cols[1]].astype(str).values.tolist()
    return pd.Series([feature1[i]+'&'+feature2[i] for i in range(df.shape[0])])
n = len(features)
for i in range(n-1):
    for j in range(i+1, n):
        cols = [features[i], features[j]]
        print(cols)
        train_dis = combine_feature(train_data[cols]).value_counts().sort_index()/train_count
        test_dis = combine_feature(test_data[cols]).value_counts().sort_index()/test_count
        index_dis = pd.Series(train_dis.index.tolist() + test_dis.index.tolist()).drop_duplicates().sort_values()
        (index_dis.map(train_dis).fillna(0)).plot()
        (index_dis.map(train_dis).fillna(0)).plot()
        plt.legend(['train','test'])
        plt.xlabel('&'.join(cols))
        plt.ylabel('ratio')
        plt.show()
# 结论：修正上述遗漏后参赛者可以发现训练集与测试集的两变量联合分布也基本保持一致，由此基本可以判定，训练集与测似集
# 的生成方式基本一摸一样，即测试集与训练集是同一批数据随机划分后的结果，有兴趣的参赛者可继续验证三变量和四变量分布。假定
# 关于验证集与测试集的这一猜想成立，会极大地增添参赛者后续进行特征工程的信心，对建模方式也会有一个整体把握。


# In[ ]:




