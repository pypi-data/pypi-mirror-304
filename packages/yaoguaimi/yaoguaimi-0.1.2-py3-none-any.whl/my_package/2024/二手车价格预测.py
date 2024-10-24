#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from autogluon.tabular import TabularDataset, TabularPredictor
from autogluon.features.generators import AutoMLPipelineFeatureGenerator
import itertools

import pandas as pd
import numpy as np
import copy
import os
from tqdm.notebook import tqdm
from collections import defaultdict
from matplotlib import pyplot as plt
import seaborn as sns
from loguru import logger
from sklearn.model_selection import GridSearchCV,cross_val_score,KFold,train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error


# In[ ]:


Train_data = pd.read_csv('used_car_train_20200313.csv',sep=' ')
Test_data = pd.read_csv('used_car_testB_20200421.csv',sep=' ')
submit = pd.read_csv('used_car_sample_submit.csv',sep=' ')
Train_data['price'] = np.log1p(Train_data['price'])


# In[ ]:


#异常值截断
Train_data.loc[Train_data['power']>600, 'power'] = 600
Train_data.loc[Train_data['power']<1, 'power'] = 1
Test_data.loc[Test_data['power']>600, 'power'] = 600
Test_data.loc[Test_data['power']<0, 'power'] = 1
Train_data.loc[Train_data['v_13']>6, 'v_13'] = 6
Test_data.loc[Test_data['v_13']>6, 'v_13'] = 6
Train_data.loc[Train_data['v_14']>4, 'v_14'] = 4
Test_data.loc[Test_data['v_14']>4, 'v_14'] = 4


# In[ ]:


# 使用 fillna() 方法填充缺失值将含有空值和“-”的值全部替换为
Train_data['notRepairedDamage'] = Train_data['notRepairedDamage'].replace('-', np.nan)
Train_data['notRepairedDamage'].fillna(0, inplace=True)

Test_data['notRepairedDamage'] = Test_data['notRepairedDamage'].replace('-', np.nan)
Test_data['notRepairedDamage'].fillna(0, inplace=True)


# In[ ]:


data = pd.concat([Train_data,Test_data],axis=0).reset_index(drop=True)


# In[ ]:





# In[ ]:


for column in ['name', 'model', 'brand', 'bodyType', 'fuelType', 'gearbox', 'notRepairedDamage','seller']:
    data[column].fillna(data[column].mode()[0], inplace=True)


# In[ ]:


# 假设我们根据观察结果，决定将power分为以下几个桶：
# - 0到75（低功率）
# - 76到150（中等功率）
# - 151到225（较高功率）
# - 226到600（高功率）
bins = [0, 75, 150, 225, 600]
labels = ['Low', 'Medium', 'High', 'Very High']
data['power_bin'] = pd.cut(data['power'], bins=bins, labels=labels, right=False)


# In[ ]:


# 查看'name'字段中最常见的值
top_names = data['name'].value_counts().nlargest(10).index

# 将高频'name'提取出来，其余的归为'Other'
data['name_top'] = data['name'].apply(lambda x: x if x in top_names else 'Other')


# In[ ]:


# 从邮编中提取城市信息，相当于加入了先验知识
data['city'] = data['regionCode'].apply(lambda x : str(x)[:-3])
data = data


# In[ ]:


# 需要转换为类别类型的字段
columns_to_convert = ['name', 'model', 'brand', 'bodyType', 'fuelType', 'gearbox', 'notRepairedDamage','seller','power_bin','name_top','city']

# 将这些字段转换为类别类型
for column in columns_to_convert:
    data[column] = data[column].astype('category')


# In[ ]:


# 定义需要组合的分类特征
categorical_features = ['model', 'brand', 'bodyType', 'fuelType', 'gearbox', 'regionCode', 'offerType']

# 创建特征组合
for i, feature_a in enumerate(categorical_features):
    for feature_b in categorical_features[i+1:]:
        data[f'{feature_a}_{feature_b}'] = data[feature_a].astype(str) + "_" + data[feature_b].astype(str)

# 查看一些新创建的特征组合列


# In[ ]:


