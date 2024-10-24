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
#test_data = pd.read_csv('test.csv')
data_all = train_data.copy()


# In[ ]:


data_all.shape


# ## 二、特征工程

# ### 1、 缺失值处理

# In[ ]:


##丢弃全为空值列
data_all = data_all.dropna(axis=1, how="all") 
 
'''
##丢弃空值率大于60%的列
pct_null = train_data_DT.isnull().sum() / len(train_data_DT)
missing_features = pct_null[pct_null > 0.60].index
train_data_DT.drop(missing_features, axis=1, inplace=True)
'''


# In[ ]:


data_all.shape


# In[ ]:


df = data_all[data_all['oneanswer'].notnull()]


# In[ ]:


#df = df[df['OLT TX Power10'].notnull()]
df = df[df['OLT TX Power10'].notnull()]
#df = df[df['AcctIPv6OutputPackets27'].notnull()]


# In[ ]:


df_bak = df.copy()


# In[ ]:


df.shape


# In[ ]:





# In[ ]:


df = df.drop(['oneanswererror','id','SHEET_ID','CONTACT_ID','物理小区名称','区县名称','网格名称','phone','Unnamed: 0','设备号','用户编码','上网账号','标准地址','详细地址','BIG_TYPE_NAME','SMALL_TYPE_NAME','SERV_TYPE_NAME','SIX_SHEET_TYPE_NAME','CUST_PROV_NAME','CUST_AREA_NAME','SHEET_NO'  
             ,'ACCEPT_CHANNEL_NAME','DUTY_REASON_NAME','DUTY_MAJOR_NAME','BUSI_DEPART_NAME','IS_CALL_COMPLETE','IS_CUSSER_COMPLETE','IS_DISTR_COMPLETE',  
             'KEYWORD_NAME','DATE_PART','MONTH_ID','DAY_ID','COMPL_PROV','COMPL_AREA','NAME_COMPL_PROV','NAME_COMPL_AREA','sendquestime','pushchannel',  
             'pushchannelname','onetime','twoanswer','twoanswererror','twoanswerother','twotime','threeanswer','threeanswererror','threeanswerother',  
             'threetime','fouranswer','fouranswererror','fouranswerother','fourtime','Unnamed: 0.1.1','维护班组','归属小区','用户IP',  
             'serialnumber','x_cu_serialnumber','loid','result','series','userid','series_num','handleprovincename','handlecitiesname','iptv','用户MAC'], axis=1)


# In[ ]:


df.info(verbose=True, null_counts=True)


# ### 2、异常值处理

# ### 3、特征构建

# #### 3.1 类别特征处理

# In[ ]:


'''
fact_list = data_all['fact_name'].value_counts()[0:35]
data_all['fact_name']=data_all['fact_name'].apply(lambda x:'其他' if x not in fact_list else x)
fact_list = data_all['user_dinner'].value_counts()[0:145]
data_all['user_dinner']=data_all['user_dinner'].apply(lambda x:'其他' if x not in fact_list else x)
'''


# In[ ]:


label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['CUST_PROV_ID'].values)))
df['CUST_PROV_ID']=label.transform(list(df['CUST_PROV_ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['CUST_AREA_ID'].values)))
df['CUST_AREA_ID']=label.transform(list(df['CUST_AREA_ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['CUST_STAR_CODE'].values)))
df['CUST_STAR_CODE']=label.transform(list(df['CUST_STAR_CODE'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['SIX_SHEET_TYPE_CODE'].values)))
df['SIX_SHEET_TYPE_CODE']=label.transform(list(df['SIX_SHEET_TYPE_CODE'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['SERV_TYPE_ID'].values)))
df['SERV_TYPE_ID']=label.transform(list(df['SERV_TYPE_ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['BIG_TYPE_CODE'].values)))
df['BIG_TYPE_CODE']=label.transform(list(df['BIG_TYPE_CODE'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['SMALL_TYPE_CODE'].values)))
df['SMALL_TYPE_CODE']=label.transform(list(df['SMALL_TYPE_CODE'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['GIS_LATLON'].values)))
df['GIS_LATLON']=label.transform(list(df['GIS_LATLON'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['IS_DISPATCH_CLOUD'].values)))
df['IS_DISPATCH_CLOUD']=label.transform(list(df['IS_DISPATCH_CLOUD'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['ACCEPT_CHANNEL_CODE'].values)))
df['ACCEPT_CHANNEL_CODE']=label.transform(list(df['ACCEPT_CHANNEL_CODE'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['IS_ONLINE_COMPLETE'].values)))
df['IS_ONLINE_COMPLETE']=label.transform(list(df['IS_ONLINE_COMPLETE'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['IS_BROADBAND'].values)))
df['IS_BROADBAND']=label.transform(list(df['IS_BROADBAND'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['NET_TYPE'].values)))
df['NET_TYPE']=label.transform(list(df['NET_TYPE'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['IS_5G'].values)))
df['IS_5G']=label.transform(list(df['IS_5G'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['menu_type'].values)))
df['menu_type']=label.transform(list(df['menu_type'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['net_type'].values)))
df['net_type']=label.transform(list(df['net_type'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['net_question_type'].values)))
df['net_question_type']=label.transform(list(df['net_question_type'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['net_question'].values)))
df['net_question']=label.transform(list(df['net_question'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['TS_Type'].values)))
df['TS_Type']=label.transform(list(df['TS_Type'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['产品规格标识'].values)))
df['产品规格标识']=label.transform(list(df['产品规格标识'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['接入方式'].values)))
df['接入方式']=label.transform(list(df['接入方式'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['ONU设备ID'].values)))
df['ONU设备ID']=label.transform(list(df['ONU设备ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['一级分光器ID'].values)))
df['一级分光器ID']=label.transform(list(df['一级分光器ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['二级分光器ID'].values)))
df['二级分光器ID']=label.transform(list(df['二级分光器ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['末级分光器ID'].values)))
df['末级分光器ID']=label.transform(list(df['末级分光器ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['PON口ID'].values)))
df['PON口ID']=label.transform(list(df['PON口ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['OLT设备ID'].values)))
df['OLT设备ID']=label.transform(list(df['OLT设备ID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['productname'].values)))
df['productname']=label.transform(list(df['productname'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['brotype'].values)))
df['brotype']=label.transform(list(df['brotype'].values))

#label = preprocessing.LabelEncoder()
#label.fit(np.unique(list(df['oneanswererror'].values)))
#df['oneanswererror']=label.transform(list(df['oneanswererror'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['TS_Type'].values)))
df['TS_Type']=label.transform(list(df['TS_Type'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['MANAGE_IPADDRESS'].values)))
df['MANAGE_IPADDRESS']=label.transform(list(df['MANAGE_IPADDRESS'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['NMS_ORIG_RES_NAME'].values)))
df['NMS_ORIG_RES_NAME']=label.transform(list(df['NMS_ORIG_RES_NAME'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['ORI_NMS_ORIG_RES_NAME'].values)))
df['ORI_NMS_ORIG_RES_NAME']=label.transform(list(df['ORI_NMS_ORIG_RES_NAME'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['EQP_SEQUENCE'].values)))
df['EQP_SEQUENCE']=label.transform(list(df['EQP_SEQUENCE'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['EQP_LOID'].values)))
df['EQP_LOID']=label.transform(list(df['EQP_LOID'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['地市'].values)))
df['地市']=label.transform(list(df['地市'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['区县'].values)))
df['区县']=label.transform(list(df['区县'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['小区编码'].values)))
df['小区编码']=label.transform(list(df['小区编码'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['OLTIP'].values)))
df['OLTIP']=label.transform(list(df['OLTIP'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['OLT设备名称'].values)))
df['OLT设备名称']=label.transform(list(df['OLT设备名称'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['OLT厂家'].values)))
df['OLT厂家']=label.transform(list(df['OLT厂家'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['BRASIP'].values)))
df['BRASIP']=label.transform(list(df['BRASIP'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['ONU设备型号'].values)))
df['ONU设备型号']=label.transform(list(df['ONU设备型号'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['device_id'].values)))
df['device_id']=label.transform(list(df['device_id'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['modelname'].values)))
df['modelname']=label.transform(list(df['modelname'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['numberofsubuser'].values)))
df['numberofsubuser']=label.transform(list(df['numberofsubuser'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['description'].values)))
df['description']=label.transform(list(df['description'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['productclass'].values)))
df['productclass']=label.transform(list(df['productclass'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['manufacturer'].values)))
df['manufacturer']=label.transform(list(df['manufacturer'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['hardwareversion'].values)))
df['hardwareversion']=label.transform(list(df['hardwareversion'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['softwareversion'].values)))
df['softwareversion']=label.transform(list(df['softwareversion'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['wantype'].values)))
df['wantype']=label.transform(list(df['wantype'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['x_cu_band'].values)))
df['x_cu_band']=label.transform(list(df['x_cu_band'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<1>_[status]'].values)))
df['lan_[lanethernetinterfaceconfig]_<1>_[status]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<1>_[status]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<2>_[status]'].values)))
df['lan_[lanethernetinterfaceconfig]_<2>_[status]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<2>_[status]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<3>_[status]'].values)))
df['lan_[lanethernetinterfaceconfig]_<3>_[status]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<3>_[status]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<4>_[status]'].values)))
df['lan_[lanethernetinterfaceconfig]_<4>_[status]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<4>_[status]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<1>_[maxbitrate_lan]'].values)))
df['lan_[lanethernetinterfaceconfig]_<1>_[maxbitrate_lan]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<1>_[maxbitrate_lan]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<2>_[maxbitrate_lan]'].values)))
df['lan_[lanethernetinterfaceconfig]_<2>_[maxbitrate_lan]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<2>_[maxbitrate_lan]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<3>_[maxbitrate_lan]'].values)))
df['lan_[lanethernetinterfaceconfig]_<3>_[maxbitrate_lan]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<3>_[maxbitrate_lan]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<4>_[maxbitrate_lan]'].values)))
df['lan_[lanethernetinterfaceconfig]_<4>_[maxbitrate_lan]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<4>_[maxbitrate_lan]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<1>_[x_cu_adaptrate]'].values)))
df['lan_[lanethernetinterfaceconfig]_<1>_[x_cu_adaptrate]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<1>_[x_cu_adaptrate]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<2>_[x_cu_adaptrate]'].values)))
df['lan_[lanethernetinterfaceconfig]_<2>_[x_cu_adaptrate]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<2>_[x_cu_adaptrate]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<3>_[x_cu_adaptrate]'].values)))
df['lan_[lanethernetinterfaceconfig]_<3>_[x_cu_adaptrate]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<3>_[x_cu_adaptrate]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<4>_[x_cu_adaptrate]'].values)))
df['lan_[lanethernetinterfaceconfig]_<4>_[x_cu_adaptrate]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<4>_[x_cu_adaptrate]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<1>_[duplexmode]'].values)))
df['lan_[lanethernetinterfaceconfig]_<1>_[duplexmode]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<1>_[duplexmode]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<2>_[duplexmode]'].values)))
df['lan_[lanethernetinterfaceconfig]_<2>_[duplexmode]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<2>_[duplexmode]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<3>_[duplexmode]'].values)))
df['lan_[lanethernetinterfaceconfig]_<3>_[duplexmode]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<3>_[duplexmode]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<4>_[duplexmode]'].values)))
df['lan_[lanethernetinterfaceconfig]_<4>_[duplexmode]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<4>_[duplexmode]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<5>_[status]'].values)))
df['lan_[lanethernetinterfaceconfig]_<5>_[status]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<5>_[status]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['lan_[lanethernetinterfaceconfig]_<5>_[duplexmode]'].values)))
df['lan_[lanethernetinterfaceconfig]_<5>_[duplexmode]']=label.transform(list(df['lan_[lanethernetinterfaceconfig]_<5>_[duplexmode]'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['wlan_maxbitrate'].values)))
df['wlan_maxbitrate']=label.transform(list(df['wlan_maxbitrate'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['wlan_wpaauthenticationmode'].values)))
df['wlan_wpaauthenticationmode']=label.transform(list(df['wlan_wpaauthenticationmode'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['wan_wanconnectiondevice_i'].values)))
df['wan_wanconnectiondevice_i']=label.transform(list(df['wan_wanconnectiondevice_i'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['wan_wanpppconnection_i'].values)))
df['wan_wanpppconnection_i']=label.transform(list(df['wan_wanpppconnection_i'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['wan_wanpppconnectionnumberofentries'].values)))
df['wan_wanpppconnectionnumberofentries']=label.transform(list(df['wan_wanpppconnectionnumberofentries'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(df['x_cu_os'].values)))
df['x_cu_os']=label.transform(list(df['x_cu_os'].values))



# In[ ]:


#每个字段前加上序号，解决列名同名问题
df = df.rename(columns={col: f"{i}_{col}" for i, col in enumerate(df.columns)})
import re
#去除字段名中汉字和常规符号以外的符号
df = df.rename(columns = lambda x:re.sub('[^A-Za-z0-9\u4e00-\u9fa5_]+', '', x))


# In[ ]:


df['设备号'] = df_bak['设备号']


# In[ ]:


df['设备号'].duplicated().sum() 


# In[ ]:


df.info(verbose=True, null_counts=True)


# In[ ]:


df_target = df['35_oneanswer']
#df = df.drop(['35_oneanswer'], axis=1)


# In[ ]:


df = df[df['585_AcctIPv6InputOctetssum2'].notnull()]


# In[ ]:


df2 = df.copy()
#df2= pd.DataFrame(df)


# In[ ]:


df_OLTTXPower= df2[df2.columns[df2.columns.str.contains("OLTTXPower")]]
df_OLTRXPower= df2[df2.columns[df2.columns.str.contains("OLTRXPower")]]
df_ONU_TX_POWER= df2[df2.columns[df2.columns.str.contains("ONU_TX_POWER")]]
df_ONU_ONU_RX_POWER= df2[df2.columns[df2.columns.str.contains("ONU_RX_POWER")]]


# In[ ]:


df_OLTTXPower['设备号'] = df2['设备号']
df_OLTRXPower['设备号'] = df2['设备号']
df_ONU_TX_POWER['设备号'] = df2['设备号']
df_ONU_ONU_RX_POWER['设备号'] = df2['设备号']


# In[ ]:


tmp_df_SendKBytessum= df2[df2.columns[df2.columns.str.contains("SendKBytessum")]]
tmp_df_ReceiveKBytessum= df2[df2.columns[df2.columns.str.contains("ReceiveKBytessum")]]
tmp_df_AcctIPv6InputOctetssum= df2[df2.columns[df2.columns.str.contains("AcctIPv6InputOctetssum")]]
tmp_df_AcctIPv6OutputOctetssum= df2[df2.columns[df2.columns.str.contains("AcctIPv6OutputOctetssum")]]
tmp_df_AcctIPv6InputPacketssum= df2[df2.columns[df2.columns.str.contains("AcctIPv6InputPacketssum")]]
tmp_df_AcctIPv6OutputPackets= df2[df2.columns[df2.columns.str.contains("AcctIPv6OutputPackets")]]


# In[ ]:


df_SendKBytessum = pd.DataFrame()
df_ReceiveKBytessum = pd.DataFrame()
df_AcctIPv6InputOctetssum = pd.DataFrame()
df_AcctIPv6OutputOctetssum = pd.DataFrame()
df_AcctIPv6InputPacketssum = pd.DataFrame()
df_AcctIPv6OutputPackets = pd.DataFrame()


# In[ ]:


df_SendKBytessum['1'] = df2['421_SendKBytessum1']
df_SendKBytessum['2'] = df2['583_SendKBytessum2']
df_SendKBytessum['3'] = df2['577_SendKBytessum3']
df_SendKBytessum['4'] = df2['571_SendKBytessum4']
df_SendKBytessum['5'] = df2['565_SendKBytessum5']
df_SendKBytessum['6'] = df2['559_SendKBytessum6']
df_SendKBytessum['7'] =  None
df_SendKBytessum['8'] = df2['553_SendKBytessum8']
df_SendKBytessum['9'] = df2['547_SendKBytessum9']
df_SendKBytessum['10'] = df2['541_SendKBytessum10']
df_SendKBytessum['11'] = df2['535_SendKBytessum11']
df_SendKBytessum['12'] = df2['529_SendKBytessum12']
df_SendKBytessum['13'] = None
df_SendKBytessum['14'] = df2['523_SendKBytessum14']
df_SendKBytessum['15'] = df2['517_SendKBytessum15']
df_SendKBytessum['16'] = df2['511_SendKBytessum16']
df_SendKBytessum['17'] = df2['505_SendKBytessum17']
df_SendKBytessum['18'] = df2['499_SendKBytessum18']
df_SendKBytessum['19'] = df2['493_SendKBytessum19']
df_SendKBytessum['20'] = df2['487_SendKBytessum20']
df_SendKBytessum['21'] = df2['481_SendKBytessum21']
df_SendKBytessum['22'] = df2['475_SendKBytessum22']
df_SendKBytessum['23'] = df2['469_SendKBytessum23']
df_SendKBytessum['24'] = df2['463_SendKBytessum24']
df_SendKBytessum['25'] = df2['457_SendKBytessum25']
df_SendKBytessum['26'] = df2['451_SendKBytessum26']
df_SendKBytessum['27'] = df2['445_SendKBytessum27']
df_SendKBytessum['28'] = df2['439_SendKBytessum28']
df_SendKBytessum['29'] = df2['433_SendKBytessum29']
df_SendKBytessum['30'] = df2['427_SendKBytessum30']


# In[ ]:


df_ReceiveKBytessum['422_ReceiveKBytessum1'] = df2['422_ReceiveKBytessum1']
df_ReceiveKBytessum['584_ReceiveKBytessum2'] = df2['584_ReceiveKBytessum2']
df_ReceiveKBytessum['578_ReceiveKBytessum3'] = df2['578_ReceiveKBytessum3']
df_ReceiveKBytessum['572_ReceiveKBytessum4'] = df2['572_ReceiveKBytessum4']
df_ReceiveKBytessum['566_ReceiveKBytessum5'] = df2['566_ReceiveKBytessum5']
df_ReceiveKBytessum['560_ReceiveKBytessum6'] = df2['560_ReceiveKBytessum6']
df_ReceiveKBytessum['ReceiveKBytessum7'] = None
df_ReceiveKBytessum['554_ReceiveKBytessum8'] = df2['554_ReceiveKBytessum8']
df_ReceiveKBytessum['548_ReceiveKBytessum9'] = df2['548_ReceiveKBytessum9']
df_ReceiveKBytessum['542_ReceiveKBytessum10'] = df2['542_ReceiveKBytessum10']
df_ReceiveKBytessum['536_ReceiveKBytessum11'] = df2['536_ReceiveKBytessum11']
df_ReceiveKBytessum['530_ReceiveKBytessum12'] = df2['530_ReceiveKBytessum12']
df_ReceiveKBytessum['ReceiveKBytessum13'] = None
df_ReceiveKBytessum['524_ReceiveKBytessum14'] = df2['524_ReceiveKBytessum14']
df_ReceiveKBytessum['518_ReceiveKBytessum15'] = df2['518_ReceiveKBytessum15']
df_ReceiveKBytessum['512_ReceiveKBytessum16'] = df2['512_ReceiveKBytessum16']
df_ReceiveKBytessum['506_ReceiveKBytessum17'] = df2['506_ReceiveKBytessum17']
df_ReceiveKBytessum['500_ReceiveKBytessum18'] = df2['500_ReceiveKBytessum18']
df_ReceiveKBytessum['494_ReceiveKBytessum19'] = df2['494_ReceiveKBytessum19']
df_ReceiveKBytessum['488_ReceiveKBytessum20'] = df2['488_ReceiveKBytessum20']
df_ReceiveKBytessum['482_ReceiveKBytessum21'] = df2['482_ReceiveKBytessum21']
df_ReceiveKBytessum['476_ReceiveKBytessum22'] = df2['476_ReceiveKBytessum22']
df_ReceiveKBytessum['470_ReceiveKBytessum23'] = df2['470_ReceiveKBytessum23']
df_ReceiveKBytessum['464_ReceiveKBytessum24'] = df2['464_ReceiveKBytessum24']
df_ReceiveKBytessum['458_ReceiveKBytessum25'] = df2['458_ReceiveKBytessum25']
df_ReceiveKBytessum['452_ReceiveKBytessum26'] = df2['452_ReceiveKBytessum26']
df_ReceiveKBytessum['446_ReceiveKBytessum27'] = df2['446_ReceiveKBytessum27']
df_ReceiveKBytessum['440_ReceiveKBytessum28'] = df2['440_ReceiveKBytessum28']
df_ReceiveKBytessum['434_ReceiveKBytessum29'] = df2['434_ReceiveKBytessum29']
df_ReceiveKBytessum['428_ReceiveKBytessum30'] = df2['428_ReceiveKBytessum30']


# In[ ]:


df_AcctIPv6InputOctetssum['423_AcctIPv6InputOctetssum1'] = df2['423_AcctIPv6InputOctetssum1']
df_AcctIPv6InputOctetssum['585_AcctIPv6InputOctetssum2'] = df2['585_AcctIPv6InputOctetssum2']
df_AcctIPv6InputOctetssum['579_AcctIPv6InputOctetssum3'] = df2['579_AcctIPv6InputOctetssum3']
df_AcctIPv6InputOctetssum['573_AcctIPv6InputOctetssum4'] = df2['573_AcctIPv6InputOctetssum4']
df_AcctIPv6InputOctetssum['567_AcctIPv6InputOctetssum5'] = df2['567_AcctIPv6InputOctetssum5']
df_AcctIPv6InputOctetssum['561_AcctIPv6InputOctetssum6'] = df2['561_AcctIPv6InputOctetssum6']
df_AcctIPv6InputOctetssum['AcctIPv6InputOctetssum7'] = None
df_AcctIPv6InputOctetssum['555_AcctIPv6InputOctetssum8'] = df2['555_AcctIPv6InputOctetssum8']
df_AcctIPv6InputOctetssum['549_AcctIPv6InputOctetssum9'] = df2['549_AcctIPv6InputOctetssum9']
df_AcctIPv6InputOctetssum['543_AcctIPv6InputOctetssum10'] = df2['543_AcctIPv6InputOctetssum10']
df_AcctIPv6InputOctetssum['537_AcctIPv6InputOctetssum11'] = df2['537_AcctIPv6InputOctetssum11']
df_AcctIPv6InputOctetssum['531_AcctIPv6InputOctetssum12'] = df2['531_AcctIPv6InputOctetssum12']
df_AcctIPv6InputOctetssum['AcctIPv6InputOctetssum13'] = None
df_AcctIPv6InputOctetssum['525_AcctIPv6InputOctetssum14'] = df2['525_AcctIPv6InputOctetssum14']
df_AcctIPv6InputOctetssum['519_AcctIPv6InputOctetssum15'] = df2['519_AcctIPv6InputOctetssum15']
df_AcctIPv6InputOctetssum['513_AcctIPv6InputOctetssum16'] = df2['513_AcctIPv6InputOctetssum16']
df_AcctIPv6InputOctetssum['507_AcctIPv6InputOctetssum17'] = df2['507_AcctIPv6InputOctetssum17']
df_AcctIPv6InputOctetssum['501_AcctIPv6InputOctetssum18'] = df2['501_AcctIPv6InputOctetssum18']
df_AcctIPv6InputOctetssum['495_AcctIPv6InputOctetssum19'] = df2['495_AcctIPv6InputOctetssum19']
df_AcctIPv6InputOctetssum['489_AcctIPv6InputOctetssum20'] = df2['489_AcctIPv6InputOctetssum20']
df_AcctIPv6InputOctetssum['483_AcctIPv6InputOctetssum21'] = df2['483_AcctIPv6InputOctetssum21']
df_AcctIPv6InputOctetssum['477_AcctIPv6InputOctetssum22'] = df2['477_AcctIPv6InputOctetssum22']
df_AcctIPv6InputOctetssum['471_AcctIPv6InputOctetssum23'] = df2['471_AcctIPv6InputOctetssum23']
df_AcctIPv6InputOctetssum['465_AcctIPv6InputOctetssum24'] = df2['465_AcctIPv6InputOctetssum24']
df_AcctIPv6InputOctetssum['459_AcctIPv6InputOctetssum25'] = df2['459_AcctIPv6InputOctetssum25']
df_AcctIPv6InputOctetssum['453_AcctIPv6InputOctetssum26'] = df2['453_AcctIPv6InputOctetssum26']
df_AcctIPv6InputOctetssum['447_AcctIPv6InputOctetssum27'] = df2['447_AcctIPv6InputOctetssum27']
df_AcctIPv6InputOctetssum['441_AcctIPv6InputOctetssum28'] = df2['441_AcctIPv6InputOctetssum28']
df_AcctIPv6InputOctetssum['435_AcctIPv6InputOctetssum29'] = df2['435_AcctIPv6InputOctetssum29']
df_AcctIPv6InputOctetssum['429_AcctIPv6InputOctetssum30'] = df2['429_AcctIPv6InputOctetssum30']


# In[ ]:


df_AcctIPv6OutputOctetssum['424_AcctIPv6OutputOctetssum1'] = df2['424_AcctIPv6OutputOctetssum1']
df_AcctIPv6OutputOctetssum['586_AcctIPv6OutputOctetssum2'] = df2['586_AcctIPv6OutputOctetssum2']
df_AcctIPv6OutputOctetssum['580_AcctIPv6OutputOctetssum3'] = df2['580_AcctIPv6OutputOctetssum3']
df_AcctIPv6OutputOctetssum['574_AcctIPv6OutputOctetssum4'] = df2['574_AcctIPv6OutputOctetssum4']
df_AcctIPv6OutputOctetssum['568_AcctIPv6OutputOctetssum5'] = df2['568_AcctIPv6OutputOctetssum5']
df_AcctIPv6OutputOctetssum['562_AcctIPv6OutputOctetssum6'] = df2['562_AcctIPv6OutputOctetssum6']
df_AcctIPv6OutputOctetssum['AcctIPv6OutputOctetssum7'] = None
df_AcctIPv6OutputOctetssum['556_AcctIPv6OutputOctetssum8'] = df2['556_AcctIPv6OutputOctetssum8']
df_AcctIPv6OutputOctetssum['550_AcctIPv6OutputOctetssum9'] = df2['550_AcctIPv6OutputOctetssum9']
df_AcctIPv6OutputOctetssum['544_AcctIPv6OutputOctetssum10'] = df2['544_AcctIPv6OutputOctetssum10']

df_AcctIPv6OutputOctetssum['538_AcctIPv6OutputOctetssum11'] = df2['538_AcctIPv6OutputOctetssum11']
df_AcctIPv6OutputOctetssum['532_AcctIPv6OutputOctetssum12'] = df2['532_AcctIPv6OutputOctetssum12']
df_AcctIPv6OutputOctetssum['AcctIPv6OutputOctetssum13'] = None
df_AcctIPv6OutputOctetssum['526_AcctIPv6OutputOctetssum14'] = df2['526_AcctIPv6OutputOctetssum14']
df_AcctIPv6OutputOctetssum['520_AcctIPv6OutputOctetssum15'] = df2['520_AcctIPv6OutputOctetssum15']
df_AcctIPv6OutputOctetssum['514_AcctIPv6OutputOctetssum16'] = df2['514_AcctIPv6OutputOctetssum16']
df_AcctIPv6OutputOctetssum['508_AcctIPv6OutputOctetssum17'] = df2['508_AcctIPv6OutputOctetssum17']
df_AcctIPv6OutputOctetssum['502_AcctIPv6OutputOctetssum18'] = df2['502_AcctIPv6OutputOctetssum18']
df_AcctIPv6OutputOctetssum['496_AcctIPv6OutputOctetssum19'] = df2['496_AcctIPv6OutputOctetssum19']
df_AcctIPv6OutputOctetssum['490_AcctIPv6OutputOctetssum20'] = df2['490_AcctIPv6OutputOctetssum20']

df_AcctIPv6OutputOctetssum['484_AcctIPv6OutputOctetssum21'] = df2['484_AcctIPv6OutputOctetssum21']
df_AcctIPv6OutputOctetssum['478_AcctIPv6OutputOctetssum22'] = df2['478_AcctIPv6OutputOctetssum22']
df_AcctIPv6OutputOctetssum['472_AcctIPv6OutputOctetssum23'] = df2['472_AcctIPv6OutputOctetssum23']
df_AcctIPv6OutputOctetssum['466_AcctIPv6OutputOctetssum24'] = df2['466_AcctIPv6OutputOctetssum24']
df_AcctIPv6OutputOctetssum['460_AcctIPv6OutputOctetssum25'] = df2['460_AcctIPv6OutputOctetssum25']
df_AcctIPv6OutputOctetssum['454_AcctIPv6OutputOctetssum26'] = df2['454_AcctIPv6OutputOctetssum26']
df_AcctIPv6OutputOctetssum['448_AcctIPv6OutputOctetssum27'] = df2['448_AcctIPv6OutputOctetssum27']
df_AcctIPv6OutputOctetssum['442_AcctIPv6OutputOctetssum28'] = df2['442_AcctIPv6OutputOctetssum28']
df_AcctIPv6OutputOctetssum['436_AcctIPv6OutputOctetssum29'] = df2['436_AcctIPv6OutputOctetssum29']
df_AcctIPv6OutputOctetssum['430_AcctIPv6OutputOctetssum30'] = df2['430_AcctIPv6OutputOctetssum30']


# In[ ]:


df_AcctIPv6InputPacketssum['425_AcctIPv6InputPacketssum1'] = df2['425_AcctIPv6InputPacketssum1']
df_AcctIPv6InputPacketssum['587_AcctIPv6InputPacketssum2'] = df2['587_AcctIPv6InputPacketssum2']
df_AcctIPv6InputPacketssum['581_AcctIPv6InputPacketssum3'] = df2['581_AcctIPv6InputPacketssum3']
df_AcctIPv6InputPacketssum['575_AcctIPv6InputPacketssum4'] = df2['575_AcctIPv6InputPacketssum4']
df_AcctIPv6InputPacketssum['569_AcctIPv6InputPacketssum5'] = df2['569_AcctIPv6InputPacketssum5']
df_AcctIPv6InputPacketssum['563_AcctIPv6InputPacketssum6'] = df2['563_AcctIPv6InputPacketssum6']
df_AcctIPv6InputPacketssum['AcctIPv6InputPacketssum7'] = None
df_AcctIPv6InputPacketssum['557_AcctIPv6InputPacketssum8'] = df2['557_AcctIPv6InputPacketssum8']
df_AcctIPv6InputPacketssum['551_AcctIPv6InputPacketssum9'] = df2['551_AcctIPv6InputPacketssum9']
df_AcctIPv6InputPacketssum['545_AcctIPv6InputPacketssum10'] = df2['545_AcctIPv6InputPacketssum10']

df_AcctIPv6InputPacketssum['539_AcctIPv6InputPacketssum11'] = df2['539_AcctIPv6InputPacketssum11']
df_AcctIPv6InputPacketssum['533_AcctIPv6InputPacketssum12'] = df2['533_AcctIPv6InputPacketssum12']
df_AcctIPv6InputPacketssum['AcctIPv6InputPacketssum13'] = None
df_AcctIPv6InputPacketssum['527_AcctIPv6InputPacketssum14'] = df2['527_AcctIPv6InputPacketssum14']
df_AcctIPv6InputPacketssum['521_AcctIPv6InputPacketssum15'] = df2['521_AcctIPv6InputPacketssum15']
df_AcctIPv6InputPacketssum['515_AcctIPv6InputPacketssum16'] = df2['515_AcctIPv6InputPacketssum16']
df_AcctIPv6InputPacketssum['509_AcctIPv6InputPacketssum17'] = df2['509_AcctIPv6InputPacketssum17']
df_AcctIPv6InputPacketssum['503_AcctIPv6InputPacketssum18'] = df2['503_AcctIPv6InputPacketssum18']
df_AcctIPv6InputPacketssum['497_AcctIPv6InputPacketssum19'] = df2['497_AcctIPv6InputPacketssum19']
df_AcctIPv6InputPacketssum['491_AcctIPv6InputPacketssum20'] = df2['491_AcctIPv6InputPacketssum20']

df_AcctIPv6InputPacketssum['485_AcctIPv6InputPacketssum21'] = df2['485_AcctIPv6InputPacketssum21']
df_AcctIPv6InputPacketssum['479_AcctIPv6InputPacketssum22'] = df2['479_AcctIPv6InputPacketssum22']
df_AcctIPv6InputPacketssum['473_AcctIPv6InputPacketssum23'] = df2['473_AcctIPv6InputPacketssum23']
df_AcctIPv6InputPacketssum['467_AcctIPv6InputPacketssum24'] = df2['467_AcctIPv6InputPacketssum24']
df_AcctIPv6InputPacketssum['461_AcctIPv6InputPacketssum25'] = df2['461_AcctIPv6InputPacketssum25']
df_AcctIPv6InputPacketssum['455_AcctIPv6InputPacketssum26'] = df2['455_AcctIPv6InputPacketssum26']
df_AcctIPv6InputPacketssum['449_AcctIPv6InputPacketssum27'] = df2['449_AcctIPv6InputPacketssum27']
df_AcctIPv6InputPacketssum['443_AcctIPv6InputPacketssum28'] = df2['443_AcctIPv6InputPacketssum28']
df_AcctIPv6InputPacketssum['437_AcctIPv6InputPacketssum29'] = df2['437_AcctIPv6InputPacketssum29']
df_AcctIPv6InputPacketssum['431_AcctIPv6InputPacketssum30'] = df2['431_AcctIPv6InputPacketssum30']


# In[ ]:


df_AcctIPv6OutputPackets['426_AcctIPv6OutputPackets1'] = df2['426_AcctIPv6OutputPackets1']
df_AcctIPv6OutputPackets['588_AcctIPv6OutputPackets2'] = df2['588_AcctIPv6OutputPackets2']
df_AcctIPv6OutputPackets['582_AcctIPv6OutputPackets3'] = df2['582_AcctIPv6OutputPackets3']
df_AcctIPv6OutputPackets['576_AcctIPv6OutputPackets4'] = df2['576_AcctIPv6OutputPackets4']
df_AcctIPv6OutputPackets['570_AcctIPv6OutputPackets5'] = df2['570_AcctIPv6OutputPackets5']
df_AcctIPv6OutputPackets['564_AcctIPv6OutputPackets6'] = df2['564_AcctIPv6OutputPackets6']
df_AcctIPv6OutputPackets['AcctIPv6OutputPackets7'] = None
df_AcctIPv6OutputPackets['558_AcctIPv6OutputPackets8'] = df2['558_AcctIPv6OutputPackets8']
df_AcctIPv6OutputPackets['552_AcctIPv6OutputPackets9'] = df2['552_AcctIPv6OutputPackets9']
df_AcctIPv6OutputPackets['546_AcctIPv6OutputPackets10'] = df2['546_AcctIPv6OutputPackets10']

df_AcctIPv6OutputPackets['540_AcctIPv6OutputPackets11'] = df2['540_AcctIPv6OutputPackets11']
df_AcctIPv6OutputPackets['534_AcctIPv6OutputPackets12'] = df2['534_AcctIPv6OutputPackets12']
df_AcctIPv6OutputPackets['AcctIPv6OutputPackets13'] = None
df_AcctIPv6OutputPackets['528_AcctIPv6OutputPackets14'] = df2['528_AcctIPv6OutputPackets14']
df_AcctIPv6OutputPackets['522_AcctIPv6OutputPackets15'] = df2['522_AcctIPv6OutputPackets15']
df_AcctIPv6OutputPackets['516_AcctIPv6OutputPackets16'] = df2['516_AcctIPv6OutputPackets16']
df_AcctIPv6OutputPackets['510_AcctIPv6OutputPackets17'] = df2['510_AcctIPv6OutputPackets17']
df_AcctIPv6OutputPackets['504_AcctIPv6OutputPackets18'] = df2['504_AcctIPv6OutputPackets18']
df_AcctIPv6OutputPackets['498_AcctIPv6OutputPackets19'] = df2['498_AcctIPv6OutputPackets19']
df_AcctIPv6OutputPackets['492_AcctIPv6OutputPackets20'] = df2['492_AcctIPv6OutputPackets20']

df_AcctIPv6OutputPackets['486_AcctIPv6OutputPackets21'] = df2['486_AcctIPv6OutputPackets21']
df_AcctIPv6OutputPackets['480_AcctIPv6OutputPackets22'] = df2['480_AcctIPv6OutputPackets22']
df_AcctIPv6OutputPackets['474_AcctIPv6OutputPackets23'] = df2['474_AcctIPv6OutputPackets23']
df_AcctIPv6OutputPackets['468_AcctIPv6OutputPackets24'] = df2['468_AcctIPv6OutputPackets24']
df_AcctIPv6OutputPackets['462_AcctIPv6OutputPackets25'] = df2['462_AcctIPv6OutputPackets25']
df_AcctIPv6OutputPackets['456_AcctIPv6OutputPackets26'] = df2['456_AcctIPv6OutputPackets26']
df_AcctIPv6OutputPackets['450_AcctIPv6OutputPackets27'] = df2['450_AcctIPv6OutputPackets27']
df_AcctIPv6OutputPackets['444_AcctIPv6OutputPackets28'] = df2['444_AcctIPv6OutputPackets28']
df_AcctIPv6OutputPackets['438_AcctIPv6OutputPackets29'] = df2['438_AcctIPv6OutputPackets29']
df_AcctIPv6OutputPackets['432_AcctIPv6OutputPackets30'] = df2['432_AcctIPv6OutputPackets30']


# In[ ]:


tmp_df_AcctIPv6InputPacketssum.info(verbose=True, null_counts=True)


# In[ ]:


df_SendKBytessum['设备号'] = df2['设备号']
df_ReceiveKBytessum['设备号'] = df2['设备号']
df_AcctIPv6InputOctetssum['设备号'] = df2['设备号']
df_AcctIPv6OutputOctetssum['设备号'] = df2['设备号']
df_AcctIPv6InputPacketssum['设备号'] = df2['设备号']
df_AcctIPv6OutputPackets['设备号'] = df2['设备号']


# In[ ]:


df_OLTTXPower=df_OLTTXPower.fillna(0)
df_OLTRXPower=df_OLTRXPower.fillna(0)
df_ONU_TX_POWER=df_ONU_TX_POWER.fillna(0)
df_ONU_ONU_RX_POWER=df_ONU_ONU_RX_POWER.fillna(0)


# In[ ]:


df_SendKBytessum=df_SendKBytessum.fillna(0)
df_ReceiveKBytessum=df_ReceiveKBytessum.fillna(0)
df_AcctIPv6InputOctetssum=df_AcctIPv6InputOctetssum.fillna(0)
df_AcctIPv6OutputOctetssum=df_AcctIPv6OutputOctetssum.fillna(0)
df_AcctIPv6InputPacketssum=df_AcctIPv6InputPacketssum.fillna(0)
df_AcctIPv6OutputPackets=df_AcctIPv6OutputPackets.fillna(0)


# In[ ]:


df_AcctIPv6OutputPackets.shape


# In[ ]:


df_OLTTXPower_tmp = df_OLTTXPower.set_index(['设备号']).stack().reset_index()
df_OLTRXPower_tmp = df_OLTRXPower.set_index(['设备号']).stack().reset_index()
df_ONU_TX_POWER_tmp = df_ONU_TX_POWER.set_index(['设备号']).stack().reset_index()
df_ONU_ONU_RX_POWER_tmp = df_ONU_ONU_RX_POWER.set_index(['设备号']).stack().reset_index()
df_SendKBytessum_tmp = df_SendKBytessum.set_index(['设备号']).stack().reset_index()
df_ReceiveKBytessum_tmp = df_ReceiveKBytessum.set_index(['设备号']).stack().reset_index()
df_AcctIPv6InputOctetssum_tmp = df_AcctIPv6InputOctetssum.set_index(['设备号']).stack().reset_index()
df_AcctIPv6OutputOctetssum_tmp = df_AcctIPv6OutputOctetssum.set_index(['设备号']).stack().reset_index()
df_AcctIPv6InputPacketssum_tmp = df_AcctIPv6InputPacketssum.set_index(['设备号']).stack().reset_index()
df_AcctIPv6OutputPackets_tmp = df_AcctIPv6OutputPackets.set_index(['设备号']).stack().reset_index()


# In[ ]:


df_OLTTXPower_tmp.rename(columns={0:'OLTTXPowe'}, inplace=True)
df_OLTRXPower_tmp.rename(columns={0:'OLTRXPower'}, inplace=True)
df_ONU_TX_POWER_tmp.rename(columns={0:'ONU_TX_POWER'}, inplace=True)
df_ONU_ONU_RX_POWER_tmp.rename(columns={0:'ONU_RX_POWER'}, inplace=True)
df_SendKBytessum_tmp.rename(columns={0:'SendKBytessu'}, inplace=True)
df_ReceiveKBytessum_tmp.rename(columns={0:'ReceiveKBytessum'}, inplace=True)
df_AcctIPv6InputOctetssum_tmp.rename(columns={0:'AcctIPv6InputOctetssum'}, inplace=True)
df_AcctIPv6OutputOctetssum_tmp.rename(columns={0:'AcctIPv6OutputOctetssum'}, inplace=True)
df_AcctIPv6InputPacketssum_tmp.rename(columns={0:'AcctIPv6InputPacketssum'}, inplace=True)
df_AcctIPv6OutputPackets_tmp.rename(columns={0:'AcctIPv6OutputPackets'}, inplace=True)


# In[ ]:


df_SendKBytessum_tmp['ReceiveKBytessum']=df_ReceiveKBytessum_tmp['ReceiveKBytessum']
df_SendKBytessum_tmp['AcctIPv6InputOctetssum']=df_AcctIPv6InputOctetssum_tmp['AcctIPv6InputOctetssum']
df_SendKBytessum_tmp['AcctIPv6OutputOctetssum']=df_AcctIPv6OutputOctetssum_tmp['AcctIPv6OutputOctetssum']
df_SendKBytessum_tmp['AcctIPv6InputPacketssum']=df_AcctIPv6InputPacketssum_tmp['AcctIPv6InputPacketssum']
df_SendKBytessum_tmp['AcctIPv6OutputPackets']=df_AcctIPv6OutputPackets_tmp['AcctIPv6OutputPackets']
df_SendKBytessum_tmp['OLTTXPowe']=df_OLTTXPower_tmp['OLTTXPowe']
df_SendKBytessum_tmp['OLTRXPower']=df_OLTRXPower_tmp['OLTRXPower']
df_SendKBytessum_tmp['ONU_TX_POWER']=df_ONU_TX_POWER_tmp['ONU_TX_POWER']
df_SendKBytessum_tmp['ONU_RX_POWER']=df_ONU_ONU_RX_POWER_tmp['ONU_RX_POWER']


# In[ ]:





# In[ ]:


df_OLTTXPower_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_OLTRXPower_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_ONU_TX_POWER_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_ONU_ONU_RX_POWER_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_SendKBytessum_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_ReceiveKBytessum_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_AcctIPv6InputOctetssum_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_AcctIPv6OutputOctetssum_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_AcctIPv6InputPacketssum_tmp.rename(columns={'level_1':'time'}, inplace=True)
df_AcctIPv6OutputPackets_tmp.rename(columns={'level_1':'time'}, inplace=True)


# In[ ]:


df_SendKBytessum_tmp.info(verbose=True, null_counts=True)


# In[ ]:


df_SendKBytessum_tmp.to_csv('df_time.csv',index=False)


# In[ ]:


print(df_SendKBytessum_tmp)


# In[ ]:


df = df.drop_duplicates(subset=['设备号'])


# In[ ]:


df.shape


# In[ ]:


df_time = pd.read_csv('G-newF_1.csv')


# In[ ]:


#每个字段前加上序号，解决列名同名问题
df_time = df_time.rename(columns={col: f"{i}_{col}" for i, col in enumerate(df_time.columns)})
import re
#去除字段名中汉字和常规符号以外的符号
df_time = df_time.rename(columns = lambda x:re.sub('[^A-Za-z0-9\u4e00-\u9fa5_]+', '', x))


# In[ ]:


df_time.rename(columns={'7890_设备号':'设备号'}, inplace=True)


# In[ ]:


new_df = pd.merge(df,df_time,on = ['设备号'],  sort=False,how='left')


# In[ ]:


new_df.shape


# In[ ]:


new_df = new_df.drop(['设备号'], axis=1)


# In[ ]:





# In[ ]:


df_target = new_df['35_oneanswer']
new_df = new_df.drop(['35_oneanswer'], axis=1)


# In[ ]:


##丢弃空值率大于80%的列
pct_null = new_df.isnull().sum() / len(new_df)
missing_features = pct_null[pct_null > 0.70].index
new_df.drop(missing_features, axis=1, inplace=True)


# In[ ]:


new_df.shape


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test, y_train, y_test = train_test_split(new_df,df_target,test_size=0.1, random_state=2021)


# In[ ]:


y_test.shape


# In[ ]:


X_train['value'] = y_train


# In[ ]:


#df = df.drop(['35_oneanswer'], axis=1)


# In[ ]:


target = X_train['value']


# In[ ]:


# 选择相关性大于0.05的作为候选特征参与训练，并加入我们认为比较重要的特征，总共66个特征参与训练
#features = (X_train.corr()['value'][abs(X_train.corr()['value'])!='K']).index

#features = features.values.tolist()

features = X_train.columns.values.tolist()
features.remove('value')
len(features)


# In[ ]:


# 生成数据和标签
#target = train_data['value']

train_selected = X_train[features]
test = X_test[features]
feature_importance_df = pd.DataFrame()
oof = np.zeros(len(train_selected))
predictions = np.zeros(len(test))

#train_selected['group'] = train_data['group']
#test['group'] = test_data['group']


# In[ ]:


#train_selected.info(verbose=True, null_counts=True)


# In[ ]:


#X_test.shape


# In[ ]:


#train_selected['group']=train_selected['group'].fillna(0)
#test['group']=test['group'].fillna(0)


# In[ ]:


cat=['1_CUST_PROV_ID','2_CUST_AREA_ID','3_CUST_STAR_CODE','4_SIX_SHEET_TYPE_CODE','5_SERV_TYPE_ID','6_BIG_TYPE_CODE','7_SMALL_TYPE_CODE','8_GIS_LATLON',  
'9_IS_DISPATCH_CLOUD','10_ACCEPT_CHANNEL_CODE','11_IS_ONLINE_COMPLETE','12_IS_BROADBAND','13_NET_TYPE','14_IS_5G','15_menu_type','16_net_type','17_net_question_type',
'18_net_question','19_TS_Type','25_产品规格标识','26_接入方式','27_ONU设备ID','28_一级分光器ID','29_二级分光器ID','30_末级分光器ID','31_PON口ID','32_OLT设备ID','33_productname',  
'34_brotype','36_MANAGE_IPADDRESS','37_NMS_ORIG_RES_NAME','40_ORI_NMS_ORIG_RES_NAME','41_EQP_SEQUENCE','42_EQP_LOID','161_地市','162_区县','163_小区编码','164_OLTIP' , 
'165_OLT设备名称','166_OLT厂家','167_BRASIP','168_ONU设备型号','169_device_id','170_modelname','171_numberofsubuser','172_description','173_productclass','174_manufacturer','175_hardwareversion' ,
'176_softwareversion','177_wantype','183_x_cu_band','185_x_cu_os','197_lan_lanethernetinterfaceconfig_1_status','198_lan_lanethernetinterfaceconfig_2_status',  
'199_lan_lanethernetinterfaceconfig_3_status', '200_lan_lanethernetinterfaceconfig_4_status','201_lan_lanethernetinterfaceconfig_1_maxbitrate_lan',  
'202_lan_lanethernetinterfaceconfig_2_maxbitrate_lan','203_lan_lanethernetinterfaceconfig_3_maxbitrate_lan','204_lan_lanethernetinterfaceconfig_4_maxbitrate_lan',  
'205_lan_lanethernetinterfaceconfig_1_x_cu_adaptrate','206_lan_lanethernetinterfaceconfig_2_x_cu_adaptrate','207_lan_lanethernetinterfaceconfig_3_x_cu_adaptrate',  
'208_lan_lanethernetinterfaceconfig_4_x_cu_adaptrate','209_lan_lanethernetinterfaceconfig_1_duplexmode','210_lan_lanethernetinterfaceconfig_2_duplexmode',  
'211_lan_lanethernetinterfaceconfig_3_duplexmode','212_lan_lanethernetinterfaceconfig_4_duplexmode','234_lan_lanethernetinterfaceconfig_5_status',  
'253_wlan_maxbitrate','254_wlan_wpaauthenticationmode','391_wan_wanpppconnection_i','392_wan_wanpppconnectionnumberofentries']


# In[ ]:


params = {'num_leaves': 10,
         'min_data_in_leaf': 14,
         'objective': 'regression',
         'max_bin':15,
         'max_depth':255,
         'learning_rate': 0.01,
         'boosting': 'gbdt',
        # 'bagging_freq': 5,
         'bagging_fraction': 0.8,   # 每次迭代时用的数据比例0.8
         'feature_fraction': 0.8,# 每次迭代中随机选择80％的参数来建树0.8201
         'bagging_seed': 11,  #  
         'reg_alpha': 1.728910519108444,#
         'reg_lambda': 4.9847051755586085,#
    #  'random_state': 42,
         'metric': 'mae',
        # 'verbosity': -1,
         'is_unbalance':True,
        # 'subsample': 0.81,#
         'min_gain_to_split': 0.01077313523861969,#
         'min_child_weight': 19.428902804238373,#
        'num_threads': -1,
         'device': 'gpu',
         'gpu_platform_id':0,
         'gpu_device_id':0,
         'seed':2021}
       

kfolds = KFold(n_splits=5,shuffle=True,random_state=15)
predictions = np.zeros(len(test))

#categorical_feature=
#cat=['fact_name','miit_net','user_dinner','user_sex','user_lv','is_voice_cover','rat','cell_type','is_dual','is_l900','is_5g','is_volte','is_volte_sign','user_status','is_mix','is_lucknumber','is_5g_dinner','in_net_group','acct_charge_type','gprs_bytes_type','complaint_level','used_2g','used_3g','used_4g','used_5g','user_age'] 
for fold_n,(trn_index,val_index) in enumerate(kfolds.split(train_selected,target)):
    print("fold_n {}".format(fold_n))
    trn_data = lgb.Dataset(train_selected.iloc[trn_index],label=target.iloc[trn_index])
    val_data = lgb.Dataset(train_selected.iloc[val_index],label=target.iloc[val_index])
    num_round=30000
    clf = lgb.train(params, trn_data, num_round, valid_sets = [trn_data, val_data], verbose_eval=200, early_stopping_rounds = 1000,categorical_feature=cat)#,cat
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


best_features.to_csv('best_features.csv',index=False)


# In[ ]:


# 计算结果
submision_lgb1=test
submision_lgb1['value']=predictions
submision_lgb1['value'].to_csv('G-submision_lgb1.csv',index=False)


# In[ ]:


y_test = pd.DataFrame(y_test)


# In[ ]:


print(y_test)


# In[ ]:


predictions_lgb_R = submision_lgb1['value']
predictions_lgb_R = pd.DataFrame(predictions_lgb_R)
predictions_lgb_R['y_test'] = y_test['35_oneanswer']
predictions_lgb_R.to_csv('G-predictions_lgb_R.csv',index=False)



# In[ ]:




