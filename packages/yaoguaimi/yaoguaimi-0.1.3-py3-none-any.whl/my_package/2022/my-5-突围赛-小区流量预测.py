#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import pandas as pd 
import numpy as np
from fbprophet import Prophet
from pandas.plotting import register_matplotlib_converters
import warnings
import datetime
from scipy import stats
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
get_ipython().run_line_magic('matplotlib', 'inline')
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric
from fbprophet.diagnostics import performance_metrics
warnings.filterwarnings("ignore")
import os
os.environ['NUMEXPR_MAX_THREADS'] = '64'


# In[ ]:


new_train_data = pd.read_csv('T3_newdata.csv')
new_train_data = reduce_mem_usage(new_train_data)


# In[ ]:


# 节假日数据

# 元旦
TF_2019yuandan=pd.DataFrame({
    'holiday':'2019 Yuan Dan',
    'ds':pd.to_datetime(['2019-1-1','2020-1-1','2021-1-1']),
      'lower_window': 0,
  'upper_window': 1,
})

# 清明节
TF_2019qinming=pd.DataFrame({
    'holiday':'2019 qin ming',
    'ds':pd.to_datetime(['2019-4-5','2020-4-5','2021-4-5']),
      'lower_window': -1,
  'upper_window': 2,
})

# 劳动节
TF_2019wuyi=pd.DataFrame({
    'holiday':'2019 wu yi',
    'ds':pd.to_datetime(['2019-5-1']),
      'lower_window': 0,
  'upper_window': 1,
})

TF_2020wuyi=pd.DataFrame({
    'holiday':'2020 wu yi',
    'ds':pd.to_datetime(['2020-5-1','2021-5-1']),
      'lower_window': 0,
  'upper_window': 5,
})


#端午节

TF_2019duanwu=pd.DataFrame({
    'holiday':'2019 wu yi',
    'ds':pd.to_datetime(['2019-6-7','2020-6-25','2021-6-12']),
      'lower_window': 0,
  'upper_window': 3,
})


#国庆节

TF_2019guoqin=pd.DataFrame({
    'holiday':'2019 guo qin',
    'ds':pd.to_datetime(['2019-10-1','2020-10-1','2021-10-1']),
      'lower_window': 0,
  'upper_window': 7,
})

#中秋节

TF_2019zhongqiu=pd.DataFrame({
    'holiday':'2019 zhong qiu ',
    'ds':pd.to_datetime(['2019-9-13','2020-10-1','2021-9-21']),
      'lower_window': 0,
  'upper_window': 1,
})


# 因为春节法定节日有一个星期，所以将春节的前后假日扩大至7天
# Spring Festival
# 春节
TF_2019Spring=pd.DataFrame({
    'holiday':'2019 Spring Festival',
    'ds':pd.to_datetime(['2019-2-5','2020-1-25','2021-2-12']),
      'lower_window': -2,
  'upper_window': 9,
})


# E-commerce festival 618
ECF_618 = pd.DataFrame({
  'holiday': 'ECF_618',
  'ds': pd.to_datetime(['2019-6-18','2020-6-18','2021-6-18']),
  'lower_window': 0,
  'upper_window': 1,
})
# E-commerce festival 1111
ECF_1111 = pd.DataFrame({
  'holiday': 'ECF_1111',
  'ds': pd.to_datetime(['2019-11-11','2020-11-11']),
  'lower_window': 0,
  'upper_window': 1,
})
# E-commerce festival 1212
ECF_1212 = pd.DataFrame({
  'holiday': 'ECF_1212',
  'ds': pd.to_datetime(['2019-12-12','2020-12-12']),
  'lower_window': 0,
  'upper_window': 1,
})
holidays=pd.concat((TF_2019yuandan,TF_2019qinming,TF_2019wuyi,TF_2020wuyi,TF_2019duanwu,  
                   TF_2019guoqin,TF_2019zhongqiu,TF_2019Spring,ECF_1111,ECF_618,ECF_1212))


# In[ ]:


#new_train_data.rename(columns={'sdate':'ds'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data.rename(columns={'dl_flow':'y'}, inplace=True)#将原来的命名修改为算法要求的命名
#new_train_data['ds']=new_train_data['ds'].map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d'))
new_train_data['ds'] = pd.to_datetime(new_train_data['ds'], format ='%Y-%m-%d')


# In[ ]:


new_train_data.head


# In[ ]:


print(new_train_data['y'].max())
print(new_train_data['y'].min())


# In[ ]:


#new_train_data=handleOutlier(new_train_data,cols='y')
print(new_train_data['y'].max())
print(new_train_data['y'].min())


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


#X1['y']=min_max_scaler.inverse_transform(train_data_scaler[0])
ScNumberList = list(new_train_data['sc_eci'].unique())
all_error = 0
i = 1


# In[ ]:


open_day_mean='2019-01-01'
close_day_mean='2021-03-01'
con_2020_1=new_train_data['ds']>=open_day_mean
con2_2020_2=new_train_data['ds']<close_day_mean
con2_2021_all=new_train_data[con_2020_1&con2_2020_2]
#con2_2021_all.loc[(con2_2021_all['ds'] > '2019-01-01') & (con2_2021_all['ds'] < '2021-02-28'), 'y'] = None


# In[ ]:


ScNumberList2 = filter(lambda x: x>1840,ScNumberList)
ScNumberList2 = list(ScNumberList2)


# In[ ]:


new_data=pd.DataFrame()
for num in ScNumberList:   
    #seasonality_mode='multiplicative'
    
    df1 = pd.DataFrame()
    df1 = con2_2021_all[(con2_2021_all['sc_eci']==num)].copy()  
    print(len(df1))
    df1=handleOutlier(df1,cols='y')
    #prediction_size = 100
   
    open_day_mean='2021-02-01'
    close_day_mean='2021-03-01'
    con_mean=df1['ds']>=open_day_mean
    con2_mean=df1['ds']<close_day_mean
    forecast_mean=df1[con_mean&con2_mean]
    temp_mean=forecast_mean['y'].mean()
  
    new_m='m'+str(num)
     
    new_m = Prophet(changepoint_range=0.8,#表示突变点（即斜率突变的点）所在的范围，如所有的突变点是基于前80%的历史数据的  #0.55
               # changepoints=['2021-02-13'],
                n_changepoints=25,
                holidays=holidays,  
                holidays_prior_scale=10, #调节节假日模型组件的强度。值越大，该节假日对模型的影响越大，值越小，节假日的影响越小，默认值：10.0。
                changepoint_prior_scale=0.04,#增长趋势模型的灵活度。调节”changepoint”选择的灵活度，值越大，选择的”changepoint”越多，从而使模型对历史数据的拟合程度变强，然而也增加了过拟合的风险。默认值：0.05。
                interval_width=0.8,  #衡量未来时间内趋势改变的程度。表示预测未来时使用的趋势间隔出现的频率和幅度与历史数据的相似度，值越大越相似，  
                                       #当mcmc_samples = 0时，该参数仅用于增长趋势模型的改变程度，当mcmc_samples > 0  时，该参数也包括了季节性趋势改变的程度。
                yearly_seasonality=True,#表示周期性年份的傅立叶级数，当变化频率很高时，可以增大傅立叶级数  
                seasonality_prior_scale=10,#调节季节性组件的强度。值越大，模型将适应更强的季节性波动，值越小，越抑制季节性波动，默认值：10.0.           
                weekly_seasonality=True,#表示周期性周份的傅立叶级数，  
                growth='linear',  #linear，logistic
                seasonality_mode='multiplicative',#multiplicative，additive
                daily_seasonality=False, #表示周期性日份的傅立叶级数， 
                mcmc_samples=20,          #mcmc采样，用于获得预测未来的不确定性。若大于0，将做mcmc样本的全贝叶斯推理，如果为0，将做最大后验估计，默认值：0。
                uncertainty_samples=1000,) #用于估计未来时间的增长趋势间隔的仿真绘制数，默认值：1000。  
                  #对于表现出强烈季节性模式而非趋势变化的时间序列，强制趋势增长率持平可能会很有用。这可以通过growth=flat在创建模型时简单地传递来实现：  # Adding the last day, fitting from scratch
    #new_m = Prophet().fit(df1, init=stan_init(m1))  # Adding the last day, warm-starting from m1
    #df1['cap'] = 70000
  #  df1['floor'] = 0 
   
    forecast = pd.DataFrame()
    new_m.fit(df1)
    
    future = new_m.make_future_dataframe(periods=92,freq='d') #92
    forecast = new_m.predict(future)    
   
    fig = new_m.plot(forecast)
    a = add_changepoints_to_plot(fig.gca(), new_m, forecast)
    
    plt.show()
    all_mean_error=mean_squared_error(df1['y'].values,forecast['yhat'].values[:len(df1)])
    open_day='2021-03-01'
    close_day='2021-06-01'
    con1=forecast['ds']>=open_day
    con2=forecast['ds']<close_day
    forecast2=forecast[con1&con2]
    forecast2=forecast2.drop(index=(forecast2.loc[(forecast2['ds']=='2021-04-30')].index))
    forecast2.rename(columns={'yhat':'value'}, inplace=True)#将原来的命名修改为算法要求的命名
    df2=pd.DataFrame()
    df2['value']=forecast2['value']
    df2['value'][df2['value']<0]=temp_mean
    df2['site'] = num
    df2['ds'] = forecast2['ds']
    
    new_data = new_data.append(df2)
    all_mean_error=mean_absolute_error(df1['y'].values,forecast['yhat'].values[:len(df1)])
    #my_error_mean = all_mean_error/415
    all_error = all_error + all_mean_error    
    mean_error = all_error/i
    mean_error_2 = all_error/len(new_data)
    i+=1
   # print("mse is",mean_squared_error(df1['y'].values,forecast['yhat'].values[:len(df1)]))
    print("mae is",all_mean_error,mean_error,mean_error_2)
    print("站点-【%s】，总数据量-【%s】,最大流量-【%s】,最小流量-【%s】,参考流量-【%s】"%(num,len(new_data),df2['value'].max(),df2['value'].min(),temp_mean))
   


# In[ ]:


print(new_data.max())
print(new_data.min())
predict_T3_2 = new_data.copy()


# In[ ]:


print(predict_T3_2.head)


# In[ ]:


predict_T3_2.to_csv('predict_T3_max_03.csv',index=False)

