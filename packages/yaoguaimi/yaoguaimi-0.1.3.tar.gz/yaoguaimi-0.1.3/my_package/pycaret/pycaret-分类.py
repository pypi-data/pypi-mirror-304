#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pycaret.datasets import get_data
# 从本地加载数据，注意dataset是数据的文件名
data = get_data(dataset='./datasets/diabetes', verbose=False)
# 从pycaret开源仓库下载公开数据
# data = get_data('diabetes', verbose=False)


# In[ ]:


# 查看数据类型和数据维度
type(data), data.shape


# In[ ]:


(pandas.core.frame.DataFrame, (768, 9))


# In[ ]:


# 最后一列表示是否为糖尿病患者，其他列为特征列
data.head()


# In[ ]:


#利用PyCaret核心函数setup，初始化建模环境并准备数据以供模型训练和评估使用：
from pycaret.classification import ClassificationExperiment
s = ClassificationExperiment()
# target目标列，session_id设置随机数种子, preprocesss是否清洗数据，train_size训练集比例, normalize是否归一化数据, normalize_method归一化方式
s.setup(data, target = 'Class variable', session_id = 0, verbose= False, train_size = 0.7, normalize = True, normalize_method = 'minmax')


# In[ ]:


s.get_config()#查看基于setup函数创建的变量：


# In[ ]:


#查看归一化的数据：
s.get_config('X_train_transformed')


# In[ ]:


#绘制某列数据的柱状图：

s.get_config('X_train_transformed')['Number of times pregnant'].hist()


# In[ ]:


#当然也可以利用如下代码创建任务示例来初始化环境：
from pycaret.classification import setup
# s = setup(data, target = 'Class variable', session_id = 0, preprocess = True, train_size = 0.7, verbose = False)


# In[ ]:


#模型训练与评估PyCaret提供了compare_models函数，通过使用默认的10折交叉验证来训练和评估模型库中所有可用估计器的性能：
best = s.compare_models()
# 选择某些模型进行比较
# best = s.compare_models(include = ['dt', 'rf', 'et', 'gbc', 'lightgbm'])
# 按照召回率返回n_select性能最佳的模型
# best_recall_models_top3 = s.compare_models(sort = 'Recall', n_select = 3)


# In[ ]:


#返回当前设置中所有经过训练的模型中的最佳模型:

best_ml = s.automl()
# best_ml


# In[ ]:


# 打印效果最佳的模型
print(best)


# In[ ]:


# 提取所有模型预测结果
models_results = s.pull()
models_results


# In[ ]:


s.plot_model(best, plot = 'confusion_matrix')


# In[ ]:


#如果在jupyter环境，可以通过evaluate_model函数来交互式展示模型的性能：
s.evaluate_model(best)


# In[ ]:


#模型预测
# 预测整个数据集
res = s.predict_model(best, data=data)
# 查看各行预测结果
# res


# In[ ]:


# 预测用于数据训练的测试集
res = s.predict_model(best)


# In[ ]:


# 保存模型到本地
_ = s.save_model(best, 'best_model', verbose = False)
# 导入模型
model = s.load_model( 'best_model')
# 查看模型结构
# model


# In[ ]:


# 预测整个数据集
res = s.predict_model(model, data=data)

