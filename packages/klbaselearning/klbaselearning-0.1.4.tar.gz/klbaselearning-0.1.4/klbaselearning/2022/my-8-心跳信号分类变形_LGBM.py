#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
import pickle
from scipy.sparse import csr_matrix, hstack
from collections import Counter
from scipy.stats import entropy
from statistics import mean
from keras import regularizers
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder, LabelBinarizer, Normalizer, LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import xgboost as xgb
from lightgbm import LGBMClassifier
import lightgbm as lgb
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

train = pd.read_csv('datasets/@huangzx23#ba5d051838cf583c27a68007e887d01c/train.csv')
test = pd.read_csv('datasets/@huangzx23#ba5d051838cf583c27a68007e887d01c/test.csv')
y_train = train['label']
x_train = train.drop(['label'], axis=1)
X_test = test
print(x_train.shape, y_train.shape)
print(X_test.shape)


# In[ ]:


import numpy as np
from joblib import Parallel, delayed
from scipy.interpolate import interp1d
from scipy.special import erf, erfinv
from sklearn.preprocessing import QuantileTransformer,PowerTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import FLOAT_DTYPES, check_array, check_is_fitted


# In[ ]:


#查看类别分布
train2 = pd.read_csv('submit_B.csv')

plt.hist(train['label'], orientation = 'vertical', histtype = 'bar', color = 'red')
plt.show() 

plt.hist(train2['label'], orientation = 'vertical', histtype = 'bar', color = 'red')
plt.show() 


# In[ ]:


# 使用 SMOTE 对数据进行上采样以解决类别不平衡问题
smote = SMOTE(random_state=2021, n_jobs=-1)
k_x_train, k_y_train = smote.fit_resample(x_train, y_train)  
print(f"after smote, k_x_train.shape: {k_x_train.shape}, k_y_train.shape: {k_y_train.shape}")
# 将训练集转换为适应 CNN 输入的 shape
#k_x_train = np.array(k_x_train).reshape(k_x_train.shape[0], k_x_train.shape[1], 1)
k_x_train = k_x_train
k_y_train = k_y_train


# In[ ]:


print(k_x_train)


# In[ ]:


plt.hist(k_y_train, orientation = 'vertical', histtype = 'bar', color = 'blue')
plt.show() 


# In[ ]:


k_x_train = k_x_train.values
X_test = X_test.values


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
        if eval_type == 'multiclass':
            scores.append(log_loss(y[val_idx], oof[val_idx]))
        
    print('CV mean score: {0:.4f}, std: {1:.4f}.'.format(np.mean(scores), np.std(scores)))
  
    return oof, predictions, scores


# In[ ]:


#### lgb
lgb_params = {
             'num_leaves': 18,    #63,20,18
             'min_data_in_leaf': 18,   #32,20
             'objective':'multiclass',
             'num_class': 4,
             'max_depth':3,#4
             'learning_rate': 0.01,
             "min_child_samples": 20,
             "boosting": "gbdt",
             "feature_fraction": 0.95,
             "bagging_freq": 1,
             "bagging_fraction": 0.95,
             "bagging_seed": 11,
            # "metric": 'mae',
             'lambda_l1': 1,  #1
             'lambda_l2': 0.5,  
             "verbosity": -1,
             'seed':2021}
folds = KFold(n_splits=5, shuffle=True, random_state=2021)
#X_ntrain = ntrain[fea_cols].values
# 生成数据和标签
print('='*10,'回归模型','='*10)
oof_lgb , predictions_lgb , scores_lgb  = train_model(k_x_train , X_test, k_y_train, params=lgb_params, folds=folds, model_type='lgb', eval_type='multiclass')


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

