#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from autogluon.tabular import TabularDataset, TabularPredictor

import numpy as np

train_data = TabularDataset('https://autogluon.s3.amazonaws.com/datasets/Inc/train.csv')
subsample_size = 1000  # subsample subset of data for faster demo, try setting this to much larger values
train_data = train_data.sample(n=subsample_size, random_state=0)
print(train_data.head())

label = 'occupation'
print("Summary of occupation column: \n", train_data['occupation'].describe())

test_data = TabularDataset('https://autogluon.s3.amazonaws.com/datasets/Inc/test.csv')
y_test = test_data[label]
test_data_nolabel = test_data.drop(columns=[label])  # delete label column

metric = 'accuracy' # we specify eval-metric just for demo (unnecessary as it's the default)


# In[ ]:


from autogluon.common import space

nn_options = {  # specifies non-default hyperparameter values for neural network models
    'num_epochs': 10,  # number of training epochs (controls training time of NN models)
    'learning_rate': space.Real(1e-4, 1e-2, default=5e-4, log=True),  # learning rate used in training (real-valued hyperparameter searched on log-scale)
    'activation': space.Categorical('relu', 'softrelu', 'tanh'),  # activation function used in NN (categorical hyperparameter, default = first entry)
    'dropout_prob': space.Real(0.0, 0.5, default=0.1),  # dropout probability (real-valued hyperparameter)
}

gbm_options = {  # specifies non-default hyperparameter values for lightGBM gradient boosted trees
    'num_boost_round': 100,  # number of boosting rounds (controls training time of GBM models)
    'num_leaves': space.Int(lower=26, upper=66, default=36),  # number of leaves in trees (integer hyperparameter)
}

hyperparameters = {  # hyperparameters of each model type
                   'GBM': gbm_options,
                   'NN_TORCH': nn_options,  # NOTE: comment this line out if you get errors on Mac OSX
                  }  # When these keys are missing from hyperparameters dict, no models of that type are trained

time_limit = 2*60  # train various models for ~2 min
num_trials = 5  # try at most 5 different hyperparameter configurations for each type of model
search_strategy = 'auto'  # to tune hyperparameters using random search routine with a local scheduler

hyperparameter_tune_kwargs = {  # HPO is not performed unless hyperparameter_tune_kwargs is specified
    'num_trials': num_trials,
    'scheduler' : 'local',
    'searcher': search_strategy,
}  # Refer to TabularPredictor.fit docstring for all valid values

predictor = TabularPredictor(label=label, eval_metric=metric).fit(
    train_data,
    time_limit=time_limit,
    hyperparameters=hyperparameters,
    hyperparameter_tune_kwargs=hyperparameter_tune_kwargs,
)


# In[ ]:


y_pred = predictor.predict(test_data_nolabel)
print("Predictions:  ", list(y_pred)[:5])
perf = predictor.evaluate(test_data, auxiliary_metrics=False)


# In[ ]:


results = predictor.fit_summary()


# In[ ]:





# In[ ]:


#使用 stacking/bagging 进行模型集成
label = 'class'  # Now lets predict the "class" column (binary classification)
test_data_nolabel = test_data.drop(columns=[label])
y_test = test_data[label]
save_path = 'agModels-predictClass'  # folder where to store trained models

predictor = TabularPredictor(label=label, eval_metric=metric).fit(train_data,
    num_bag_folds=5, num_bag_sets=1, num_stack_levels=1,
    hyperparameters = {'NN_TORCH': {'num_epochs': 2}, 'GBM': {'num_boost_round': 20}},  # last  argument is just for quick demo here, omit it in real applications
)


# In[ ]:


# Lets also specify the "f1" metric
predictor = TabularPredictor(label=label, eval_metric='f1', path=save_path).fit(
    train_data, auto_stack=True,
    time_limit=30, hyperparameters={'FASTAI': {'num_epochs': 10}, 'GBM': {'num_boost_round': 200}}  # last 2 arguments are for quick demo, omit them in real applications
)
predictor.leaderboard(test_data)


# In[ ]:


#决策阈值校准
'''
通过将预测决策阈值调整为默认值 0.5 以外的值，可以在二元分类中实现指标得分的大幅提升，例如和"f1"。"balanced_accuracy"calibrate_decision_threshold

"f1"以下是校准和未校准决策阈值的情况下在测试数据上取得的分数的示例：'''
print(f'Prior to calibration (predictor.decision_threshold={predictor.decision_threshold}):')
scores = predictor.evaluate(test_data)

calibrated_decision_threshold = predictor.calibrate_decision_threshold()
predictor.set_decision_threshold(calibrated_decision_threshold)

print(f'After calibration (predictor.decision_threshold={predictor.decision_threshold}):')
scores_calibrated = predictor.evaluate(test_data)


# In[ ]:


#默认情况下，predict()将predict_proba()使用 AutoGluon 认为最准确的模型，该模型通常是许多单个模型的集合。以下是如何查看这是哪个模型：
predictor.model_best


# In[ ]:


#在决定使用哪个模型之前，让我们评估 AutoGluon 之前在我们的测试数据上训练的所有模型：
predictor.leaderboard(test_data)
predictor.leaderboard(extra_info=True)
predictor.leaderboard(test_data, extra_metrics=['accuracy', 'balanced_accuracy', 'log_loss'])
i = 0  # index of model to use
model_to_use = predictor.model_names()[i]
model_pred = predictor.predict(datapoint, model=model_to_use)
print("Prediction from %s model: %s" % (model_to_use, model_pred.iloc[0]))


# In[ ]:


#我们可以轻松访问有关训练预测器或特定模型的各种信息：
all_models = predictor.model_names()
model_to_use = all_models[i]
specific_model = predictor._trainer.load_model(model_to_use)

# Objects defined below are dicts of various information (not printed here as they are quite large):
model_info = specific_model.get_info()
predictor_information = predictor.info()


# In[ ]:


y_pred_proba = predictor.predict_proba(test_data_nolabel)
perf = predictor.evaluate_predictions(y_true=y_test, y_pred=y_pred_proba)
perf = predictor.evaluate(test_data)
predictor.feature_importance(test_data)


# In[ ]:


'''
推理速度作为拟合约束
如果您在拟合预测器之前知道延迟约束，则可以将其明确指定为拟合参数。AutoGluon 随后将以尝试满足约束的方式自动训练模型。

此约束包含两个部分：infer_limit和infer_limit_batch_size：

infer_limit是预测 1 行数据所需的时间（以秒为单位）。例如，infer_limit=0.05表示每行数据 50 毫秒，或每秒 20 行的吞吐量。

infer_limit_batch_size是计算每行速度时一次传递的要预测的行数。这非常重要，因为infer_limit_batch_size=1（在线推理）非常不理想，因为各种操作无论数据大小都有固定的成本开销。如果您可以批量传递测试数据，则应指定infer_limit_batch_size=10000。
'''


# In[ ]:


# At most 0.05 ms per row (20000 rows per second throughput)
infer_limit = 0.00005
# adhere to infer_limit with batches of size 10000 (batch-inference, easier to satisfy infer_limit)
infer_limit_batch_size = 10000
# adhere to infer_limit with batches of size 1 (online-inference, much harder to satisfy infer_limit)
# infer_limit_batch_size = 1  # Note that infer_limit<0.02 when infer_limit_batch_size=1 can be difficult to satisfy.
predictor_infer_limit = TabularPredictor(label=label, eval_metric=metric).fit(
    train_data=train_data,
    time_limit=30,
    infer_limit=infer_limit,
    infer_limit_batch_size=infer_limit_batch_size,
)

# NOTE: If bagging was enabled, it is important to call refit_full at this stage.
#  infer_limit assumes that the user will call refit_full after fit.
# predictor_infer_limit.refit_full()

# NOTE: To align with inference speed calculated during fit, models must be persisted.
predictor_infer_limit.persist()
# Below is an optimized version that only persists the minimum required models for prediction.
# predictor_infer_limit.persist('best')

predictor_infer_limit.leaderboard()


# In[ ]:


test_data_batch = test_data.sample(infer_limit_batch_size, replace=True, ignore_index=True)

import time
time_start = time.time()
predictor_infer_limit.predict(test_data_batch)
time_end = time.time()

infer_time_per_row = (time_end - time_start) / len(test_data_batch)
rows_per_second = 1 / infer_time_per_row
infer_time_per_row_ratio = infer_time_per_row / infer_limit
is_constraint_satisfied = infer_time_per_row_ratio <= 1

print(f'Model is able to predict {round(rows_per_second, 1)} rows per second. (User-specified Throughput = {1 / infer_limit})')
print(f'Model uses {round(infer_time_per_row_ratio * 100, 1)}% of infer_limit time per row.')
print(f'Model satisfies inference constraint: {is_constraint_satisfied}')


# In[ ]:


'''
更快的预设或超参数
fit()如果您知道推理延迟或内存一开始会成为问题，那么您可以相应地调整训练过程以确保不会产生笨重的模型，而不是试图在预测时加速繁琐的训练模型。

一种选择是指定更轻量级的presets：
'''


# In[ ]:


presets = ['good_quality', 'optimize_for_deployment']
predictor_light = TabularPredictor(label=label, eval_metric=metric).fit(train_data, presets=presets, time_limit=30)


# In[ ]:


#另一种选择是指定更轻量的超参数：
predictor_light = TabularPredictor(label=label, eval_metric=metric).fit(train_data, hyperparameters='very_light', time_limit=30)


# In[ ]:


#最后，你也可以完全排除某些难以操作的模型进行训练。下面我们排除那些速度较慢的模型（K 近邻、神经网络）：
excluded_model_types = ['KNN', 'NN_TORCH']
predictor_light = TabularPredictor(label=label, eval_metric=metric).fit(train_data, excluded_model_types=excluded_model_types, time_limit=30)


# In[ ]:


'''
{
	'NN_TORCH': [{}],
	'GBM': [{'extra_trees': True, 'ag_args': {'name_suffix': 'XT'}}, {}, {'learning_rate': 0.03, 'num_leaves': 128, 'feature_fraction': 0.9, 'min_data_in_leaf': 3, 'ag_args': {'name_suffix': 'Large', 'priority': 0, 'hyperparameter_tune_kwargs': None}}],
	'CAT': [{}],
	'XGB': [{}],
	'FASTAI': [{}],
	'RF': [{'criterion': 'gini', 'ag_args': {'name_suffix': 'Gini', 'problem_types': ['binary', 'multiclass']}}, {'criterion': 'entropy', 'ag_args': {'name_suffix': 'Entr', 'problem_types': ['binary', 'multiclass']}}, {'criterion': 'squared_error', 'ag_args': {'name_suffix': 'MSE', 'problem_types': ['regression', 'quantile']}}],
	'XT': [{'criterion': 'gini', 'ag_args': {'name_suffix': 'Gini', 'problem_types': ['binary', 'multiclass']}}, {'criterion': 'entropy', 'ag_args': {'name_suffix': 'Entr', 'problem_types': ['binary', 'multiclass']}}, {'criterion': 'squared_error', 'ag_args': {'name_suffix': 'MSE', 'problem_types': ['regression', 'quantile']}}],
	'KNN': [{'weights': 'uniform', 'ag_args': {'name_suffix': 'Unif'}}, {'weights': 'distance', 'ag_args': {'name_suffix': 'Dist'}}],
}
'''


# In[ ]:


'''
如果遇到内存
为了减少训练期间的内存使用量，您可以单独尝试以下每种策略或将它们组合起来（但这可能会损害准确性）：

在 中fit()，集合（或这些模型的某些子集）。excluded_model_types = ['KNN', 'XT' ,'RF']

尝试不同presets的fit()。

在fit()，设置或。hyperparameters = 'light'hyperparameters = 'very_light'

表中的文本字段需要大量内存来进行 N-gram 特征化。为了缓解这种情况fit()，您可以：(1) 添加'ignore_text'到presets列表中（忽略文本特征），或 (2) 指定参数：

'''
from sklearn.feature_extraction.text import CountVectorizer
from autogluon.features.generators import AutoMLPipelineFeatureGenerator
feature_generator = AutoMLPipelineFeatureGenerator(vectorizer=CountVectorizer(min_df=30, ngram_range=(1, 3), max_features=MAX_NGRAM, dtype=np.uint8))
#例如使用（尝试 10000 以下的各种值来减少用于表示每个文本字段的 N-gram 特征的数量）MAX_NGRAM = 1000


# In[ ]:


'''
如果遇到磁盘空间
为了减少磁盘使用量，您可以单独尝试以下每种策略或尝试它们的组合：

确保删除predictor.path之前运行的所有文件夹！如果多次fit()调用，这些文件夹可能会占用您的可用空间。如果您未指定，AutoGluon 仍会自动将其模型保存到名为“AutogluonModels/ag-[TIMESTAMP]”的文件夹中，其中 TIMESTAMP 记录了调用时间，因此如果可用空间不足，请确保也删除这些文件夹。fit()pathfit()

调用predictor.save_space()以删除期间生成的辅助文件fit()。

如果您只打算使用此预测器进行推理，请调用（将删除非预测相关功能所需的文件，如）。predictor.delete_models(models_to_keep='best', dry_run=False)fit_summary

在 中fit()，你可以添加'optimize_for_deployment'到presets列表中，训练完成后将自动调用前两种策略。

上述减少内存使用量的策略大多数也会减少磁盘使用量（但可能会损害准确性）。

'''

