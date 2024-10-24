#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd


# In[ ]:


pd.set_option('display.max_row', None)
pd.set_option('display.max_columns', None)


# In[ ]:


train = pd.read_csv('train_data.csv', index_col=False)
test = pd.read_csv('validation.csv', index_col=False)
kpi_data = pd.read_csv('Compensation KPI.csv', index_col=False)
train.shape, test.shape, kpi_data.shape


# In[ ]:


#数据聚合
kpi_data.drop_duplicates(subset=['时间', '日期','补偿小区CI'],keep='first', inplace=True)
kpi_data['time'] = kpi_data['日期'].map(str) + "/" + kpi_data['时间'].map(str) 
kpi_data['time'] = pd.to_datetime(kpi_data['time'])
train['time'] = pd.to_datetime(train['time'])
test['time'] = pd.to_datetime(test['time'])
#数据合并
train = pd.merge(train, kpi_data, on=['time', '补偿小区CI'], how='left')
test = pd.merge(test, kpi_data, on=['time', '补偿小区CI'], how='left')
train.drop(['日期', '时间'], axis=1, inplace=True)
test.drop(['日期', '时间'], axis=1, inplace=True)

#写入本地
train.to_csv('train.csv',index=False)
test.to_csv('test.csv',index=False)


# In[ ]:


train.shape, test.shape


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:





# In[ ]:




