#!/usr/bin/env python
# coding: utf-8

# # 赛事背景
# 
# 房屋租赁市场是房地产市场的重要组成部分。中国城市化进程的加剧，导致一二线城市房价不断攀升，越来越多的人选择以房屋租赁的方式来满足住房的需求。价格是反映一定时期内房屋租赁价格水平变动趋势和变动程度，分析预测房屋租赁价格，对于发展完善房屋租赁市场有着重要的意义。
# 
# 据统计，中国有近2亿租房人口，租户偏好千变万化，房源种类各不相同。如何高效且合理的解决房屋价值预估，成为各大平台关注的问题。某租房平台将部分房屋信息数据开放，诚邀大家帮助他们建立价格预测模型来预测房屋租赁价格（敏感信息已脱敏）。
# 
# ## 赛事任务
# 
# 给定某租房平台实际业务中的相关租房信息，包含31个与房屋相关的字段，其中“房屋租金”字段为房屋信息的真实基本租金，即不包含服务费、电费、水费和燃气费等。任务目标是通过训练集训练模型，来预测测试集中“房屋租金”字段的具体值，以此为依据，提高房屋价值预估准确率。
# 
# ## 数据说明
# 
# 赛题数据由训练集和测试集组成，总数据量超过30w，包含31个特征字段。为了保证比赛的公平性，将会从中抽取20万条作为训练集，5万条作为测试集，同时会对部分字段信息进行脱敏。
# 
# ```
# ID、区域1、区域2、区域3、街道、上传日期、服务费、供暖费用、电力基础价格、有阳台、没有停车位、有厨房、有地窖、居住面积、房屋状况、内饰质量、可带宠物、加热类型、有电梯、房屋类型、邮政编码、房间数量、所处楼层、建筑楼层、有花园、最后翻新年份、是新建筑、建成年份、价格趋势、上传图片、房屋租金
# ```

# # 数据读取

# In[ ]:


import pandas as pd
import seaborn as sns

get_ipython().run_line_magic('pylab', 'inline')


# In[ ]:


train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')


# In[ ]:


train_df.head()


# # 数据分析

# ## 房屋租金

# In[ ]:


train_df['房屋租金'].max()


# In[ ]:


train_df[train_df['房屋租金'] > train_df['房屋租金'].quantile(0.999)].head(1)


# ## 缺失值分析

# In[ ]:


train_df.isnull().mean(0)


# ## 相关性分析

# In[ ]:


train_df.corr()['房屋租金']


# ## 探索性分析

# In[ ]:


train_df.groupby(['区域1'])['房屋租金'].mean().plot(kind='bar')


# In[ ]:


train_df.groupby(['有花园'])['房屋租金'].mean()


# # 特征编码

# In[ ]:


train_df.dtypes


# In[ ]:


train_df['上传日期_day'] = train_df['上传日期'].apply(lambda x: int(x[-2:]))
test_df['上传日期_day'] = test_df['上传日期'].apply(lambda x: int(x[-2:]))


# In[ ]:


train_df['上传日期_month'] = train_df['上传日期'].apply(lambda x: x[:2])
test_df['上传日期_month'] = test_df['上传日期'].apply(lambda x: x[:2])

train_df['上传日期_month'] = train_df['上传日期_month'].apply(lambda x: ['Fe', 'Ma', 'Oc', 'Se'].index(x))
test_df['上传日期_month'] = test_df['上传日期_month'].apply(lambda x: ['Fe', 'Ma', 'Oc', 'Se'].index(x))

train_df.drop(['上传日期'], axis=1, inplace=True)
test_df.drop(['上传日期'], axis=1, inplace=True)


# In[ ]:


train_df['可带宠物'] = train_df['可带宠物'].map({'negotiable': 0.5, 'no': 0, 'yea': 1})
test_df['可带宠物'] = test_df['可带宠物'].map({'negotiable': 0.5, 'no': 0, 'yea': 1})


# In[ ]:


for col in train_df.select_dtypes(bool).columns:
    train_df[col] = train_df[col].astype(int)
    test_df[col] = test_df[col].astype(int)


# In[ ]:


train_df.dtypes


# In[ ]:


train_df['房屋租金'] = np.log1p(train_df['房屋租金'])


