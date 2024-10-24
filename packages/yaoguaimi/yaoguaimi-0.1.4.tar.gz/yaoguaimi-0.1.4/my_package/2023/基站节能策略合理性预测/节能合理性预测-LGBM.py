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


# In[ ]:


# 导入数据  
print("Loading Data ... ")  
train_data = pd.read_csv('train_去重_时间特征.csv')
test_data = pd.read_csv('test_去重_时间特征.csv')


# In[ ]:


#train_data = train_data.drop(['CI','Year','Month','DayOfWeek','DayOfYear','Minute','Second','MU_second','WeekOfYear'], axis=1)
#test_data = test_data.drop(['CI','Year','Month','DayOfWeek','DayOfYear','Minute','Second','MU_second','WeekOfYear'], axis=1)

train_data = train_data.drop(['CI','day','dayPart','节能策略是否合理（0为不合理，1为合理）','time'], axis=1)
test_data = test_data.drop(['CI','day','dayPart','time'], axis=1)


# In[ ]:


data_all = train_data.copy()


# In[ ]:


data_all.shape


# In[ ]:


df_bak = data_all.copy()


# In[ ]:


#data_target = data_all['节能策略是否合理（0为不合理，1为合理）']
data_target = data_all['label']


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(12,12))
x = train_data['label'].value_counts().index.values
y = train_data["label"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


data_all.shape


# In[ ]:


data_all['label'] = data_target


# In[ ]:


df = data_all[data_all['label'].notnull()]


# In[ ]:


df.shape


# In[ ]:


df.info(verbose=True, null_counts=True)


# In[ ]:


newdf = df.copy()


# In[ ]:


'''
newdf['覆盖类型'] = newdf['覆盖类型'].astype('category')
newdf['覆盖场景'] = newdf['覆盖场景'].astype('category')
newdf['设备型号'] = newdf['设备型号'].astype('category')
newdf['补偿小区CI'] = newdf['补偿小区CI'].astype('category')
newdf['hour'] = newdf['hour'].astype('category')
newdf['weekday'] = newdf['weekday'].astype('category')
newdf['hour_section'] = newdf['hour_section'].astype('category')
#newdf['dayPart'] = newdf['dayPart'].astype('category')


test_data['覆盖类型'] = test_data['覆盖类型'].astype('category')
test_data['覆盖场景'] = test_data['覆盖场景'].astype('category')
test_data['设备型号'] = test_data['设备型号'].astype('category')
test_data['补偿小区CI'] = test_data['补偿小区CI'].astype('category')
test_data['hour'] = test_data['hour'].astype('category')
test_data['weekday'] = test_data['weekday'].astype('category')
test_data['hour_section'] = test_data['hour_section'].astype('category')
#test_data['dayPart'] = test_data['dayPart'].astype('category')

'''


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = newdf['label'].value_counts().index.values
y = newdf["label"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


newdf.info(verbose=True, null_counts=True)
from sklearn.model_selection import train_test_split
X=newdf
y=newdf['label']
train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.2,random_state=2022)
print(test_x.shape)
print(train_x.shape)
print(test_y.shape)


# In[ ]:


train_x['label'] = train_y


# In[ ]:





# In[ ]:


cat=['覆盖类型','覆盖场景','设备型号','hour','weekday','hour_section','补偿小区CI'] 


# In[ ]:





# In[ ]:


# 选择相关性大于0.05的作为候选特征参与训练，并加入我们认为比较重要的特征，总共66个特征参与训练
#features = (train_data.corr()['score'][abs(train_data.corr()['score'])!='K']).index
features = train_data.columns.values.tolist()
features.remove('label')
len(features)


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(12,12))
x = train_data['label'].value_counts().index.values
y = train_data["label"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


#train_data['score'][train_data['score'] < 2] =1
#train_data['score'][train_data['score'] > 8] =0
#train_data = train_data[(train_data['score'] == 1) | (train_data['score'] ==0)]


# In[ ]:


# 生成数据和标签
target = train_data['label']
train_selected = train_data[features]
test = test_data[features]
feature_importance_df = pd.DataFrame()
oof = np.zeros(len(train_data))
predictions = np.zeros(len(test_data))
#train_selected['group'] = train_data['group']
#test['group'] = test_data['group']


# In[ ]:


#train_selected['group']=train_selected['group'].fillna(0)
#test['group']=test['group'].fillna(0)


# In[ ]:


#train_selected=train_selected.fillna(0)
#test=test.fillna(0)


# In[ ]:





# In[ ]:





# In[ ]:


train_selected.info(verbose=True, null_counts=True)


# In[ ]:


train_selected.shape


# In[ ]:


test.shape


# In[ ]:


params = {'num_leaves': 95,
         'min_data_in_leaf': 40,
         'objective': 'binary',
         'max_depth': 16,
         'learning_rate': 0.01,
         'boosting': 'gbdt',
         'bagging_freq': 5,
         'bagging_fraction': 0.8,   # 每次迭代时用的数据比例0.8
         'feature_fraction': 0.8201,# 每次迭代中随机选择80％的参数来建树0.8201
         'bagging_seed': 11,
         'reg_alpha': 1.728910519108444,
         'reg_lambda': 4.9847051755586085,
         'random_state': 42,
         'max_bin':1023,
        #'metric': 'f1',
         'verbosity': -1,
         'subsample': 0.81,
         'min_gain_to_split': 0.01077313523861969,
         'min_child_weight': 19.428902804238373,
         'num_threads': 4,
         'seed':2021}
       

kfolds = KFold(n_splits=5,shuffle=True,random_state=15)
predictions = np.zeros(len(test))


for fold_n,(trn_index,val_index) in enumerate(kfolds.split(train_selected,target)):
    print("fold_n {}".format(fold_n))
    trn_data = lgb.Dataset(train_selected.iloc[trn_index],label=target.iloc[trn_index])
    val_data = lgb.Dataset(train_selected.iloc[val_index],label=target.iloc[val_index])
    num_round=100000
    clf = lgb.train(params, trn_data, num_round, valid_sets = [trn_data, val_data], verbose_eval=1000, early_stopping_rounds = 8000,categorical_feature=cat)
    oof[val_index] = clf.predict(train_selected.iloc[val_index], num_iteration=clf.best_iteration)
    predictions += clf.predict(test,num_iteration=clf.best_iteration)/5
    fold_importance_df = pd.DataFrame()
    fold_importance_df["feature"] = features
    fold_importance_df["importance"] = clf.feature_importance()
    fold_importance_df["fold"] = fold_n + 1
    feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)
    #print("CV score: {:<8.5f}".format(mean_squared_error(target, oof)**0.5))


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


best_features.to_csv('赛题2_best_features.csv',index=False)


# In[ ]:


# 计算结果
submision_lgb1=test
submision_lgb1['value']=predictions
submision_lgb1['value'].to_csv('赛题2-submision_lgb1.csv',index=False)



# In[ ]:


predictions_lgb_R = submision_lgb1['value'].round(0)

predictions_lgb_R.to_csv('赛题2-predictions_lgb_R.csv',index=False)


# In[ ]:


print(predictions)


# In[ ]:


test_data=pd.DataFrame()
test_data['label'] = submision_lgb1['value'].apply(lambda x:1 if x>0.54 else 0) #[1 0] [4565 1837]


#test_data['label'] = pred_test
plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = test_data['label'].value_counts().index.values
y = test_data['label'].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:





# In[ ]:


test_data['label'].to_csv('赛题2_Day10_lgbm_0.54_1911.csv',index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




