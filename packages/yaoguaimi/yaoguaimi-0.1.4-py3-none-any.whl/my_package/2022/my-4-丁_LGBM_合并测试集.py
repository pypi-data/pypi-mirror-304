#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.decomposition import PCA #主成分分析法
import os
import math
import time
import random
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import roc_auc_score
import json
import warnings
from sklearn import preprocessing
import lightgbm as lgb  
import pickle  
from sklearn.model_selection import train_test_split  
from sklearn.metrics import roc_auc_score, roc_curve,mean_squared_error
from sklearn.model_selection import KFold,GridSearchCV
from sklearn import metrics
from joblib import Parallel, delayed
pd.set_option('display.max_columns',None)
warnings.filterwarnings("ignore")
warnings.warn("once")
from scipy.interpolate import interp1d
from scipy.special import erf, erfinv
from sklearn.preprocessing import QuantileTransformer,PowerTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import FLOAT_DTYPES, check_array, check_is_fitted
 


# In[ ]:


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


# In[ ]:


# 导入数据  
print("Loading Data ... ")  
new_train_data = pd.read_csv('/home/bwfy/桌面/比赛赛集/产品评分数据集/Train.csv')
new_test_data = pd.read_csv('/home/bwfy/桌面/比赛赛集/产品评分数据集/Test.csv')
submi=pd.read_csv('/home/bwfy/桌面/比赛赛集/submision_lgb1.csv')


# In[ ]:


new_train_data=handleOutlier(new_train_data,detect="value", method="median")
new_test_data=handleOutlier(new_test_data,detect="value", method="median")


# In[ ]:


#合并字段
data_all = pd.concat([new_train_data.assign(is_train = 1),new_test_data.assign(is_train = 0)],ignore_index=True) #合并train和test，并且用is_train进行标记
train = data_all['is_train'] == 1##提前进行标记
test  = data_all['is_train'] == 0
print('数据全集量是',len(data_all))
train_count = len(data_all[train])
print('训练集样本量是',train_count)
test_count = len(data_all[test])
print('测试集样本量是',test_count)
print('样本比例为：', train_count/test_count)

#data_all=handleOutlier(data_all,detect="value", method="median")


# In[ ]:


data_all_B = data_all.copy()


# In[ ]:


data_all_B.describe()


# In[ ]:


data_all_B['value'] =   data_all['value']
data_all_B['is_train'] = data_all['is_train']


# In[ ]:


data_all['KPI_A_5']= data_all['KPI_A_5'].astype('category')
data_all['KPI_A_7']= data_all['KPI_A_7'].astype('category')


# In[ ]:


data_all_B.drop(["KPI_A_10",'KPI_A_11','KPI_A_5','KPI_A_7','KPI_A_12',],axis=1,inplace=True)


# In[ ]:


train_data_1 = data_all_B[data_all_B['is_train']== 1]
test_data_1  = data_all_B[data_all_B['is_train']== 0]


# In[ ]:


train_data_1.to_csv('T1_gs_train.csv',index=False)
test_data_1.to_csv('T1_gs_test.csv',index=False)


# In[ ]:


train_data_1 = train_data_1.drop(['is_train'],axis=1)
test_data_1 = test_data_1.drop(['is_train','value'],axis=1)


# In[ ]:


print(submi)


# In[ ]:


test_data_1=test_data_1.reset_index()


# In[ ]:


test_data_1 ['value'] = submi['value']


# In[ ]:


print(test_data_1)


# In[ ]:


train_data_dall = pd.concat([train_data_1.assign(is_train = 1),test_data_1.assign(is_train = 0)],ignore_index=True) #合并train和test，并且用is_train进行标记


# In[ ]:


train_data_dall.to_csv('train_data_dall.csv',index=False)


# In[ ]:


train_data_dall = train_data_dall.drop(['is_train','index'],axis=1)


# In[ ]:


test_data_1 = test_data_1.drop(['value'],axis=1)


# In[ ]:


# 选择相关性大于0.05的作为候选特征参与训练，并加入我们认为比较重要的特征，总共66个特征参与训练
features = (train_data_dall.corr()['value'][abs(train_data_dall.corr()['value'])!='K']).index
features = features.values.tolist()
features.remove('value')
len(features)


# In[ ]:


# 生成数据和标签
target = train_data_dall['value']
train_selected = train_data_dall[features]
test = test_data_1[features]
feature_importance_df = pd.DataFrame()
oof = np.zeros(len(train_data_dall))
predictions = np.zeros(len(test_data_1))


# In[ ]:


print (15**2)


# In[ ]:


params ={#'N_estimator':10000, #3000
         'num_leaves': 197,#最大值不超过 2^'max_depth'# 2**7  800
         'min_data_in_leaf': 40,
         'objective': 'regression',#regression_l1
         'max_depth': 15,#19
         'learning_rate': 0.03,#0.03
         'boosting': 'gbdt',
         'bagging_freq': 0,
         'bagging_fraction': 0.8,   # 每次迭代时用的数据比例0.8
         'feature_fraction': 0.9,# 每次迭代中随机选择80％的参数来建树0.8201
         'bagging_seed': 11,
          'min_data_in_leaf':1,
            'max_bin': 298,
        'lambda_l1': 0,
          'lambda_l2': 0,
    #   'reg_alpha': 1.728910519108444,
       #  'reg_lambda': 4.9847051755586085,
         'random_state': 42,
         'metric': {'mae'},
         'verbosity': -1,
         'subsample': 0.81,
         'min_gain_to_split': 0.01077313523861969,
         'min_child_weight': 19.428902804238373,
         'num_threads': 8,
         'seed':2021}
          #zero_as_missing=true 会将 0 也当作缺失值处理。
kfolds = KFold(n_splits=5,shuffle=True,random_state=15)#15

predictions = np.zeros(len(test))

#categorical_feature=
#cat=['KPI_A_5','KPI_A_7','KPI_A_12','KPI_A_9'] 

for fold_n,(trn_index,val_index) in enumerate(kfolds.split(train_selected,target)):
    print("fold_n {}".format(fold_n))
    trn_data = lgb.Dataset(train_selected.iloc[trn_index],label=target.iloc[trn_index])
    val_data = lgb.Dataset(train_selected.iloc[val_index],label=target.iloc[val_index])
    num_round=100000
    clf = lgb.train(params, trn_data, num_round, valid_sets = [trn_data, val_data],   
                    verbose_eval=1000, early_stopping_rounds = 2000)#categorical_feature=cat
    oof[val_index] = clf.predict(train_selected.iloc[val_index], num_iteration=clf.best_iteration)
    predictions += clf.predict(test,num_iteration=clf.best_iteration)/5
    fold_importance_df = pd.DataFrame()
    fold_importance_df["feature"] = features
    fold_importance_df["importance"] = clf.feature_importance()
    fold_importance_df["fold"] = fold_n + 1
    feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)
    print("CV score: {:<8.5f}".format(mean_squared_error(target, oof)**0.5))


# In[ ]:


cols = (feature_importance_df[["feature", "importance"]]
        .groupby("feature")
        .mean()
        .sort_values(by="importance", ascending=False)[:1000].index)
best_features = feature_importance_df.loc[feature_importance_df.feature.isin(cols)]

plt.figure(figsize=(14,26))
sns.barplot(x="importance", y="feature", data=best_features.sort_values(by="importance",ascending=False))
plt.title('LightGBM Features (averaged over folds)')
plt.tight_layout()


# In[ ]:


### best_features.to_csv('best_features.csv',index=False)


# In[ ]:


# 计算结果
submision_lgb1=test
submision_lgb1['value']=predictions
submision_lgb1['value'].to_csv('submision_lgb2.csv',index=False)

