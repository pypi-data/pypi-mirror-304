#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.decomposition import PCA #主成分分析法
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.ensemble import GradientBoostingClassifier
#from yellowbrick.features import FeatureImportances
from sklearn.linear_model import LogisticRegression
#from yellowbrick.features import ParallelCoordinates
from sklearn.model_selection import train_test_split
#from yellowbrick.features import parallel_coordinates,PCADecomposition
#from yellowbrick.classifier import classification_report
from sklearn.linear_model import Ridge
#from yellowbrick.regressor import PredictionError
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
from sklearn.metrics import roc_auc_score
import json
import warnings
from sklearn import preprocessing
import lightgbm as lgb  
import pickle  
from sklearn.model_selection import train_test_split  
from preprocessing import filterData, delData, fillNanList, dropDuplicate,\
    handleOutlier, minMaxScale, cate2Num,standardizeData,\
    discrete, tran_math_function, minMaxScale, standardizeData,\
    onehot_map, map_dict_tran, binary_map, pca_selection,dfs_feature,\
    continue_time, discrete_time, statistics_time

from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from catboost import CatBoostRegressor
pd.set_option('display.max_columns',None)
warnings.filterwarnings("ignore")


# In[ ]:


# 导入数据  
print("Loading Data ... ")  
train_data = pd.read_csv('X_train_transformed_915.csv')
test_data = pd.read_csv('X_test_transformed_915.csv')


# In[ ]:


'''
train_data['dinner_type'] = train_data['dinner_type'].astype('category')
train_data['terminal_5g_type'] = train_data['terminal_5g_type'].astype('category')
train_data['model_id'] = train_data['model_id'].astype('category')
train_data['support_band'] = train_data['support_band'].astype('category')
train_data['ue_tac_id'] = train_data['ue_tac_id'].astype('category')
train_data['agegroup'] = train_data['agegroup'].astype('category')
train_data['datagroup'] = train_data['datagroup'].astype('category')
train_data['billgroup'] = train_data['billgroup'].astype('category')
train_data['volte_duragroup'] = train_data['volte_duragroup'].astype('category')
train_data['flowgroup'] = train_data['flowgroup'].astype('category')
train_data['call_out_timesgroup'] = train_data['call_out_timesgroup'].astype('category')
train_data['call_out_duragroup'] = train_data['call_out_duragroup'].astype('category')
train_data['call_in_timesgroup'] = train_data['call_in_timesgroup'].astype('category')
train_data['listed_pricegroup'] = train_data['listed_pricegroup'].astype('category')
train_data['user_lv'] = train_data['user_lv'].astype('category')
train_data['sex'] = train_data['sex'].astype('category')
train_data['user_status'] = train_data['user_status'].astype('category')
train_data['fuse_type'] = train_data['fuse_type'].astype('category')
train_data['service_type'] = train_data['service_type'].astype('category')
train_data['complaint_status'] = train_data['complaint_status'].astype('category')



test_data['dinner_type'] = test_data['dinner_type'].astype('category')
test_data['terminal_5g_type'] = test_data['terminal_5g_type'].astype('category')
test_data['model_id'] = test_data['model_id'].astype('category')
test_data['support_band'] = test_data['support_band'].astype('category')
test_data['ue_tac_id'] = test_data['ue_tac_id'].astype('category')
test_data['agegroup'] = test_data['agegroup'].astype('category')
test_data['datagroup'] = test_data['datagroup'].astype('category')
test_data['billgroup'] = test_data['billgroup'].astype('category')
test_data['volte_duragroup'] = test_data['volte_duragroup'].astype('category')
test_data['flowgroup'] = test_data['flowgroup'].astype('category')
test_data['call_out_timesgroup'] = test_data['call_out_timesgroup'].astype('category')
test_data['call_out_duragroup'] = test_data['call_out_duragroup'].astype('category')
test_data['call_in_timesgroup'] = test_data['call_in_timesgroup'].astype('category')
test_data['listed_pricegroup'] = test_data['listed_pricegroup'].astype('category')
test_data['user_lv'] = test_data['user_lv'].astype('category')
test_data['sex'] = test_data['sex'].astype('category')
test_data['user_status'] = test_data['user_status'].astype('category')
test_data['fuse_type'] = test_data['fuse_type'].astype('category')
test_data['service_type'] = test_data['service_type'].astype('category')
test_data['complaint_status'] = test_data['complaint_status'].astype('category')
'''


# In[ ]:


#train_data = train_data.iloc[0:79755]


# In[ ]:


#train_data.to_csv('train_data_20.csv',index=False)
#test_data.to_csv('test_data_20.csv',index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


print(train_data['svc_id'])


# In[ ]:





# In[ ]:





# In[ ]:


cat=['svc_id','complaint_status','is_5g','is_mix','is_sa_opened_silently','is_support_5gsa_dual','is_volte','user_group','miit5g','miit4g','miit3g','miit2g','is_dual','unicom_5g','unicom_4g','unicom_3g','unicom_2g','u_mize','t_mize','m_mize','all_mize','dinner_type','terminal_5g_type','ue_tac_id','sex','user_status','fuse_type','service_type','complaint_status'] 


# In[ ]:


#train_data = train_data.drop(['msisdn','NLP','user_lv_tfidf','model_name_tfidf','terminal_5g_type_tfidf'], axis=1)
#test_data = test_data.drop(['msisdn','NLP','user_lv_tfidf','model_name_tfidf','terminal_5g_type_tfidf'], axis=1)
train_data = train_data.drop(['msisdn','model_id'], axis=1)
test_data = test_data.drop(['msisdn','model_id'], axis=1)


# In[ ]:


# 选择相关性大于0.05的作为候选特征参与训练，并加入我们认为比较重要的特征，总共66个特征参与训练
#features = (train_data.corr()['score'][abs(train_data.corr()['score'])!='K']).index
features = train_data.columns.values.tolist()
features.remove('score')
len(features)


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(12,12))
x = train_data['score'].value_counts().index.values
y = train_data["score"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


#train_data['score'][train_data['score'] < 2] =1
#train_data['score'][train_data['score'] > 8] =0
#train_data = train_data[(train_data['score'] == 1) | (train_data['score'] ==0)]


# In[ ]:


# 生成数据和标签
target = train_data['score']
train_selected = train_data[features]
test = test_data[features]
feature_importance_df = pd.DataFrame()
oof = np.zeros(len(train_data))
predictions = np.zeros(len(test_data))
#train_selected['group'] = train_data['group']
#test['group'] = test_data['group']


# In[ ]:


#train_selected['group']=train_selected['group'].fillna(0)
#test['group']=test['group'].fillna(0)


# In[ ]:


#train_selected=train_selected.fillna(0)
#test=test.fillna(0)


# In[ ]:





# In[ ]:





# In[ ]:


train_selected.info(verbose=True, null_counts=True)


# In[ ]:


train_selected.shape


# In[ ]:


test.shape


# In[ ]:


params = {'num_leaves': 95,
         'min_data_in_leaf': 40,
         'objective': 'regression_l1',
         'max_depth': 16,
         'learning_rate': 0.01,
         'boosting': 'gbdt',
         'bagging_freq': 5,
         'bagging_fraction': 0.8,   # 每次迭代时用的数据比例0.8
         'feature_fraction': 0.8201,# 每次迭代中随机选择80％的参数来建树0.8201
         'bagging_seed': 11,
         'reg_alpha': 1.728910519108444,
         'reg_lambda': 4.9847051755586085,
         'random_state': 42,
         'max_bin':1023,
        'metric': 'rmse',
         'verbosity': -1,
         'subsample': 0.81,
         'min_gain_to_split': 0.01077313523861969,
         'min_child_weight': 19.428902804238373,
         'num_threads': 4,
         'seed':2021}
       

kfolds = KFold(n_splits=5,shuffle=True,random_state=15)
predictions = np.zeros(len(test))


for fold_n,(trn_index,val_index) in enumerate(kfolds.split(train_selected,target)):
    print("fold_n {}".format(fold_n))
    trn_data = lgb.Dataset(train_selected.iloc[trn_index],label=target.iloc[trn_index])
    val_data = lgb.Dataset(train_selected.iloc[val_index],label=target.iloc[val_index])
    num_round=100000
    clf = lgb.train(params, trn_data, num_round, valid_sets = [trn_data, val_data], verbose_eval=1000, early_stopping_rounds = 8000,categorical_feature=cat)
    oof[val_index] = clf.predict(train_selected.iloc[val_index], num_iteration=clf.best_iteration)
    predictions += clf.predict(test,num_iteration=clf.best_iteration)/5
    fold_importance_df = pd.DataFrame()
    fold_importance_df["feature"] = features
    fold_importance_df["importance"] = clf.feature_importance()
    fold_importance_df["fold"] = fold_n + 1
    feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)
    #print("CV score: {:<8.5f}".format(mean_squared_error(target, oof)**0.5))


# In[ ]:


cols = (feature_importance_df[["feature", "importance"]]
        .groupby("feature")
        .mean()
        .sort_values(by="importance", ascending=False)[:1000].index)
best_features = feature_importance_df.loc[feature_importance_df.feature.isin(cols)]

plt.figure(figsize=(14,26))
sns.barplot(x="importance", y="feature", data=best_features.sort_values(by="importance",ascending=False))
plt.title('LightGBM Features (averaged over folds)')
plt.tight_layout()


# In[ ]:


best_features.to_csv('best_features.csv',index=False)


# In[ ]:


# 计算结果
submision_lgb1=test
submision_lgb1['value']=predictions
submision_lgb1['value'].to_csv('G-submision_lgb1.csv',index=False)

submision_lgb1['value'].to_csv('G-submision_lgb1.csv',index=False)


# In[ ]:


predictions_lgb_R = submision_lgb1['value'].round(0)

predictions_lgb_R.to_csv('G-predictions_lgb_R.csv',index=False)


# In[ ]:


print(predictions)


# In[ ]:


submision_lgb1=test
submision_lgb1['value']=predictions
submision_lgb1['value'][submision_lgb1['value'] >8.5] =10
#submision_lgb1['value'][submision_lgb1['value'] <=6] =1
submision_lgb1['value']=submision_lgb1['value'].round(0)


# In[ ]:


'''
plt.figure()
fig, ax = plt.subplots(figsize=(12,12))
x = submision_lgb1['value'].value_counts().index.values
y = submision_lgb1["value"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")
'''


# In[ ]:


submision_lgb1['value'].to_csv('赛题1_Day9_lgbm_1.csv',index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




