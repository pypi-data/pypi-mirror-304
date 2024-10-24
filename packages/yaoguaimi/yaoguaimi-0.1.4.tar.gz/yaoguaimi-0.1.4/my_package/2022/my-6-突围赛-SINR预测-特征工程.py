#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from preprocessing import filterData, delData, fillNanList, dropDuplicate,\
    handleOutlier, minMaxScale, cate2Num,standardizeData,\
    discrete, tran_math_function, minMaxScale, standardizeData,\
    onehot_map, map_dict_tran, binary_map, pca_selection,dfs_feature,\
    continue_time, discrete_time, statistics_time


# In[ ]:


##数据读取
train_data_file ="datasets/@huangzx23#8f2c6daaed50c6137673dbe1c1de33a7/train_age.csv"
test_data_file = "datasets/@huangzx23#8f2c6daaed50c6137673dbe1c1de33a7/test_age.csv"
app_events_file = "datasets/@huangzx23#8f2c6daaed50c6137673dbe1c1de33a7/app_events.csv"
events_file = "datasets/@huangzx23#8f2c6daaed50c6137673dbe1c1de33a7/events.csv"
phone_device_model_file = "datasets/@huangzx23#8f2c6daaed50c6137673dbe1c1de33a7/phone_device_model.csv"
app_data_file = "datasets/@huangzx23#8f2c6daaed50c6137673dbe1c1de33a7/app_data.csv"

train_data= pd.read_csv(train_data_file)
test_data= pd.read_csv(test_data_file)
train_data_MR= pd.read_csv(train_data_MR_file)
test_data_KPI= pd.read_csv(test_data_KPI_file)
test_data_MR= pd.read_csv(test_data_MR_file)


# In[ ]:


train_data_DT = train_data_DT.fillna(method = "bfill").fillna(method = "pad")


# In[ ]:


#数据集压缩
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
train_data_DT_new = train_data_DT.copy()
train_data_DT_new=reduce_mem_usage(train_data_DT_new)
train_data_KPI_new = train_data_KPI.copy()
train_data_KPI_new=reduce_mem_usage(train_data_KPI_new)
train_data_MR_new = train_data_MR.copy()
train_data_MR_new=reduce_mem_usage(train_data_MR_new)
test_data_KPI_new = test_data_KPI.copy()
test_data_KPI_new=reduce_mem_usage(test_data_KPI_new)
test_data_MR_new = test_data_MR.copy()
test_data_MR_new=reduce_mem_usage(test_data_MR_new)


# In[ ]:


train_data_DT_new_1 =train_data_DT.copy()


# In[ ]:


#DT表处理
train_data_DT_new_1 = train_data_DT_new_1.dropna(axis='index', how='all', subset=['RSRQ','RSRP','RSSI']) #丢弃'RSSI','RSRP','SINR','RSSI'列为空值的行


# In[ ]:


train_data_DT_new_1.drop(["Longitude","Latitude","PDCCH Grant Count DL/s",'PDCCH Grant Count UL/s','PDSCH BLER', 'PUSCH BLER', 'Rank2 CQI Code0',
       'Rank2 CQI Code1'],axis=1,inplace=True)


# In[ ]:


train_data_DT_new_1.drop(['PUSCH RB Count/s', 'PDSCH RB Count/s', 'Cell 1st EARFCN',
       'Cell 1st PCI', 'Cell 1st RSRP', 'Cell 1st RSRQ', 'Cell 2nd EARFCN',
       'Cell 2nd PCI', 'Cell 2nd RSRP', 'Cell 2nd RSRQ', 'Cell 3rd EARFCN',
       'Cell 3rd PCI', 'Cell 3rd RSRP', 'Cell 3rd RSRQ', 'Cell 4th EARFCN',
       'Cell 4th PCI', 'Cell 4th RSRP', 'Cell 4th RSRQ', 'Cell 5th EARFCN',
       'Cell 5th PCI', 'Cell 5th RSRP', 'Cell 5th RSRQ', 'Cell 6th EARFCN',
       'Cell 6th PCI', 'Cell 6th RSRP', 'Cell 6th RSRQ', '1st RSSI',
       '2nd RSSI', '3rd RSSI', '4th RSSI', '5th RSSI', '6th RSSI'],axis=1,inplace=True)


# In[ ]:


print(train_data_DT_new_1.columns)


# In[ ]:


new_train_data_DT=train_data_DT_new_1.copy()


# In[ ]:


print(new_train_data_DT.columns)


# In[ ]:


##离散化 MR和SINR的时间序列

timecol="ComputerTime"
new_train_data_DT=discrete_time(new_train_data_DT,timecol)


# In[ ]:


#聚合DT时间
new_train_data_DT['ds']=new_train_data_DT['ECI'].astype('str').str.cat(new_train_data_DT['Year'].astype('str'),sep='.')
new_train_data_DT['ds']=new_train_data_DT['ds'].astype('str').str.cat(new_train_data_DT['Month'].astype('str'),sep='.')
new_train_data_DT['ds']=new_train_data_DT['ds'].astype('str').str.cat(new_train_data_DT['Day'].astype('str'),sep='.')
new_train_data_DT['ds']=new_train_data_DT['ds'].astype('str').str.cat(new_train_data_DT['Hour'].astype('str'),sep='.')
new_train_data_DT['ds']=new_train_data_DT['ds'].astype('str').str.cat(new_train_data_DT['Minute'].astype('str'),sep='.')
new_train_data_DT['ds']=new_train_data_DT['ds'].astype('str').str.cat(new_train_data_DT['Second'].astype('str'),sep='.')


# In[ ]:


print(new_train_data_DT)


# In[ ]:


#按秒分组分组DT
new_train_data_DT_second=new_train_data_DT.groupby([new_train_data_DT['ECI'],new_train_data_DT['Year'],  
                                                   new_train_data_DT['Month'],new_train_data_DT['Day'],  
                                                   new_train_data_DT['Hour'],new_train_data_DT['Minute'],  
                                                  new_train_data_DT['Second']]).mean()
new_train_data_DT_second = new_train_data_DT_second.reset_index()


# In[ ]:


new_train_data_DT_second.to_csv('new_train_data_DT_second.csv',index=False)


# In[ ]:


train_data_MR_new_1 = train_data_MR_new.copy()


# In[ ]:


print(train_data_MR_new_1.columns)


# In[ ]:


train_data_MR_new_1.drop( ['cqi', 'cqi0', 'cqi1','sc_dlrstxpower', 'sc_thermalnoisepower', 'imsi', 'msisdn','imei', 'longitude', 'latitude','city'],axis=1,inplace=True)


# In[ ]:


print(train_data_MR_new_1.columns)


# In[ ]:


##离散 MR和SINR的时间序列

timecol="sdate"
train_data_MR_new_1=discrete_time(train_data_MR_new_1,timecol)


# In[ ]:


new_train_data_DT_second.rename(columns={'ECI':'sc_eci'}, inplace=True)
new_train_data_DT_second.rename(columns={'ComputerTime':'sdate'}, inplace=True)


# In[ ]:


#聚合MR时间
train_data_MR_new_1['ds']=train_data_MR_new_1['sc_eci'].astype('str').str.cat(train_data_MR_new_1['Year'].astype('str'),sep='.')
train_data_MR_new_1['ds']=train_data_MR_new_1['ds'].astype('str').str.cat(train_data_MR_new_1['Month'].astype('str'),sep='.')
train_data_MR_new_1['ds']=train_data_MR_new_1['ds'].astype('str').str.cat(train_data_MR_new_1['Day'].astype('str'),sep='.')
train_data_MR_new_1['ds']=train_data_MR_new_1['ds'].astype('str').str.cat(train_data_MR_new_1['Hour'].astype('str'),sep='.')
train_data_MR_new_1['ds']=train_data_MR_new_1['ds'].astype('str').str.cat(train_data_MR_new_1['Minute'].astype('str'),sep='.')
train_data_MR_new_1['ds']=train_data_MR_new_1['ds'].astype('str').str.cat(train_data_MR_new_1['Second'].astype('str'),sep='.')


# In[ ]:


#合并新MR集---------------------OK
new_train_dain_MR_Second = pd.merge(train_data_MR_new_1,new_train_data_DT_second,on =  
                             ['sc_eci','Year','Month','Day','Hour','Minute','Second'],  
                             sort=False,how='left')


# In[ ]:


new_train_dain_MR_Second.to_csv('new_train_dain_MR_Second.csv',index=False)


# In[ ]:


new_train_dain_MR_15S = new_train_dain_MR_Second.copy()


# In[ ]:


print (new_train_dain_MR_15S['SINR'].isnull().sum())


# In[ ]:


new_train_dain_MR_15S.shape


# In[ ]:


new_train_dain_MR_2 = new_train_dain_MR_15S.copy()
train_DT_new_4 = new_train_data_DT_second.copy()
train_DT_new_sc = new_train_data_DT_second.copy()


# In[ ]:


print(new_train_dain_MR_2.columns)


# In[ ]:


new_train_dain_MR_2 = new_train_dain_MR_2.drop(['MU_second_x','DayOfWeek_x','DayOfYear_x', 'WeekOfYear_x', 'DayOfWeek_y', 'DayOfYear_y', 'WeekOfYear_y',
       'MU_second_y'],axis=1)


# In[ ]:


cols = new_train_dain_MR_2.columns.tolist()


# In[ ]:


print(cols)


# In[ ]:


cols2 = train_DT_new_sc.columns.tolist()


# In[ ]:


print(cols2)


# In[ ]:


#new_train_dain_MR_2.rename(columns={'ds_x':'ds'}, inplace=True)


# In[ ]:


print(new_train_dain_MR_2['SINR'].isnull().sum())


# In[ ]:


print(new_train_dain_MR_2['SINR'].isnull().sum())
train_DT_new_sc['ds']=train_DT_new_sc['sc_eci'].astype('str').str.cat(train_DT_new_sc['Year'].astype('str'),sep='.')
train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Month'].astype('str'),sep='.')
train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Day'].astype('str'),sep='.')
train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Hour'].astype('str'),sep='.')
train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Minute'].astype('str'),sep='.')
train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Second'].astype('str'),sep='.')
train_SINR_ds=pd.DataFrame()
#建立SINR字典map
train_SINR_ds['ds'] = train_DT_new_sc['ds']
train_SINR_ds['SINR'] = train_DT_new_sc['SINR']

mapping = train_SINR_ds.set_index('ds',).squeeze()

new_train_dain_MR_2['SINR'].fillna(new_train_dain_MR_2['ds'].map(mapping),inplace=True)

print(new_train_dain_MR_2['SINR'].isnull().sum())


# In[ ]:


#遍历填充空值秒反向
print(train_DT_new_sc.loc[0,'Second'] )  #显示原始秒
for i in range(60):
    i += 1
    train_DT_new_sc['Second']= train_DT_new_sc['Second']-1
    #聚合SINR集时间
    train_DT_new_sc['ds']=train_DT_new_sc['sc_eci'].astype('str').str.cat(train_DT_new_sc['Year'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Month'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Day'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Hour'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Minute'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Second'].astype('str'),sep='.')        
    train_SINR_new_8=pd.DataFrame()
    train_SINR_new_8['ds'] = train_DT_new_sc['ds']
    train_SINR_new_8['SINR'] = train_DT_new_sc['SINR']    
    mapping = train_SINR_new_8.set_index('ds',).squeeze()
    new_train_dain_MR_2['SINR'].fillna(new_train_dain_MR_2['ds'].map(mapping),inplace=True)
    print(i)
    print(new_train_dain_MR_2['SINR'].isnull().sum())
train_DT_new_sc['Second']= train_DT_new_sc['Second']+60 #还原时间
print('MR负向填充已经完成...........')
print('MRsecend已复原')
print(train_DT_new_sc.loc[0,'Second'] )    #验证复原秒


# In[ ]:


#遍历填充空值秒正向
print(train_DT_new_sc.loc[0,'Second'] )  #显示原始秒
for i in range(60):
    i += 1
    train_DT_new_sc['Second']= train_DT_new_sc['Second']+1
    #聚合SINR集时间
    train_DT_new_sc['ds']=train_DT_new_sc['sc_eci'].astype('str').str.cat(train_DT_new_sc['Year'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Month'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Day'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Hour'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Minute'].astype('str'),sep='.')
    train_DT_new_sc['ds']=train_DT_new_sc['ds'].astype('str').str.cat(train_DT_new_sc['Second'].astype('str'),sep='.')
    train_SINR_new_9=pd.DataFrame()
    train_SINR_new_9['ds'] = train_DT_new_sc['ds']
    train_SINR_new_9['SINR'] = train_DT_new_sc['SINR']    
    mapping = train_SINR_new_9.set_index('ds',).squeeze()
    new_train_dain_MR_2['SINR'].fillna(new_train_dain_MR_2['ds'].map(mapping),inplace=True)
    print(i)
    print(new_train_dain_MR_2['SINR'].isnull().sum())
train_DT_new_sc['Second']= train_DT_new_sc['Second']-60 #还原时间
print('MR正向填充已经完成...........')
print('MRsecend已复原')
print(train_DT_new_sc.loc[0,'Second'] )  #显示原始秒


# In[ ]:


###按分钟分组
#train_SINR_new_6 = new_train_data_DT.copy()

train_SINR_new_6 = new_train_data_DT['SINR'].groupby([new_train_data_DT['ECI'],new_train_data_DT['Year'],  
                                                   new_train_data_DT['Month'],new_train_data_DT['Day'],  
                                                   new_train_data_DT['Hour'],new_train_data_DT['Minute'],  
                                                   ]).mean()
train_SINR_new_6 = train_SINR_new_6.reset_index()
train_SINR_new_6.rename(columns={'ECI':'sc_eci'}, inplace=True)

new_train_dain_MR_3 = new_train_dain_MR_2.copy()


# In[ ]:


new_train_dain_MR_3['ds']=new_train_dain_MR_3['sc_eci'].astype('str').str.cat(new_train_dain_MR_3['Year'].astype('str'),sep='.')
new_train_dain_MR_3['ds']=new_train_dain_MR_3['ds'].astype('str').str.cat(new_train_dain_MR_3['Month'].astype('str'),sep='.')
new_train_dain_MR_3['ds']=new_train_dain_MR_3['ds'].astype('str').str.cat(new_train_dain_MR_3['Day'].astype('str'),sep='.')
new_train_dain_MR_3['ds']=new_train_dain_MR_3['ds'].astype('str').str.cat(new_train_dain_MR_3['Hour'].astype('str'),sep='.')
new_train_dain_MR_3['ds']=new_train_dain_MR_3['ds'].astype('str').str.cat(new_train_dain_MR_3['Minute'].astype('str'),sep='.')


# In[ ]:


print(new_train_dain_MR_3.columns)


# In[ ]:


train_SINR_new_6['ds']=train_SINR_new_6['sc_eci'].astype('str').str.cat(train_SINR_new_6['Year'].astype('str'),sep='.')
train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Month'].astype('str'),sep='.')
train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Day'].astype('str'),sep='.')
train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Hour'].astype('str'),sep='.')
train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Minute'].astype('str'),sep='.')


# In[ ]:


print(train_SINR_new_6.columns)


# In[ ]:


#不合并，原始分钟数填充一次
train_SINR_ds_1=pd.DataFrame()
train_SINR_ds_1['ds'] = train_SINR_new_6['ds']
train_SINR_ds_1['SINR'] = train_SINR_new_6['SINR']
mapping = train_SINR_ds_1.set_index('ds',).squeeze()
new_train_dain_MR_3['SINR'].fillna(new_train_dain_MR_3['ds'].map(mapping),inplace=True)
print(new_train_dain_MR_3['SINR'].isnull().sum())


# In[ ]:


print(train_SINR_new_6.loc[0,'Minute'] )  #显示原始分钟
#遍历填充空值分钟反向
for i in range(60):
    i += 1
    train_SINR_new_6['Minute']= train_SINR_new_6['Minute']-1
    #聚合SINR集时间
    train_SINR_new_6['ds']=train_SINR_new_6['sc_eci'].astype('str').str.cat(train_SINR_new_6['Year'].astype('str'),sep='.')
    train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Month'].astype('str'),sep='.')
    train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Day'].astype('str'),sep='.')
    train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Hour'].astype('str'),sep='.')
    train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Minute'].astype('str'),sep='.')
    train_SINR_new_10=pd.DataFrame()
    train_SINR_new_10['ds'] = train_SINR_new_6['ds']
    train_SINR_new_10['SINR'] = train_SINR_new_6['SINR']    
    mapping = train_SINR_new_10.set_index('ds',).squeeze()
    new_train_dain_MR_3['SINR'].fillna(new_train_dain_MR_3['ds'].map(mapping),inplace=True)
    print(i)
    print(new_train_dain_MR_3['SINR'].isnull().sum())
train_SINR_new_6['Minute']= train_SINR_new_6['Minute']+60 #还原时间
print('MRMinute负向填充已经完成...........')
print('MRMinutesecend已复原')
print(train_SINR_new_6.loc[0,'Minute'] ) 


# In[ ]:


print(train_SINR_new_6.loc[0,'Minute'] )  #显示原始分钟
#遍历填充空值分钟反向
for i in range(60):
    i += 1
    train_SINR_new_6['Minute']= train_SINR_new_6['Minute']+1
    #聚合SINR集时间
    train_SINR_new_6['ds']=train_SINR_new_6['sc_eci'].astype('str').str.cat(train_SINR_new_6['Year'].astype('str'),sep='.')
    train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Month'].astype('str'),sep='.')
    train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Day'].astype('str'),sep='.')
    train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Hour'].astype('str'),sep='.')
    train_SINR_new_6['ds']=train_SINR_new_6['ds'].astype('str').str.cat(train_SINR_new_6['Minute'].astype('str'),sep='.')
    train_SINR_new_11=pd.DataFrame()
    train_SINR_new_11['ds'] = train_SINR_new_6['ds']
    train_SINR_new_11['SINR'] = train_SINR_new_6['SINR']    
    mapping = train_SINR_new_11.set_index('ds',).squeeze()
    new_train_dain_MR_3['SINR'].fillna(new_train_dain_MR_3['ds'].map(mapping),inplace=True)
    print(i)
    print(new_train_dain_MR_3['SINR'].isnull().sum())
train_SINR_new_6['Minute']= train_SINR_new_6['Minute']-60 #还原时间
print('MRMinute负向填充已经完成...........')
print('MRMinut已复原')
print(train_SINR_new_6.loc[0,'Minute'] )  #显示原始分钟


# In[ ]:


#最后填充中位数
new_train_dain_MR_3['SINR'].fillna(new_train_dain_MR_3['SINR'].median(),inplace=True)
#new_train_dain_MR_3['SINR'].fillna(0,inplace=True)
print(new_train_dain_MR_3['SINR'].isnull().sum())


# In[ ]:


gr


# In[ ]:


new_train_dain_MR_4 = new_train_dain_MR_3.copy()


# In[ ]:


print(cols3)


# In[ ]:


cols4 = new_train_dain_MR_4.columns.tolist()


# In[ ]:


print(cols4)


# In[ ]:


#处理KPI表
new_train_data_KPI=train_data_KPI_new.copy()


# In[ ]:


#计算eci值
new_train_data_KPI['sc_eci']=new_train_data_KPI['ENBID']*256+new_train_data_KPI['LCRID']
timecol="START_DATE"
new_train_data_KPI=discrete_time(new_train_data_KPI,timecol)#离散时间 


# In[ ]:


#初始化时段（按分钟）
new_train_dain_MR_4['minute_part'] = 0


# In[ ]:


#划分时段
ki = len(new_train_dain_MR_4)
print(ki)

for i in range(ki):
   
    if 0 <= new_train_dain_MR_4.loc[i,'Minute'] < 15:        
        new_train_dain_MR_4.loc[i,'minute_part'] = 0
    
    if 15 <= new_train_dain_MR_4.loc[i,'Minute'] < 30:       
        new_train_dain_MR_4.loc[i,'minute_part'] = 15
    
    if 30 <= new_train_dain_MR_4.loc[i,'Minute'] < 45:        
        new_train_dain_MR_4.loc[i,'minute_part'] = 30
    
    if 45 <= new_train_dain_MR_4.loc[i,'Minute'] < 60:       
        new_train_dain_MR_4.loc[i,'minute_part'] = 45


# In[ ]:


new_train_data_KPI.rename(columns={'Minute':'minute_part'}, inplace=True)


# In[ ]:


#丢弃同名字段
#new_train_dain_MR_4 = new_train_dain_MR_4.drop('second',axis=1)
new_train_data_KPI = new_train_data_KPI.drop(['DayOfWeek','DayName','DayOfYear','WeekOfYear','Second','MU_second'],axis=1)


# In[ ]:


#对齐字段
new_train_dain_MR_4['ENBID_LCRID']=new_train_dain_MR_4['enbid'].astype('str').str.cat(new_train_dain_MR_4['sc_lcrid'].astype('str'),sep='_')


# In[ ]:


#合并MR
new_train_dain_MR_all = pd.merge(new_train_dain_MR_4,new_train_data_KPI,on =  
                             ['sc_eci','ENBID_LCRID','Year','Month','Day','Hour','minute_part'],  
                             sort=False,how='left')


# In[ ]:


#输也带重复值的表
new_train_dain_MR_all.to_csv('new_train_dain_MR_all_duplicates.csv',index=False)


# In[ ]:


test_data_KPI_new_1 = test_data_KPI_new.copy()
test_data_MR_new_1 = test_data_MR_new.copy()


# In[ ]:


#TEST集重复流程
test_data_KPI_new_1['sc_eci']=test_data_KPI_new_1['ENBID']*256+test_data_KPI_new_1['LCRID']
timecol="START_DATE"
test_data_KPI_new_1=discrete_time(test_data_KPI_new_1,timecol)
timecol="sdate"
test_data_MR_new_1=discrete_time(test_data_MR_new_1,timecol)


# In[ ]:


test_data_MR_new_1['minute_part'] = 0


# In[ ]:


ki = len(test_data_MR_new_1)
print(ki)
for i in range(ki):
   
    if 0 <= test_data_MR_new_1.loc[i,'Minute'] < 15:        
        test_data_MR_new_1.loc[i,'minute_part'] = 0
    
    if 15 <= test_data_MR_new_1.loc[i,'Minute'] < 30:       
        test_data_MR_new_1.loc[i,'minute_part'] = 15
    
    if 30 <= test_data_MR_new_1.loc[i,'Minute'] < 45:        
        test_data_MR_new_1.loc[i,'minute_part'] = 30
    
    if 45 <= test_data_MR_new_1.loc[i,'Minute'] < 60:       
        test_data_MR_new_1.loc[i,'minute_part'] = 45


# In[ ]:


test_data_KPI_new_1.rename(columns={'Minute':'minute_part'}, inplace=True)


# In[ ]:


test_data_MR_new_1 = test_data_MR_new_1.drop(['DayOfWeek','DayName','DayOfYear','WeekOfYear','Second','MU_second'],axis=1)
test_data_KPI_new_1 = test_data_KPI_new_1.drop(['DayOfWeek','DayName','DayOfYear','WeekOfYear','Second','MU_second'],axis=1)


# In[ ]:


test_data_MR_new_1['ENBID_LCRID']=test_data_MR_new_1['enbid'].astype('str').str.cat(test_data_MR_new_1['sc_lcrid'].astype('str'),sep='_')


# In[ ]:


new_test_data_MR_all = pd.merge(test_data_MR_new_1,test_data_KPI_new_1,on =  
                             ['sc_eci','ENBID_LCRID','Year','Month','Day','Hour','minute_part'],  
                             sort=False,how='left')


# In[ ]:


new_test_data_MR_all.to_csv('new_test_data_MR_all_New.csv',index=False)
#new_train_dain_MR_all.to_csv('new_train_dain_MR_all.csv',index=False)


# In[ ]:


#去除MR集中的重复值
Test_MR_all = new_train_dain_MR_all.drop_duplicates(subset=['sc_eci',
                                                            'sdate',  
                                                            '空口上行业务流量',  
                                                            '空口业务总流量',  
                                                            '空口下行业务流量',
                                                            '下行PRB平均占用率',
                                                            '上行PRB平均占用率',
                                                            'RRC连接平均数',
                                                            'RRC连接最大数',
                                                            'sc_lcrid',
                                                            'sc_rsrp',
                                                            'sc_rsrp',
                                                            'sc_phr',
                                                            'sc_tadv',
                                                            'sc_sinrul'])


# In[ ]:


Test_MR_all.to_csv('new_train_dain_MR_drop.csv',index=False)


# In[ ]:


Fu_train_data = Test_MR_all.copy()
Fu_test_data = new_test_data_MR_all.copy()


# In[ ]:


cols3 = Fu_train_data.columns.tolist()


# In[ ]:


print(cols3)


# In[ ]:


Fu_train_data = Fu_train_data.drop(['上行底噪','每E_RAB的流量','ds','SINR','EARFCN DL', 'PCI', 'RSRP', 'SINR', 'RSRQ', 'minute_part', 'ENBID_LCRID', 'START_DATE', 'START_HOUR', 'CITY_NAME', 'ENBID', 'LCRID',],axis=1)


# In[ ]:


cols5 = Fu_train_data.columns.tolist()


# In[ ]:


print(cols5)


# In[ ]:


Fu_train_data['SINR'] = Test_MR_all['SINR']


# In[ ]:


cols4 = Fu_test_data.columns.tolist()


# In[ ]:


print(cols4)


# In[ ]:


Fu_test_data = Fu_test_data.drop(['city','上行底噪','每E_RAB的流量','imsi', 'msisdn', 'imei', 'longitude', 'latitude', 'cqi', 'cqi0', 'cqi1', 'sc_dlrstxpower', 'sc_thermalnoisepower','CITY_NAME', 'ENBID', 'LCRID', 'ENBID_LCRID', 'START_DATE', ],axis=1)


# In[ ]:


print(Fu_train_data.columns)


# In[ ]:


Fu_train_data['E_RAB建立成功率']=Fu_train_data['E_RAB建立成功率']/100
Fu_train_data['RRC连接建立成功率']=Fu_train_data['RRC连接建立成功率']/100
Fu_train_data['RRC连接重建比率']=Fu_train_data['RRC连接重建比率']/100
Fu_train_data['PDCCH信道占用率']=Fu_train_data['PDCCH信道占用率']/100
Fu_train_data['下行PRB平均占用率']=Fu_train_data['下行PRB平均占用率']/100
Fu_train_data['上行PRB平均占用率']=Fu_train_data['上行PRB平均占用率']/100
Fu_train_data['ENB内切换出成功率']=Fu_train_data['ENB内切换出成功率']/100
Fu_train_data['ENB间X2切换出成功率']=Fu_train_data['ENB间X2切换出成功率']/100
Fu_train_data['RSRP大于等于－105的比例']=Fu_train_data['RSRP大于等于－105的比例']/100


# In[ ]:


Fu_test_data['E_RAB建立成功率']=Fu_test_data['E_RAB建立成功率']/100
Fu_test_data['RRC连接建立成功率']=Fu_test_data['RRC连接建立成功率']/100
Fu_test_data['RRC连接重建比率']=Fu_test_data['RRC连接重建比率']/100
Fu_test_data['PDCCH信道占用率']=Fu_test_data['PDCCH信道占用率']/100
Fu_test_data['下行PRB平均占用率']=Fu_test_data['下行PRB平均占用率']/100
Fu_test_data['上行PRB平均占用率']=Fu_test_data['上行PRB平均占用率']/100
Fu_test_data['ENB内切换出成功率']=Fu_test_data['ENB内切换出成功率']/100
Fu_test_data['ENB间X2切换出成功率']=Fu_test_data['ENB间X2切换出成功率']/100
Fu_test_data['RSRP大于等于－105的比例']=Fu_test_data['RSRP大于等于－105的比例']/100


# In[ ]:


Fu_train_data['无线接通率__1'] =Fu_train_data['RRC连接建立成功率']*Fu_train_data['E_RAB建立成功率']
Fu_test_data['无线接通率__1'] =Fu_test_data['RRC连接建立成功率']*Fu_test_data['E_RAB建立成功率']


# In[ ]:


Fu_train_data['RRC连接成功次数_2'] =Fu_train_data['RRC连接建立成功率']*Fu_train_data['RRC连接平均数']
Fu_test_data['RRC连接成功次数_2'] =Fu_test_data['RRC连接建立成功率']*Fu_test_data['RRC连接平均数']


# In[ ]:


Fu_train_data['RRC连接失败数_3'] =Fu_train_data['RRC连接重建比率']*Fu_train_data['RRC连接平均数']/(1-Fu_train_data['RRC连接重建比率'])
Fu_test_data['RRC连接失败数_3'] =Fu_test_data['RRC连接重建比率']*Fu_test_data['RRC连接平均数']/(1-Fu_test_data['RRC连接重建比率'])


# In[ ]:


Fu_train_data['电平差异值1']= abs(Fu_train_data['nc1_rsrp'] -Fu_train_data['sc_rsrp'])
Fu_train_data['电平差异值2']= abs(Fu_train_data['nc2_rsrp'] -Fu_train_data['sc_rsrp'])
Fu_train_data['电平差异值3']= abs(Fu_train_data['nc3_rsrp'] -Fu_train_data['sc_rsrp'])
Fu_train_data['电平差异值4']= abs(Fu_train_data['nc4_rsrp'] -Fu_train_data['sc_rsrp'])
Fu_train_data['电平差异值5']= abs(Fu_train_data['nc5_rsrp'] -Fu_train_data['sc_rsrp'])
Fu_train_data['电平差异值6']= abs(Fu_train_data['nc6_rsrp'] -Fu_train_data['sc_rsrp'])
Fu_train_data['电平差异值7']= abs(Fu_train_data['nc7_rsrp'] -Fu_train_data['sc_rsrp'])


# In[ ]:


Fu_test_data['电平差异值1']= abs(Fu_test_data['nc1_rsrp'] -Fu_test_data['sc_rsrp'])
Fu_test_data['电平差异值2']= abs(Fu_test_data['nc2_rsrp'] -Fu_test_data['sc_rsrp'])
Fu_test_data['电平差异值3']= abs(Fu_test_data['nc3_rsrp'] -Fu_test_data['sc_rsrp'])
Fu_test_data['电平差异值4']= abs(Fu_test_data['nc4_rsrp'] -Fu_test_data['sc_rsrp'])
Fu_test_data['电平差异值5']= abs(Fu_test_data['nc5_rsrp'] -Fu_test_data['sc_rsrp'])
Fu_test_data['电平差异值6']= abs(Fu_test_data['nc6_rsrp'] -Fu_test_data['sc_rsrp'])
Fu_test_data['电平差异值7']= abs(Fu_test_data['nc7_rsrp'] -Fu_test_data['sc_rsrp'])


# In[ ]:


Fu_train_data['上行业务信道占用PRB平均数_4'] =Fu_train_data['sc_puschprbnum']*Fu_train_data['上行PRB平均占用率']
Fu_test_data['上行业务信道占用PRB平均数_4'] =Fu_test_data['sc_puschprbnum']*Fu_test_data['上行PRB平均占用率']


# In[ ]:


Fu_train_data['下行业务信道占用PRB平均数_5'] =Fu_train_data['sc_pdschprbnum']*Fu_train_data['下行PRB平均占用率']
Fu_test_data['下行业务信道占用PRB平均数_5'] =Fu_test_data['sc_pdschprbnum']*Fu_test_data['下行PRB平均占用率']


# In[ ]:


Fu_train_data['下行每PRB流量流量_7'] =Fu_train_data['空口下行业务流量']/Fu_train_data['下行业务信道占用PRB平均数_5']
Fu_test_data['下行每PRB流量流量_7'] =Fu_test_data['空口下行业务流量']/Fu_test_data['下行业务信道占用PRB平均数_5']


# In[ ]:


Fu_train_data['上行每PRB流量流量_8'] =Fu_train_data['空口上行业务流量']/Fu_train_data['上行业务信道占用PRB平均数_4']
Fu_test_data['上行每PRB流量流量_8'] =Fu_test_data['空口上行业务流量']/Fu_test_data['上行业务信道占用PRB平均数_4']


# In[ ]:


Fu_train_data['总每PRB流量流量_9'] =Fu_train_data['空口业务总流量']/(Fu_train_data['上行业务信道占用PRB平均数_4']+Fu_train_data['下行业务信道占用PRB平均数_5'])
Fu_test_data['总每PRB流量流量_9'] =Fu_test_data['空口业务总流量']/(Fu_test_data['上行业务信道占用PRB平均数_4']+Fu_test_data['下行业务信道占用PRB平均数_5'])


# In[ ]:


Fu_train_data['总每PRB流量流量_9'] =Fu_train_data['空口业务总流量']/(Fu_train_data['上行业务信道占用PRB平均数_4']+Fu_train_data['下行业务信道占用PRB平均数_5'])


# In[ ]:


Fu_train_data['无线掉线率_6'] =Fu_train_data['E_RAB掉线率']/(1-Fu_train_data['UE上下文掉线率'])
Fu_test_data['无线掉线率_6'] =Fu_test_data['E_RAB掉线率']/(1-Fu_test_data['UE上下文掉线率'])


# In[ ]:


print(cols3)


# In[ ]:


Fu_train_data.to_csv('Fu_train_data_new_3.csv',index=False)


# In[ ]:


Fu_test_data.to_csv('Fu_test_data_new_3.csv',index=False)

