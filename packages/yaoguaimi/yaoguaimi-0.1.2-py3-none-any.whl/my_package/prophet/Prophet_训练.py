#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import pandas as pd 
import numpy as np
from prophet import Prophet
from pandas.plotting import register_matplotlib_converters
import warnings
import datetime
from scipy import stats
#import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
get_ipython().run_line_magic('matplotlib', 'inline')
#from fbprophet.plot import add_changepoints_to_plot
#from fbprophet.diagnostics import cross_validation
#from fbprophet.plot import plot_cross_validation_metric
#from fbprophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation
from prophet.plot import add_changepoints_to_plot
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import performance_metrics



warnings.filterwarnings("ignore")
import os
#os.environ['NUMEXPR_MAX_THREADS'] = '64'


# In[ ]:


# ================================ 异常值检测 ================================

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


#c1,c2,c6
new_train_data = pd.read_csv('new_df_处理异常值_缺失_new.csv')
c0_c8_data = pd.read_csv('new_改进.csv')#new_改进  #new_c1_c8_预测.csv 10.50
c0_c8_data_new = pd.read_csv('new_c1_c8_预测.csv')


# In[ ]:


new_train_data.head


# In[ ]:


c0_c8_data = c0_c8_data.drop(['c0'], axis=1)
c0_c8_data['c1']=c0_c8_data_new['c1']
c0_c8_data['c2']=c0_c8_data_new['c2']
c0_c8_data['c3']=c0_c8_data_new['c3']


# In[ ]:


#new_train_data = handleOutlier(new_train_data)


# In[ ]:


#new_train_data = handleOutlier(new_train_data)
#c0_c8_data= handleOutlier(c0_c8_data)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#new_train_data=handleOutlier(new_train_data,cols='y')
#df3.shape


# In[ ]:


aaa = pd.factorize(new_train_data['ID'])   #将ID号转为数字
new_train_data["ID"] = aaa[0]  #将ID号转为数字


# In[ ]:


print(new_train_data)


# In[ ]:


new_train_data.rename(columns={'time':'ds'}, inplace=True)#将原来的命名修改为算法要求的命名
new_train_data.rename(columns={'c0':'y'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'c1':'add_A'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'c2':'add_B'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'c3':'add_C'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'c4':'add_D'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'c5':'add_E'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'c6':'add_F'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'c7':'add_G'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'c8':'add_H'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data['ds']=new_train_data['ds'].map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d'))
#new_train_data['ds'] = pd.to_datetime(new_train_data['ds'], format ='%Y-%m-%d %H:%M')


# In[ ]:


print(new_train_data['ds'].max())
print(new_train_data['ds'].min())


# In[ ]:


print(new_train_data['y'])
train_data_2=pd.DataFrame()
new_train_data.head


# In[ ]:


'''
train_data_2['y']=new_train_data['y']
feature_columns = [col for col in train_data_2.columns if col not in ['ds']]
min_max_scaler = preprocessing.MinMaxScaler()
min_max_scaler = min_max_scaler.fit(train_data_2[feature_columns])
train_data_scaler = min_max_scaler.transform(train_data_2[feature_columns])

train_data_scaler=pd.DataFrame(train_data_scaler)
train_data_scaler.rename(columns={0:'y'}, inplace = True)
train_data_scaler['ds']=new_train_data['ds']
train_data_scaler['sc_eci']=new_train_data['sc_eci']
train_data_scaler.head
'''


# In[ ]:


ScNumberList = list(new_train_data['ID'].unique())
all_error = 0
i = 1
R_all_error=0


# In[ ]:


print(ScNumberList)


# In[ ]:


'''
open_day_mean='2021-11-21'
close_day_mean='2022-01-07'
con_2020_1=new_train_data['ds']>=open_day_mean
con2_2020_2=new_train_data['ds']<close_day_mean
con2_2021_all=new_train_data[con_2020_1&con2_2020_2]
#con2_2021_all.loc[(con2_2021_all['ds'] > '2019-01-01') & (con2_2021_all['ds'] < '2021-02-28'), 'y'] = None
'''


# In[ ]:


con2_2021_all = new_train_data.copy()


# In[ ]:


#ScNumberListhandle = [28,38,39,41,46,48,51,62,79]


# In[ ]:


#con2_2021_all = con2_2021_all.fillna(method = "bfill").fillna(method = "pad")
con2_2021_all['c1'] = con2_2021_all['c1'].fillna(method = "bfill").fillna(method = "pad")
con2_2021_all['c2'] = con2_2021_all['c2'].fillna(method = "bfill").fillna(method = "pad")
con2_2021_all['c3'] = con2_2021_all['c3'].fillna(method = "bfill").fillna(method = "pad")
con2_2021_all['c4'] = con2_2021_all['c4'].fillna(method = "bfill").fillna(method = "pad")
con2_2021_all['c5'] = con2_2021_all['c5'].fillna(method = "bfill").fillna(method = "pad")
con2_2021_all['c6'] = con2_2021_all['c6'].fillna(method = "bfill").fillna(method = "pad")
con2_2021_all['c7'] = con2_2021_all['c7'].fillna(method = "bfill").fillna(method = "pad")
con2_2021_all['c8'] = con2_2021_all['c8'].fillna(method = "bfill").fillna(method = "pad")




# In[ ]:


new_data=pd.DataFrame()
for num in ScNumberList:   
    df1 = pd.DataFrame()
    df1 = con2_2021_all[(con2_2021_all['ID']==num)].copy()  
    #print(len(df1))   
    open_day_mean='2021-12-22'
    close_day_mean='2021-12-25'
    con_mean=df1['ds']>=open_day_mean
    con2_mean=df1['ds']<close_day_mean
    forecast_mean=df1[con_mean&con2_mean]
    temp_mean=forecast_mean['y'].max()
   

    #if num in ScNumberListhandle:
    #df1=handleOutlier(df1)  
   # df1=handleOutlier(df1,cols='c1')  
   # df1=handleOutlier(df1,cols='c2')  
   # df1=handleOutlier(df1,cols='c3') 
   # df1=handleOutlier(df1,cols='c4') 
   # df1=handleOutlier(df1,cols='c5') 
   # df1=handleOutlier(df1,cols='c6') 
   # df1=handleOutlier(df1,cols='c7') 
   # df1=handleOutlier(df1,cols='c8') 
    new_m='m'+str(num)
    new_m = Prophet(
                    changepoint_range=0.95,#表示突变点（即斜率突变的点）所在的范围，如所有的突变点是基于前80%的历史数据的  #0.55
                   # changepoints=['2021-02-13'],
                    #n_changepoints=24,
                    #holidays=holidays,  
                   # holidays_prior_scale=10, #调节节假日模型组件的强度。值越大，该节假日对模型的影响越大，值越小，节假日的影响越小，默认值：10.0。
                    changepoint_prior_scale=0.9,#增长趋势模型的灵活度。调节”changepoint”选择的灵活度，值越大，选择的”changepoint”越多，从而使模型对历史数据的拟合程度变强，然而也增加了过拟合的风险。默认值：0.05。
               # interval_width=0.8,  #衡量未来时间内趋势改变的程度。表示预测未来时使用的趋势间隔出现的频率和幅度与历史数据的相似度，值越大越相似，  
                                      #当mcmc_samples = 0时，该参数仅用于增长趋势模型的改变程度，当mcmc_samples > 0  时，该参数也包括了季节性趋势改变的程度。
               # yearly_seasonality=False,#表示周期性年份的傅立叶级数，当变化频率很高时，可以增大傅立叶级数  
                seasonality_prior_scale=10,#调节季节性组件的强度。值越大，模型将适应更强的季节性波动，值越小，越抑制季节性波动，默认值：10.0.           
                weekly_seasonality=True,#表示周期性周份的傅立叶级数，  
                growth='linear', #linear，logistic
                seasonality_mode='additive',#multiplicative，additive
                daily_seasonality=True, #表示周期性日份的傅立叶级数， 
               # mcmc_samples=10,          #mcmc采样，用于获得预测未来的不确定性。若大于0，将做mcmc样本的全贝叶斯推理，如果为0，将做最大后验估计，默认值：0。
                uncertainty_samples=1000,
                ) #用于估计未来时间的增长趋势间隔的仿真绘制数，默认值：1000。  
                  #对于表现出强烈季节性模式而非趋势变化的时间序列，强制趋势增长率持平可能会很有用。这可以通过growth=flat在创建模型时简单地传递来实现：  # Adding the last day, fitting from scratch
   # df1['cap'] = 3800
   # df1['floor'] = 0 
    new_m.add_regressor('c1')
    new_m.add_regressor('c2')
    new_m.add_regressor('c3')
    new_m.add_regressor('c4')
    new_m.add_regressor('c5')
    new_m.add_regressor('c6')
    new_m.add_regressor('c7')
    new_m.add_regressor('c8')
    new_m.add_country_holidays(country_name='CN')
    forecast = pd.DataFrame()
   # df1=handleOutlier(df1)
    new_m.fit(df1)
    future = new_m.make_future_dataframe(periods=24,freq='H') #92
   # print(future)
    
    j1=(i-1)*24
    j2=i*24
    c0_c8_temp = c0_c8_data.iloc[j1:j2]
    df3 = df1.drop(['ID','ds'], axis=1)
    df3  = pd.concat([df3, c0_c8_temp], axis=0)   
    df3 = df3.reset_index()
   # print(df1)
    future['c1'] = df3['c1']
    future['c2'] = df3['c2']
    future['c3'] = df3['c3']
    future['c4'] = df3['c4']
    future['c5'] = df3['c5']
    future['c6'] = df3['c6']
    future['c7'] = df3['c7']
    future['c8'] = df3['c8']
    #future=future.fillna(0)
    #future['cap'] = 4000

    forecast = new_m.predict(future)    

    fig = new_m.plot(forecast[-7*24:])
  
    fig = new_m.plot(forecast)

    plt.show()
   
    forecast2 = forecast.tail(24)     #forecast2=forecast[forecast['ds']=='2022-01-06']
    forecast2.rename(columns={'yhat':'value'}, inplace=True)#将原来的命名修改为算法要求的命名
    
    df2=pd.DataFrame()
    df2['value']=forecast2['value']
    #df2['value'][df2['value']<0]=temp_mean
    df2['site'] = num
    df2['ds'] = forecast2['ds']
    new_data = new_data.append(df2)
    
   
    
    mae_old = df1.fillna(method = "bfill").fillna(method = "pad")

   # mae_new =forecast['yhat'][:len(df1)]
    mae_new =forecast.head(len(df1))
   # print(mae_old['y'])
    mae_old=mae_old.head(len(df1))
    
    
    all_mean_error=mean_absolute_error(mae_old['y'],mae_new['yhat'])
    
    temp_metrics = forecast.tail(48)
    temp_metrics = temp_metrics.head(24)
    
    
    last_24 = df1.fillna(method = "bfill").fillna(method = "pad")

    
    last_24 = last_24.tail(24)
   # print(last_24)
    #print('--------------------------------------------------------------------------')
  #  print(temp_metrics)


    R_mean_error = mean_absolute_error(last_24['y'],temp_metrics['yhat'])
    R_all_error = R_all_error +R_mean_error
    my_error_mean = all_mean_error/352
    all_error = all_error + all_mean_error    
    mean_error = all_error/i
    mean_error_2 = all_error/len(new_data)
    R_error = R_all_error/i
    i+=1
  #  print("mse is",mean_squared_error(df1['y'].values,forecast['yhat'].values[:len(df1)]))
    print("mae is",all_mean_error,mean_error,mean_error_2,"最近24小时mae is",R_mean_error,R_error)
  #  print("mae is",all_mean_error,mean_error)
    print("站点-【%s】，总数据量-【%s】,最大流量-【%s】,最小流量-【%s】,参考流量-【%s】"%(num,len(new_data),df2['value'].max(),df2['value'].min(),temp_mean))


# In[ ]:


print(mae_new)


# In[ ]:





# In[ ]:


future.shape


# In[ ]:





# In[ ]:


print(new_data.max())
print(new_data.min())
predict_T3_2 = new_data.copy()
#predict_T3_2[predict_T3_2['value'] < 0] =0
#print(predict_T3_2.min())


# In[ ]:


'''
forecast3=pd.DataFrame()
forecast3['value']=predict_T3_2['value']
#forecast3=min_max_scaler.inverse_transform(forecast3)

forecast3=pd.DataFrame(forecast3)
forecast3.rename(columns={0:'value'}, inplace = True)
forecast3.head
'''


# In[ ]:


predict_T3_2.head


# In[ ]:


predict_T3_2['value'][predict_T3_2['value']<0].count()


# In[ ]:


predict_T3_2['value'][predict_T3_2['value']<0]=0


# In[ ]:


predict_T3_2['value'][predict_T3_2['value']<0].count()


# In[ ]:


#predict_T3_2 = predict_T3_2.round(2)


# In[ ]:





# In[ ]:


predict_T3_2['value'].to_csv('predict_day21_1_9.39.csv',index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




