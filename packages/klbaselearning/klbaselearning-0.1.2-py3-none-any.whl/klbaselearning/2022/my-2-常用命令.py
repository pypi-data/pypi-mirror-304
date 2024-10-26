#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import os
import datetime
import math
import time
import random
import json
import warnings
from xgboost import XGBClassifier
import xgboost as xgb
from lightgbm import LGBMClassifier
import lightgbm as lgb
import pickle
from prettytable import PrettyTable
from imblearn.over_sampling import SMOTE
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPool2D, Activation, Dropout, Flatten, PReLU, BatchNormalization
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.callbacks import Callback, ModelCheckpoint, TensorBoard, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import plot_model
from tensorflow.keras.optimizers import Adagrad, Adam, Adadelta, Adamax
from tensorflow.keras import Sequential, utils, regularizers, Model, Input
from tensorflow.keras.layers import Flatten, Dense, Conv1D, MaxPool1D, Dropout, AvgPool1D
import tensorflow.keras as K
from keras.utils import np_utils
from keras import regularizers
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.decomposition import PCA #主成分分析法
from sklearn.preprocessing import OneHotEncoder, LabelBinarizer, Normalizer, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score,log_loss,roc_auc_score,roc_curve
from sklearn.ensemble import GradientBoostingClassifier
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric
from fbprophet.diagnostics import performance_metrics
from preprocessing import filterData, delData, fillNanList, dropDuplicate,\
    handleOutlier, minMaxScale, cate2Num,standardizeData,\
    discrete, tran_math_function, minMaxScale, standardizeData,\
    onehot_map, map_dict_tran, binary_map, pca_selection,dfs_feature,\
    continue_time, discrete_time, statistics_time
from statsmodels.tsa.stattools import *
from statsmodels.stats.diagnostic import acorr_ljungbox
from statistics import mean


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)


# In[ ]:


A_train = A_train.drop_duplicates(subset=['ds']) #丢弃重复


# In[ ]:


A_train['ds']=A_train['Year'].astype('str').str.cat(A_train['Month'].astype('str'),sep='-')
A_train['ds']=A_train['ds'].astype('str').str.cat(A_train['Day'].astype('str'),sep='-')


# In[ ]:


import datetime
new_train_data_1['ds']=new_train_data_1['ds'].map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d '))


# In[ ]:


#将异常值赋值为NAN
A_train['y']  = A_train['y'].where(A_train['y'] > 0 , np.nan)


# In[ ]:


A_train = A_train.fillna(method = "bfill").fillna(method = "pad")


# In[ ]:


new_train_data_1['add_A'] = np.nan


# In[ ]:


train_data_2['y']=new_train_data['y']
feature_columns = [col for col in train_data_2.columns if col not in ['ds']]
min_max_scaler = preprocessing.MinMaxScaler()
min_max_scaler = min_max_scaler.fit(train_data_2[feature_columns])
train_data_scaler = min_max_scaler.transform(train_data_2[feature_columns])

train_data_scaler=pd.DataFrame(train_data_scaler)
train_data_scaler.rename(columns={0:'y'}, inplace = True)
train_data_scaler['ds']=new_train_data['ds']
train_data_scaler.head


# In[ ]:


forecast3=pd.DataFrame()
forecast3['value']=forecast2['value']
forecast3=min_max_scaler.inverse_transform(forecast3)


# In[ ]:


dataset_1 = features4.values
data_mean_1 = dataset_1[:train_split].mean(axis =0)

data_std_1 = dataset_1[:train_split].std(axis = 0)

dataset_1 = (dataset_1 - data_mean_1)/data_std_1


# In[ ]:


kk2 = pd.DataFrame(kk)*data_std_1 + data_mean_1