# 特征列表
features = ['v_0', 'v_1', 'v_2', 'v_3', 'v_4', 'v_5', 'v_6', 'v_7', 'v_8', 'v_9', 'v_10', 'v_11', 'v_12', 'v_13', 'v_14']

# 生成所有可能的两两组合
combinations = list(itertools.combinations(features, 2))

# 为每对特征组合生成交叉特征
for combo in combinations:
    new_feature_name = f"{combo[0]}_x_{combo[1]}"
    data[new_feature_name] = data[combo[0]] * data[combo[1]]

# 检查新生成的交叉特征
print(data.columns)


# In[ ]:


# 使用时间：data['creatDate'] - data['regDate']，反应汽车使用时间，一般来说价格与使用时间成反比
# 不过要注意，数据里有时间出错的格式，所以我们需要 errors='coerce'
data['used_time'] = (pd.to_datetime(data['creatDate'], format='%Y%m%d', errors='coerce') - 
                            pd.to_datetime(data['regDate'], format='%Y%m%d', errors='coerce')).dt.days


# In[ ]:





# In[ ]:


# 数据分桶 以 power 为例
# 这时候我们的缺失值也进桶了，
# 为什么要做数据分桶呢，原因有很多，= =
# 1. 离散后稀疏向量内积乘法运算速度更快，计算结果也方便存储，容易扩展；
# 2. 离散后的特征对异常值更具鲁棒性，如 age>30 为 1 否则为 0，对于年龄为 200 的也不会对模型造成很大的干扰；
# 3. LR 属于广义线性模型，表达能力有限，经过离散化后，每个变量有单独的权重，这相当于引入了非线性，能够提升模型的表达能力，加大拟合；
# 4. 离散后特征可以进行特征交叉，提升表达能力，由 M+N 个变量编程 M*N 个变量，进一步引入非线形，提升了表达能力；
# 5. 特征离散后模型更稳定，如用户年龄区间，不会因为用户年龄长了一岁就变化

# 当然还有很多原因，LightGBM 在改进 XGBoost 时就增加了数据分桶，增强了模型的泛化性

bin = [i*10 for i in range(31)]
data['power_bin'] = pd.cut(data['power'], bin, labels=False)
data[['power_bin', 'power']].head()


# In[ ]:


#对regDate和creatDate拆分，年月日
data['regDate_y'] = (data['regDate']/10000).astype('int64')
data['regDate_m'] = (data['regDate']/100-data['regDate_y']*100).astype('int64')
data['regDate_d'] = (data['regDate']-data['regDate_m']*100-data['regDate_y']*10000).astype('int64')
data['creatDate_y'] = (data['creatDate']/10000).astype('int64')
data['creatDate_m'] = (data['creatDate']/100-data['creatDate_y']*100).astype('int64')
data['creatDate_d'] = (data['creatDate']-data['creatDate_m']*100-data['creatDate_y']*10000).astype('int64')


# In[ ]:


data['offerType'].isna().any()
data.drop('offerType', axis=1, inplace=True)


# In[ ]:


# 删除不需要的数据
data = data.drop(['creatDate', 'regDate', 'regionCode','SaleID'], axis=1)


# In[ ]:


train_df = data[data['price'].notna()].reset_index(drop=True)
# 标签范围太大不利于神经网络进行拟合，这里先对其进行log变换
test_df = data[data['price'].isna()].reset_index(drop=True)
del test_df['price']


# In[ ]:


test_df.shape


# In[ ]:


label = 'price'
#,eval_metric='mean_absolute_error'


# In[ ]:


predictor = TabularPredictor(label=label,eval_metric='mean_absolute_error').fit(train_df,num_gpus=1, time_limit=10000000,verbosity = 4,presets='best_quality',)#num_bag_folds=6, num_bag_sets=2, num_stack_levels=2,


# In[ ]:


y_pred = predictor.predict(test_df)
y_pred.head()  # Predictions


# In[ ]:


predictor.evaluate(train_df)


# In[ ]:


y_pred_original = np.expm1(y_pred)
submit['price']=y_pred_original


# In[ ]:


submit.to_csv('submit_2_3_4.csv')


# In[ ]:




