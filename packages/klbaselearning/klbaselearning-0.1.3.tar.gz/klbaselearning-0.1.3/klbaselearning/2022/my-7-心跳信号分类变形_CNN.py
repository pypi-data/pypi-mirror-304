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
class GaussRankScaler(BaseEstimator, TransformerMixin):
    def __init__(self, epsilon=1e-4, copy=True, n_jobs=None, interp_kind='linear', interp_copy=False):
        self.epsilon     = epsilon
        self.copy        = copy
        self.interp_kind = interp_kind
        self.interp_copy = interp_copy
        self.fill_value  = 'extrapolate'
        self.n_jobs      = n_jobs
 
    def fit(self, X, y=None):
       
        X = check_array(X, copy=self.copy, estimator=self, dtype=FLOAT_DTYPES, force_all_finite=True)
 
        self.interp_func_ = Parallel(n_jobs=self.n_jobs)(delayed(self._fit)(x) for x in X.T)
        return self
 
    def _fit(self, x):
        x = self.drop_duplicates(x)
        rank = np.argsort(np.argsort(x))
        bound = 1.0 - self.epsilon
        factor = np.max(rank) / 2.0 * bound
        scaled_rank = np.clip(rank / factor - bound, -bound, bound)
        return interp1d(
            x, scaled_rank, kind=self.interp_kind, copy=self.interp_copy, fill_value=self.fill_value)
 
    def transform(self, X, copy=None):
       
        check_is_fitted(self, 'interp_func_')
 
        copy = copy if copy is not None else self.copy
        X = check_array(X, copy=copy, estimator=self, dtype=FLOAT_DTYPES, force_all_finite=True)
 
        X = np.array(Parallel(n_jobs=self.n_jobs)(delayed(self._transform)(i, x) for i, x in enumerate(X.T))).T
        return X
 
    def _transform(self, i, x):
        return erfinv(self.interp_func_[i](x))
 
    def inverse_transform(self, X, copy=None):
        
        check_is_fitted(self, 'interp_func_')
 
        copy = copy if copy is not None else self.copy
        X = check_array(X, copy=copy, estimator=self, dtype=FLOAT_DTYPES, force_all_finite=True)
 
        X = np.array(Parallel(n_jobs=self.n_jobs)(delayed(self._inverse_transform)(i, x) for i, x in enumerate(X.T))).T
        return X
 
    def _inverse_transform(self, i, x):
        inv_interp_func = interp1d(self.interp_func_[i].y, self.interp_func_[i].x, kind=self.interp_kind,
                                   copy=self.interp_copy, fill_value=self.fill_value)
        return inv_interp_func(erf(x))
 
    @staticmethod
    def drop_duplicates(x):
        is_unique = np.zeros_like(x, dtype=bool)
        is_unique[np.unique(x, return_index=True)[1]] = True
        return x[is_unique]


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


feature_names = k_x_train.columns.values.tolist() 
scaler_linear    = GaussRankScaler(interp_kind='linear',) 
for c in feature_names:
    k_x_train[c+'_linear_grank'] = scaler_linear.fit_transform(k_x_train[c].values.reshape(-1,1))
    
gaussian_linear_feature_names = [c + '_linear_grank' for c in feature_names]


# In[ ]:


feature_names = X_test.columns.values.tolist() 
scaler_linear    = GaussRankScaler(interp_kind='linear',) 
for c in feature_names:
    X_test[c+'_linear_grank'] = scaler_linear.fit_transform(X_test[c].values.reshape(-1,1))  
gaussian_linear_feature_names = [c + '_linear_grank' for c in feature_names]


# In[ ]:


os.environ['PYTHONHASHSEED'] = '0'
tf.keras.backend.clear_session()


# In[ ]:


#---------------------------------------------------------------
# Defining CALLBACKS
#---------------------------------------------------------------
filepath = "model_save/weights-{epoch:02d}-{val_accuracy:.04f}.hdf5"
checkPoint = ModelCheckpoint(filepath=filepath, monitor='val_accuracy', 
                             verbose=1, save_best_only=True, mode='auto')

#logDir = 'logs'
#tensorBoard_callback = TensorBoard(log_dir=logDir, histogram_freq=1, write_graph=True)

earlyStop = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, 
                          verbose=1, mode='auto', restore_best_weights=True)

reduceLR = ReduceLROnPlateau(monitor='val_loss', factor=0.1, 
                             patience=3, verbose=1, mode='auto')
callBacks = [reduceLR, earlyStop]


# In[ ]:


def noEvModel(input_dim, output_dim):
    model = Sequential()
    model.add(Input(shape=(input_dim,)))
    model.add(Dense(256, activation='tanh', kernel_initializer=tf.keras.initializers.GlorotUniform(seed=44)))
    model.add(PReLU(alpha_initializer="zeros"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(4, activation='softmax', kernel_initializer=tf.keras.initializers.GlorotUniform(seed=46)))
    model.compile(loss='categorical_crossentropy', optimizer='adamax', metrics=['accuracy'])
    return model


# In[ ]:


print(k_x_train.shape)


# In[ ]:


print(k_y_train.shape)


# In[ ]:


noEventModel = noEvModel(k_x_train.shape[1], 4)
noEventModel.summary()


# In[ ]:


def noEventsModel(shuffle):
    """
    Takes a list of Random Seeds, splits the data into Train and CV based on Seed, trains model and takes average of 
    predictions while testing  
    """
    model_list=[]
    loss_list=[]
    avg_cv_loss=0
    for i in range(len(shuffle)):
        print('--Iteration #', i)
        X_tr, X_cr, y_train, y_cv = train_test_split(k_x_train, k_y_train, stratify=k_y_train, test_size=0.15, random_state=shuffle[i])
        
        y_train=np_utils.to_categorical(y_train)
        y_cv=np_utils.to_categorical(y_cv)
        model=noEvModel(X_tr.shape[1], 4)
        model.fit(X_tr, y_train, batch_size=256, epochs=100, verbose=2, shuffle=True, validation_data=(X_cr, y_cv),callbacks=callBacks)
        model.save('saved_models/noEvents/nn '+str(i+1))
        pred=model.predict(X_cr)
        cv_loss=log_loss(y_cv, pred)
        print("Validation Log Loss of  Model in Current Run: ", cv_loss)
        model_list.append(model)
        loss_list.append(cv_loss)
    avg_cv_loss = mean(loss_list)
    print("Average CV Loss of 6 Runs :", avg_cv_loss)
    return(model_list)


# In[ ]:


shuffle = [7, 14, 21, 28, 35, 42]
nnNoEvModel = noEventsModel(shuffle)


# In[ ]:


X_train, X_cv, y_train, y_cv = train_test_split(k_x_train, k_y_train, test_size=0.2, random_state=0, stratify=k_y_train)


# In[ ]:


avg_pred=np.zeros((X_train.shape[0],4))
for i in range(len(nnNoEvModel)):
    train_pred=nnNoEvModel[i].predict(X_train)
    avg_pred+=train_pred
avg_pred/=len(nnNoEvModel)
print("Train Average Log-Loss: ",log_loss(y_train, avg_pred))


# In[ ]:


avg_pred=np.zeros((X_cv.shape[0],4))
for i in range(len(nnNoEvModel)):
    cv_pred = nnNoEvModel[i].predict(X_cv)
    avg_pred += cv_pred
avg_pred/=len(nnNoEvModel)
print("CV Average Log-Loss: ",log_loss(y_cv, avg_pred))


# In[ ]:


prednoEv=np.zeros((X_test.shape[0],4))
for i in range(len(nnNoEvModel)):
    te_pred = nnNoEvModel[i].predict(X_test)
    prednoEv += te_pred
prednoEv/=len(nnNoEvModel)


# In[ ]:


pred = noEventModel.predict(X_train)
llNNnoEVTr=log_loss(y_train, pred)
print("Training Log Loss of NN Model: ",llNNnoEVTr)
pred = noEventModel.predict(X_cv)
llNNnoEVCv=log_loss(y_cv, pred)
print("Validation Log Loss of NN Model: ",llNNnoEVCv)


# In[ ]:


prednoEv = noEventModel.predict(X_test)


# In[ ]:


y_test_pred = np.argmax(prednoEv, axis=1)


# In[ ]:


print(prednoEv)


# In[ ]:


print(y_test_pred)#[3 3 3 ... 3 1 3]

