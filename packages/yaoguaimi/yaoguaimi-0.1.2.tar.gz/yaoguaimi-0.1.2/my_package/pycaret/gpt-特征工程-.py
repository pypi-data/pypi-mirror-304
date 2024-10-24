#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 特征工程的常用Baseline，包括缺失值处理、类型转换、独热编码、异常值处理、数据平衡、特征选择和归一化
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# 假设我们有一个示例数据集
np.random.seed(42)
data = {
    'feature1': [1, 2, np.nan, 4, 5, np.nan, 7, 8],  # 带有缺失值的数值特征
    'feature2': ['A', 'B', 'A', np.nan, 'B', 'B', 'A', 'C'],  # 带有缺失值的类别特征
    'feature3': [100, 200, 300, 400, 500, 600, 700, 800],  # 数值特征
    'label': [0, 1, 0, 1, 0, 1, 0, 1]  # 标签
}

# 将数据加载为DataFrame
df = pd.DataFrame(data)

# 1. 缺失值处理
# 数值特征使用均值填充，类别特征使用最频繁值填充
num_imputer = SimpleImputer(strategy='mean')
cat_imputer = SimpleImputer(strategy='most_frequent')
df['feature1'] = num_imputer.fit_transform(df[['feature1']])
df['feature2'] = cat_imputer.fit_transform(df[['feature2']])

# 2. 类型转换与独热编码
# 使用OneHotEncoder将类别特征转换为独热编码
encoder = OneHotEncoder(sparse=False, drop='first')
encoded_features = encoder.fit_transform(df[['feature2']])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['feature2']))

# 合并独热编码后的特征到原数据集中
df = pd.concat([df, encoded_df], axis=1)
df.drop('feature2', axis=1, inplace=True)

# 3. 异常值处理
# 简单示例：对于feature3，移除大于600的异常值
df = df[df['feature3'] <= 600]

# 4. 数据归一化和标准化
# 使用StandardScaler对数值特征进行标准化，使用MinMaxScaler进行归一化
scaler_standard = StandardScaler()
scaler_minmax = MinMaxScaler()
df[['feature1', 'feature3']] = scaler_standard.fit_transform(df[['feature1', 'feature3']])
df[['feature1', 'feature3']] = scaler_minmax.fit_transform(df[['feature1', 'feature3']])

# 5. 特征选择
# 使用SelectKBest选择最重要的2个特征
X = df.drop('label', axis=1)
y = df['label']
selector = SelectKBest(score_func=f_classif, k=2)
X_new = selector.fit_transform(X, y)
selected_features = X.columns[selector.get_support()]
print(f"Selected Features: {selected_features}")

# 6. 数据平衡
# 使用随机上采样平衡数据集
from sklearn.utils import resample

df_majority = df[df['label'] == 0]
df_minority = df[df['label'] == 1]

df_minority_upsampled = resample(df_minority,
                                 replace=True,  # 允许重复采样
                                 n_samples=len(df_majority),  # 上采样到多数类的样本数
                                 random_state=42)  # 随机种子

# 合并上采样后的数据集
df_upsampled = pd.concat([df_majority, df_minority_upsampled])
print(f"Balanced Data Label Counts:\n{df_upsampled['label'].value_counts()}")

# 7. 特征工程流水线示例
# 构建一个Pipeline来完成特征工程和模型训练
pipeline = Pipeline([
    ('num_imputer', SimpleImputer(strategy='mean')),  # 数值特征缺失值填充
    ('scaler', StandardScaler()),  # 标准化数值特征
    ('feature_selection', SelectKBest(score_func=f_classif, k=2)),  # 特征选择
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))  # 分类模型
])

# 使用流水线拟合数据并进行预测
X_upsampled = df_upsampled.drop('label', axis=1)
y_upsampled = df_upsampled['label']
pipeline.fit(X_upsampled, y_upsampled)

# 打印流水线中各步骤的名称和参数
print("Pipeline steps and parameters:")
for step_name, step in pipeline.named_steps.items():
    print(f"{step_name}: {step}")


# In[ ]:


from sklearn.decomposition import PCA #主成分分析法

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

from autogluon.tabular import TabularDataset,TabularPredictor
from autogluon.multimodal import MultiModalPredictor

def reduce_mem_usage(df):
    # 处理前 数据集总内存计算
    start_mem = df.memory_usage().sum() / 1024**2 
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    # 遍历特征列
    for col in df.columns:
        # 当前特征类型
        col_type = df[col].dtype
        # 处理 numeric 型数据
        if col_type != object:
            c_min = df[col].min()  # 最小值
            c_max = df[col].max()  # 最大值
            # int 型数据 精度转换
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            # float 型数据 精度转换
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        # 处理 object 型数据
        else:
            df[col] = df[col].astype('category')  # object 转 category
    
    # 处理后 数据集总内存计算
    end_mem = df.memory_usage().sum() / 1024**2 
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df
train_data = reduce_mem_usage(train_data)  # 精度量化

test_data = reduce_mem_usage(test_data)  # 精度量化