# In[ ]:


train_df['区域1_租金价格'] = train_df['区域1'].map(train_df.groupby(['区域1'])['房屋租金'].mean())
test_df['区域1_租金价格'] = test_df['区域1'].map(train_df.groupby(['区域1'])['房屋租金'].mean())

train_df['区域2_租金价格'] = train_df['区域2'].map(train_df.groupby(['区域2'])['房屋租金'].mean())
test_df['区域2_租金价格'] = test_df['区域2'].map(train_df.groupby(['区域2'])['房屋租金'].mean())

train_df['邮政编码_租金价格'] = train_df['邮政编码'].map(train_df.groupby(['邮政编码'])['房屋租金'].mean())
test_df['邮政编码_租金价格'] = test_df['邮政编码'].map(train_df.groupby(['邮政编码'])['房屋租金'].mean())


# In[ ]:


train_df['所处楼层_div'] = train_df['所处楼层'] / train_df['建筑楼层']
test_df['所处楼层_div'] = test_df['所处楼层'] / test_df['建筑楼层']

train_df['所处楼层_max'] = (train_df['所处楼层'] == train_df['建筑楼层']).astype(int)
test_df['所处楼层_max'] = (test_df['所处楼层'] == test_df['建筑楼层']).astype(int)

train_df['居住面积_mean'] = train_df['居住面积'] / train_df['房间数量']
test_df['居住面积_mean'] = test_df['居住面积'] / test_df['房间数量']


# In[ ]:


train_df['建成年龄'] = 2022 - train_df['建成年份']
test_df['建成年龄'] = 2022 - test_df['建成年份']

train_df['翻新年龄'] = 2022 - train_df['最后翻新年份']
test_df['翻新年龄'] = 2022 - test_df['最后翻新年份']


# # 搭建模型

# In[ ]:


for col in ['区域1', '区域2', '区域3', '街道', '房屋类型', '房屋状况', '可带宠物', '邮政编码']:
    train_df[col] = train_df[col].astype('category')
    test_df[col] = test_df[col].astype('category')


# In[ ]:


# 模型交叉验证
def run_model_cv(model, kf, X_tr, y, X_te, cate_col=None):
    train_pred = np.zeros( len(X_tr) )
    test_pred = np.zeros( len(X_te)  )

    cv_clf = []
    for tr_idx, val_idx in kf.split(X_tr, y):
        x_tr = X_tr.iloc[tr_idx]; y_tr = y.iloc[tr_idx]

        x_val = X_tr.iloc[val_idx]; y_val = y.iloc[val_idx]

        call_back = [
            lgb.early_stopping(50),
        ]
        eval_set = [(x_val, y_val)]
        model.fit(x_tr, y_tr, eval_set=eval_set, callbacks=call_back, verbose=-1,
                 categorical_feature= 'auto', eval_metric= 'mae', )

        cv_clf.append(model)

        train_pred[val_idx] = model.predict(x_val)
        test_pred += model.predict(X_te)

    test_pred /= kf.n_splits
    
    print(np.abs(np.exp(train_pred) - np.exp(y)).mean())
    return train_pred, test_pred, cv_clf


# In[ ]:


from sklearn.model_selection import KFold
import lightgbm as lgb

test_pred_tta = np.zeros( len(test_df)  )
for _ in range(1):
    clf = lgb.LGBMRegressor(
        max_depth=7, 
        n_estimators=4000, 
        n_jobs=-1, 
        verbose=-1,
        verbosity=-1,
        learning_rate=0.03,
        random_state=np.random.randint(100)
    )

    train_pred, test_pred, cv_clf = run_model_cv(
        clf, KFold(n_splits=5, random_state=np.random.randint(100), shuffle=True),
        train_df.drop(['ID', '房屋租金'], axis=1),
        train_df['房屋租金'],
        test_df.drop(['ID'], axis=1),
    )
    
    test_pred_tta += test_pred

# 133.28688613802427，95.7
# 132.1 75.0


# In[ ]:


pd.DataFrame({
    'ID': test_df['ID'],
    '房屋租金': np.exp(test_pred_tta / 1).astype(int)
}).to_csv('submit.csv', index=None)


# In[ ]:




