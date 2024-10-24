#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from autogluon.tabular import TabularDataset,TabularPredictor
import os
import pandas as pd
import numpy as np
os.environ["NUMEXPR_MAX_THREADS"] = '20'


# ### 1、导入数据

# In[2]:


# 导入数据  
print("Loading Data ... ")  
df = pd.read_csv('../user_data/train_data_F.csv')#在特征工程代码中生成的中间文件
test_data = pd.read_csv('../user_data/test_data_F.csv')#在特征工程代码中生成的中间文件
best_sub = pd.read_csv('../user_data/best_sub_9704.csv')#注:best_sub_9704.csv为上一次最好提交结果，该CSV也为此模型在原始训练文件中跑出，但模型参数可能略有不同，分数0.9704（7月4日），在这个CSV基础上提取训练样本加入原训练集中，让模型学习更多的隐藏因子。


# ### 2、数据预处理

# In[3]:


test_data3 = test_data.copy()
test_data2 = test_data.copy()
#test_data2 = df.copy()
#test_data2['是否流失'] = best_sub['是否流失']


# In[4]:


#best_sub[best_sub['是否流失']>0.992].count()  #注"0.992"该数值由于上一次迭代的时候没做记录，但误差应该在0.0001-0.001之间


# In[5]:


#best_sub[best_sub['是否流失']<0.0093].count()  #注"0.009"该数值由于上一次迭代的时候没做记录了，但误差应该在0.0001-0.003之间


# In[6]:


#new_test2 = test_data2[(test_data2['是否流失'] > 0.992) | (test_data2['是否流失'] < 0.0093)] #具体数值由于上一次迭代的时候没做记录了，但误差应该在0.0001-0.003之间


# In[7]:


#new_test2.head


# In[8]:


#new_test2['是否流失'][new_test2['是否流失'] > 0.9] =1


# In[9]:


#new_test2['是否流失'][new_test2['是否流失'] < 0.1] =0


# In[10]:


#print(new_test2)


# In[11]:


#newdf = pd.concat([df.assign(is_train = 1),new_test2.assign(is_train = 0)],ignore_index=True) #合并train和test，并且用is_train进行标记


# In[12]:


#newdf=np.concatenate((df,test_data2),axis=0)


# In[13]:


newdf = df.copy()


# In[14]:


#newdf = pd.DataFrame(newdf)


# In[15]:


newdf.head


# In[16]:


#test_data2['是否流失'] = best_sub['是否流失']


# In[17]:


newdf = newdf.drop(['客户ID','is_train','平均丢弃数据呼叫数'], axis=1)#'平均丢弃数据呼叫数',


# In[18]:


'''
newdf['地理区域'] = newdf['地理区域'].astype('category')
newdf['是否双频'] = newdf['是否双频'].astype('category')
newdf['是否翻新机'] = newdf['是否翻新机'].astype('category')
newdf['手机网络功能'] = newdf['手机网络功能'].astype('category')
newdf['婚姻状况'] = newdf['婚姻状况'].astype('category')
newdf['信息库匹配'] = newdf['信息库匹配'].astype('category')
newdf['新手机用户'] = newdf['新手机用户'].astype('category')
newdf['账户消费限额'] = newdf['账户消费限额'].astype('category')
newdf['信用卡指示器'] = newdf['信用卡指示器'].astype('category')
newdf['是否双频'] = newdf['是否双频'].astype('category')
'''


# In[19]:


'''
newdf['过去三个月的平均每月使用分钟数bin'] = newdf['过去三个月的平均每月使用分钟数bin'].astype('category')
newdf['过去三个月的平均每月通话次数bin'] = newdf['过去三个月的平均每月通话次数bin'].astype('category')
newdf['过去三个月的平均月费用bin'] = newdf['过去三个月的平均月费用bin'].astype('category')
newdf['过去六个月的平均每月使用分钟数bin'] = newdf['过去六个月的平均每月使用分钟数bin'].astype('category')
newdf['过去六个月的平均每月通话次数bin'] = newdf['过去六个月的平均每月通话次数bin'].astype('category')
newdf['过去六个月的平均月费用bin'] = newdf['过去六个月的平均月费用bin'].astype('category')
newdf['平均未接语音呼叫数bin'] = newdf['平均未接语音呼叫数bin'].astype('category')
newdf['平均非高峰语音呼叫数bin'] = newdf['平均非高峰语音呼叫数bin'].astype('category')
newdf['使用高峰语音通话的平均不完整分钟数bin'] = newdf['使用高峰语音通话的平均不完整分钟数bin'].astype('category')

'''
'''
newdf['当前设备使用天数bin'] = newdf['当前设备使用天数bin'].astype('category')
newdf['当前手机价格bin'] = newdf['当前手机价格bin'].astype('category')
'''


# In[20]:


#newdf = newdf.drop(['平均峰值数据调用次数','平均掉线或占线呼叫数','平均呼入和呼出高峰语音呼叫数','平均非高峰语音呼叫数','非高峰数据呼叫的平均数量','平均已完成呼叫数','平均呼叫转移呼叫数','平均呼叫等待呼叫数','一分钟内的平均呼入电话数','客户生命周期内平均月费用','过去三个月的平均月费用','平均三通电话数','平均接听语音电话数','使用客户服务电话的平均分钟数','平均超额费用','家庭成人人数','预计收入','在职总月数','家庭中唯一订阅者的数量','家庭活跃用户数','平均月费用','平均语音费用','平均客户服务电话次数','数据超载的平均费用','平均漫游呼叫数','平均掉线语音呼叫数','平均丢弃数据呼叫数','平均占线语音呼叫数','平均占线数据调用次数','平均未接语音呼叫数','未应答数据呼叫的平均次数','尝试数据调用的平均数','平均完成的语音呼叫数','完成数据调用的平均数','过去六个月的平均月费用'], axis=1)
#newdf = newdf.drop(['客户ID','平均峰值数据调用次数','平均掉线或占线呼叫数','平均呼入和呼出高峰语音呼叫数','平均非高峰语音呼叫数','非高峰数据呼叫的平均数量','地理区域','平均已完成呼叫数','平均呼叫转移呼叫数','平均呼叫等待呼叫数','账户消费限额','一分钟内的平均呼入电话数','客户生命周期内平均月费用','过去三个月的平均月费用','平均三通电话数','平均接听语音电话数','使用客户服务电话的平均分钟数','平均超额费用','是否翻新机','手机网络功能','婚姻状况','家庭成人人数','信息库匹配','预计收入','信用卡指示器','在职总月数','家庭中唯一订阅者的数量','家庭活跃用户数','新手机用户','平均月费用','平均语音费用','平均客户服务电话次数','数据超载的平均费用','平均漫游呼叫数','平均掉线语音呼叫数','平均丢弃数据呼叫数','平均占线语音呼叫数','平均占线数据调用次数','平均未接语音呼叫数','未应答数据呼叫的平均次数','尝试数据调用的平均数','是否双频','平均完成的语音呼叫数','完成数据调用的平均数','过去六个月的平均月费用'], axis=1)


# In[21]:


#newdf = newdf.drop(['is_train','尝试拨打的平均语音呼叫次数','平均完成的语音呼叫数','计费调整后的呼叫总数','计费调整后的总分钟数','平均超额费用','尝试数据调用的平均数','计费调整后的总费用','平均非高峰语音呼叫数'], axis=1)


# ### 3、训练数据准备

# In[22]:


newdf.info(verbose=True, null_counts=True)
from sklearn.model_selection import train_test_split
X=newdf
y=newdf['是否流失']
train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.0001,random_state=2022)
print(test_x.shape)
print(train_x.shape)
print(test_y.shape)


# In[23]:


'''
"multiclass": [
    "accuracy",
    "acc",
    "balanced_accuracy",
    "mcc",
    "roc_auc_ovo_macro",
    "log_loss",
    "nll",
    "pac_score",
    "quadratic_kappa",
    "precision_macro",
    "precision_micro",
    "precision_weighted",
    "recall_macro",
    "recall_micro",
    "recall_weighted",
    "f1_macro",
    "f1_micro",
    "f1_weighted"
  ],
'''
'''
"binary": [
    "accuracy",
    "acc",
    "balanced_accuracy",
    "mcc",
    "roc_auc_ovo_macro",
    "log_loss",
    "nll",
    "pac_score",
    "quadratic_kappa",
    "roc_auc",
    "average_precision",
    "precision",
    "precision_macro",
    "precision_micro",
    "precision_weighted",
    "recall",
    "recall_macro",
    "recall_micro",
    "recall_weighted",
    "f1",
    "f1_macro",
    "f1_micro",
    "f1_weighted"
  ],
  '''

#num_bag_folds, num_stack_levels, num_bag_sets, hyperparameter_tune_kwargs, hyperparameters, refit_full.


# ### 4、训练数据

# In[ ]:


#注：训练时间较长，约为11个小时，将生成约31.5GB大小的模型文件夹
predictor = TabularPredictor(label='是否流失', eval_metric='roc_auc').fit(train_data=X,presets='best_quality',verbosity = 3,auto_stack=True,  num_bag_folds=10, num_bag_sets=10, num_stack_levels=3) #ag_args_fit={'num_cpus': 20},hyperparameters = {'NN_TORCH': {'num_epochs': 500}, },#auto_stack=True,  num_bag_folds=5, num_bag_sets=3, num_stack_levels=3 


# In[ ]:


results = predictor.fit_summary()   #8034#"AutogluonModels/ag-20220704_164359/"


# In[ ]:


#predictor.leaderboard(train_x, silent=True)


# ### 5、预测数据

# In[28]:


#读取生成的模型，该模型文件夹名为每次训练模型后自动生成，需自已替换，这里预置的模型即为本次比赛本队获得0.97079分数的模型，大小共31.5G，
predictor=TabularPredictor.load("../user_data/ag-20220707_184911_best97079") 
#results_importance = predictor.feature_importance(X)


# In[ ]:


'''
from sklearn.metrics import confusion_matrix,accuracy_score,recall_score,f1_score,classification_report

test_data_t=test_x.drop(labels=['是否流失'],axis=1)
#模型预测
predictor=TabularPredictor.load("AutogluonModels/ag-20220619_132656/")
#可以设置不同的模型，也可以不写model，默认是最优的模型
pred=predictor.predict(test_data_t)#,model='LightGBM'
#获取准确率、召回率、F1值
cy=confusion_matrix(pred, test_y)
print("confusion_matrix:",cy)
dc=accuracy_score(pred, test_y)
print("accuracy_score",dc)
recall=recall_score(pred, test_y)
print("recall_score",recall)
f1=f1_score(pred, test_y)
print("f1_score",f1)
'''


# In[29]:


test_data = test_data.drop(['客户ID'], axis=1)


# In[ ]:


'''
test_data['地理区域'] = test_data['地理区域'].astype('category')
test_data['是否双频'] = test_data['是否双频'].astype('category')
test_data['是否翻新机'] = test_data['是否翻新机'].astype('category')
test_data['手机网络功能'] = test_data['手机网络功能'].astype('category')
test_data['婚姻状况'] = test_data['婚姻状况'].astype('category')
test_data['信息库匹配'] = test_data['信息库匹配'].astype('category')
test_data['新手机用户'] = test_data['新手机用户'].astype('category')
test_data['账户消费限额'] = test_data['账户消费限额'].astype('category')
test_data['信用卡指示器'] = test_data['信用卡指示器'].astype('category')
test_data['是否双频'] = test_data['是否双频'].astype('category')
'''


# In[4]:


#df3=df.copy()


# In[5]:


#df3 = df3.drop(['客户ID','是否流失'], axis=1)


# In[28]:


#pd.set_option('display.max_rows',None) 


# In[ ]:


#pd.set_option('max_row',300)
#pd.set_option('display.float_format',lambda x:' %.5f' % x)


# In[31]:


#pd.options.display.max_rows = None


# In[ ]:


#predictor.feature_importance(X)
#results_importance2.to_csv('results_importance2.csv',index=False)


# In[32]:


#预测数据
pred_test=predictor.predict_proba(test_data)#,model='LightGBM'


# In[36]:


pred_test.head


# ### 7、结果输出

# In[3]:


test_data3['是否流失'] = pred_test[1]

test_data3[['客户ID','是否流失']].to_csv('../user_data/best_sub_9704.csv', index=False)


# In[ ]:




