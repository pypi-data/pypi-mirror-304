#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from scipy.sparse import csr_matrix, hstack
from collections import Counter
from scipy.stats import entropy
from statistics import mean
import math
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder, LabelBinarizer, Normalizer, LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import xgboost as xgb
from lightgbm import LGBMClassifier
import lightgbm as lgb
from sklearn import preprocessing
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPool2D, Activation, Dropout, Flatten, PReLU, BatchNormalization
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.callbacks import Callback, ModelCheckpoint, TensorBoard, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import plot_model
from tensorflow.keras.optimizers import Adagrad, Adam, Adadelta, Adamax
from keras.utils import np_utils
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss
from prettytable import PrettyTable
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import mean_squared_error,mean_absolute_error
from catboost import CatBoostRegressor
import time


# In[ ]:


def save_sparse_matrix(filename, xmtr):
    np.savez(filename,data = xmtr.data ,indices= xmtr.indices,
             indptr =xmtr.indptr, shape=xmtr.shape )
    
#Loads a sparse matrix
def load_sparse_matrix(filename):
    tmp = np.load(filename)
    return csr_matrix((tmp['data'], tmp['indices'], tmp['indptr']), shape= tmp['shape'])


# In[ ]:


Xev_tr = load_sparse_matrix('sparse/Xev_tr.npz')
Xev_te = load_sparse_matrix('sparse/Xev_te.npz')
gender_age_data_train = pd.read_csv('train_data_all.csv', dtype={'device_id':np.str})
yev = gender_age_data_train['value']-1


# In[ ]:


def train_model(X, X_test, y, params, folds, model_type='lgb', eval_type='regression'):
    oof = np.zeros(X.shape[0])
    predictions = np.zeros(X_test.shape[0])
    scores = []
    for fold_n, (trn_idx, val_idx) in enumerate(folds.split(X, y)):
        print('Fold', fold_n, 'started at', time.ctime()) 
        if model_type == 'lgb':
            trn_data = lgb.Dataset(X[trn_idx], y[trn_idx])
            val_data = lgb.Dataset(X[val_idx], y[val_idx])
           # trn_data = lgb.Dataset(X[trn_idx].iloc[trn_index],label=target.iloc[trn_index])
           # val_data = lgb.Dataset(X[val_idx].iloc[val_index],label=target.iloc[val_index])                     
            clf = lgb.train(params, trn_data, num_boost_round=20000, 
                            valid_sets=[trn_data, val_data], 
                            verbose_eval=100, early_stopping_rounds=300)
            oof[val_idx] = clf.predict(X[val_idx], num_iteration=clf.best_iteration)
            predictions += clf.predict(X_test, num_iteration=clf.best_iteration) / folds.n_splits
        
        if model_type == 'xgb':
            trn_data = xgb.DMatrix(X[trn_idx], y[trn_idx])
            val_data = xgb.DMatrix(X[val_idx], y[val_idx])
            watchlist = [(trn_data, 'train'), (val_data, 'valid_data')]
            clf = xgb.train(dtrain=trn_data, num_boost_round=20000, 
                            evals=watchlist, early_stopping_rounds=200, 
                            verbose_eval=100, params=params)
            oof[val_idx] = clf.predict(xgb.DMatrix(X[val_idx]), ntree_limit=clf.best_ntree_limit)
            predictions += clf.predict(xgb.DMatrix(X_test), ntree_limit=clf.best_ntree_limit) / folds.n_splits
        
        if (model_type == 'cat') and (eval_type == 'regression'):
            clf = CatBoostRegressor(iterations=20000, eval_metric='MAE', **params)
            clf.fit(X[trn_idx], y[trn_idx], 
                    eval_set=(X[val_idx], y[val_idx]),
                    cat_features=[], use_best_model=True, verbose=100)
            oof[val_idx] = clf.predict(X[val_idx])
            predictions += clf.predict(X_test) / folds.n_splits
            
        if (model_type == 'cat') and (eval_type == 'binary'):
            clf = CatBoostClassifier(iterations=20000, eval_metric='Logloss', **params)
            clf.fit(X[trn_idx], y[trn_idx], 
                    eval_set=(X[val_idx], y[val_idx]),
                    cat_features=[], use_best_model=True, verbose=100)
            oof[val_idx] = clf.predict_proba(X[val_idx])[:,1]
            predictions += clf.predict_proba(X_test)[:,1] / folds.n_splits
        print(predictions)
        if eval_type == 'regression':
            scores.append(mean_squared_error(oof[val_idx], y[val_idx])**0.5)
        if eval_type == 'binary':
            scores.append(log_loss(y[val_idx], oof[val_idx]))
        
    print('CV mean score: {0:.4f}, std: {1:.4f}.'.format(np.mean(scores), np.std(scores)))
    
    return oof, predictions, scores


# In[ ]:


#### lgb
lgb_params = {
             'num_leaves': 18,    #63,20,18
             'min_data_in_leaf': 18,   #32,20
             'objective':'regression_l1',
             'max_depth':3,#4
             'learning_rate': 0.01,
             "min_child_samples": 20,
             "boosting": "gbdt",
             "feature_fraction": 0.95,
             "bagging_freq": 1,
             "bagging_fraction": 0.95,
             "bagging_seed": 11,
             "metric": 'mae',
             'lambda_l1': 1,  #1
             'lambda_l2': 0.5,  
             "verbosity": -1,
             'seed':2021}
folds = KFold(n_splits=5, shuffle=True, random_state=2021)
#X_ntrain = ntrain[fea_cols].values
# 生成数据和标签
print('='*10,'回归模型','='*10)
oof_lgb , predictions_lgb , scores_lgb  = train_model(Xev_tr , Xev_te, yev, params=lgb_params, folds=folds, model_type='lgb', eval_type='regression')


# In[ ]:


sub_df=pd.DataFrame()
sub_df["target"] = predictions_lgb
sub_df.to_csv('predictions_lgb.csv', index=False)


# In[ ]:


oof_lgb  = pd.DataFrame(oof_lgb)


predictions_lgb  = pd.DataFrame(predictions_lgb)

oof_lgb.to_csv('oof_lgb.csv',header=None,index=False)


predictions_lgb.to_csv('predictions_lgb.csv',header=None,index=False)
predictions_lgb.to_csv('predictions_lgb_2.csv',index=False)


# In[ ]:


predictions_lgb_R = (predictions_lgb+0.5).round(0)
predictions_lgb_R.to_csv('predictions_lgb_R.csv',index=False)


# In[ ]:


#### cat
cat_params = {'learning_rate': 0.03, 'depth': 9, 'l2_leaf_reg': 10, 'bootstrap_type': 'Bernoulli',
              'od_type': 'Iter', 'od_wait': 50, 'random_seed': 2021, 'allow_writing_files': False,'loss_function': 'MAE'}
folds = KFold(n_splits=10, shuffle=True, random_state=2021)
print('='*10,'回归模型','='*10)
oof_cat , predictions_cat , scores_cat  = train_model(Xev_tr , Xev_te, yev , params=cat_params, folds=folds, model_type='cat', eval_type='regression')


# In[ ]:


sub_df = pd.DataFrame()
sub_df["target"] = predictions_cat
sub_df.to_csv('predictions_cat.csv', index=False)
oof_cat  = pd.DataFrame(oof_cat)
predictions_cat  = pd.DataFrame(predictions_cat)
oof_cat.to_csv('oof_cat.csv',header=None,index=False)
predictions_cat.to_csv('predictions_cat.csv',header=None,index=False)
predictions_cat.to_csv('predictions_cat_f.csv',index=False)


# In[ ]:


predictions_cat_R = predictions_cat.round(0)
predictions_cat_R.to_csv('predictions_cat_R.csv',index=False)


# ### 加权融合

# In[ ]:


sub_df = pd.DataFrame()
#sub_df  = (predictions_lgb + predictions_xgb + predictions_cat) / 3
sub_df  = (predictions_lgb + predictions_cat) / 2
sub_df.to_csv('predictions_wei_average.csv', index=False)


# In[ ]:


sub_df2 = sub_df.round(0)

sub_df2.to_csv('predictions_wei_average_r.csv', index=False)


# ### Stacking融合

# In[ ]:


from sklearn.linear_model import Ridge, RidgeCV
from sklearn.linear_model import BayesianRidge
#### stack 回归模型  without-outliers回归模型 分类模型
def stack_model(oof_1, oof_2,  predictions_1, predictions_2, y, eval_type='regression'):
   
    train_stack = np.vstack([oof_1, oof_2]).transpose()
    test_stack = np.vstack([predictions_1, predictions_2]).transpose()
    from sklearn.model_selection import RepeatedKFold
    folds = RepeatedKFold(n_splits=5, n_repeats=2, random_state=2020)
    oof = np.zeros(train_stack.shape[0])
    predictions = np.zeros(test_stack.shape[0])

    for fold_, (trn_idx, val_idx) in enumerate(folds.split(train_stack, y)):
        print("fold n°{}".format(fold_+1))
        trn_data, trn_y = train_stack[trn_idx], y[trn_idx]
        val_data, val_y = train_stack[val_idx], y[val_idx]
        print("-" * 10 + "Stacking " + str(fold_) + "-" * 10)
        clf = BayesianRidge()
        clf.fit(trn_data, trn_y)

        oof[val_idx] = clf.predict(val_data)
        predictions += clf.predict(test_stack) / (5 * 2)
    if eval_type == 'regression':
        print('mean: ',np.sqrt(mean_squared_error(y, oof)))
    if eval_type == 'binary':
        print('mean: ',log_loss(y, oof))
    
    return oof, predictions
print('='*30)
oof_stack , predictions_stack  = stack_model(oof_lgb[0] , oof_cat[0] , predictions_lgb[0] , predictions_cat[0] , yev)


# In[ ]:


sub_df = pd.DataFrame()
sub_df["target"] = predictions_stack
sub_df.to_csv('predictions_stack.csv', index=False)

sub_df2 = sub_df.round(0)

sub_df2.to_csv('predictions_stack_r.csv', index=False)

