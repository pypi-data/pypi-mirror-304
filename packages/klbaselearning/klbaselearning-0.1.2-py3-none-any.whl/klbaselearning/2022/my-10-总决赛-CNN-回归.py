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


# In[ ]:


os.environ['PYTHONHASHSEED'] = '0'
tf.keras.backend.clear_session()
from sklearn.metrics import mean_absolute_error,mean_squared_error
from tensorflow.python.keras.callbacks import LearningRateScheduler


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
Xev_tr = Xev_tr.toarray()
Xev_te = Xev_te.toarray()
pre_lgb = pd.read_csv('predictions_lgb_2.csv')

gender_age_data_train = pd.read_csv('train_data_all.csv', dtype={'device_id':np.str})
yev = gender_age_data_train['value']


# In[ ]:


print(Xev_tr.shape)


# In[ ]:


#print(Xev_tr.shape[1])


# In[ ]:


yev.shape


# In[ ]:


earlyStop = EarlyStopping(monitor='mae', min_delta=0, patience=15, 
                          verbose=1, mode='auto', restore_best_weights=True)

reduceLR = ReduceLROnPlateau(monitor='mae', factor=0.1, 
                             patience=15, verbose=1, mode='auto')
callBacks = [reduceLR, earlyStop]


# In[ ]:


#,kernel_regularizer=regularizers.l2(0.001), activity_regularizer=regularizers.l1(0.001),
# REF - https://www.kaggle.com/c/talkingdata-mobile-user-demographics/discussion/23424
def evModel(input_dim, output_dim):
    model = Sequential()
    model.add(Input(shape=(input_dim,)))     
    model.add(Dense(10, activation='relu',kernel_initializer=tf.keras.initializers.GlorotNormal(seed=33)))
   # model.add(PReLU(alpha_initializer="zeros"))
    model.add(Dropout(0.2))
    model.add(Dense(5, activation='relu',kernel_initializer=tf.keras.initializers.GlorotNormal(seed=34)))
  #  model.add(PReLU(alpha_initializer="zeros"))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='relu',kernel_initializer=tf.keras.initializers.GlorotNormal(seed=36)))
    model.compile(loss='mean_absolute_error', optimizer='Adam',metrics=['mae']) #tf.keras.optimizers.Adam()  
    return model


# In[ ]:


def eventsModel(shuffle):
    """
    Takes a list of Random Seeds, splits the data into Train and CV based on Seed, trains model and takes average of 
    predictions while testing  
    """
    model_list=[]
    loss_list=[]
    avg_cv_loss=0
    for i in range(len(shuffle)):
        print('--Iteration #', i)
        X_tr, X_cr, y_train, y_cv = train_test_split(Xev_tr, yev, test_size=0.1, random_state=shuffle[i])
        print(X_tr.shape)
        print(X_cr.shape)
        model=evModel(X_tr.shape[1], 1)
        model.fit(X_tr, y_train, batch_size=32, epochs=800, verbose=1, shuffle=True, validation_data=(X_cr, y_cv),callbacks=callBacks)
        model.save('saved_models/noEvents/nn '+str(i+1))
        pred=model.predict(X_cr)
        print(pred.shape)
        print(y_cv.shape)
        cv_loss=mean_squared_error(y_cv, pred)
        print("Validation Log Loss of  Model in Current Run: ", cv_loss)
        model_list.append(model)
        loss_list.append(cv_loss)
        avg_cv_loss = mean(loss_list)
        print("Average CV Loss of 6 Runs :", avg_cv_loss)
    return(model_list)


# In[ ]:


shuffle = [7, 14, 21,  42] #28,35
nnEvModel = eventsModel(shuffle)


# In[ ]:


avg_pred=np.zeros((Xev_tr.shape[0],1))
for i in range(len(nnEvModel)):
    train_pred=nnEvModel[i].predict(Xev_tr)
    avg_pred+=train_pred
avg_pred /= len(nnEvModel)
print("Train Average Log-Loss: ",mean_squared_error(yev, avg_pred))


# In[ ]:


predEv=np.zeros((Xev_te.shape[0],1))
for i in range(len(nnEvModel)):
    te_pred = nnEvModel[i].predict(Xev_te)
    predEv += te_pred
predEv/=(len(nnEvModel))


# In[ ]:


print(predEv)


# In[ ]:


predEv2= pd.DataFrame(predEv)

predEv2.to_csv('predictions_cnn.csv',index=False)


# In[ ]:


sub_df_cnn = pd.DataFrame()
sub_df_cnn  = ((pre_lgb.values + predEv2.values) / 2).round(0)
print(sub_df_cnn)
kk = pd.DataFrame(sub_df_cnn)
kk.to_csv('CNN_wei_average.csv', index=False)

