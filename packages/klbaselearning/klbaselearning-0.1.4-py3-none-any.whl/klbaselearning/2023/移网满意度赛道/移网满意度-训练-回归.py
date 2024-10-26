#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.decomposition import PCA #主成分分析法

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

from autogluon.tabular import TabularDataset,TabularPredictor
from autogluon.multimodal import MultiModalPredictor

os.environ["NUMEXPR_MAX_THREADS"] = '20'


# In[ ]:


# 导入数据  
print("Loading Data ... ")  
train_data = pd.read_csv('X_train_transformed_915.csv')
test_data = pd.read_csv('X_test_transformed_915.csv')


# In[ ]:


'''
def reduce_mem_usage(df):
    # 处理前 数据集总内存计算
    start_mem = df.memory_usage().sum() / 1024**2 
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    # 遍历特征列
    for col in df.columns:
        # 当前特征类型
        col_type = df[col].dtype
        # 处理 numeric 型数据
        if col_type != object:
            c_min = df[col].min()  # 最小值
            c_max = df[col].max()  # 最大值
            # int 型数据 精度转换
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            # float 型数据 精度转换
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        # 处理 object 型数据
        else:
            df[col] = df[col].astype('category')  # object 转 category
    
    # 处理后 数据集总内存计算
    end_mem = df.memory_usage().sum() / 1024**2 
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df
train_data = reduce_mem_usage(train_data)  # 精度量化

test_data = reduce_mem_usage(test_data)  # 精度量化
'''


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


'''
train_data['score'][train_data['score'] <6 ] =1
#train_data['score'][train_data['score'] < 2] =0
train_data['score'][train_data['score'] >7]=10

#train_data['score']=train_data['score']*10
'''


# In[ ]:


#train_data = train_data[(train_data['score'] == 1) | (train_data['score'] ==10)]


# In[ ]:


#train_data['support_band']= train_data['support_band'].astype(str)
#test_data['support_band']= test_data['support_band'].astype(str)


# In[ ]:





# In[ ]:


data_all = train_data.copy()


# In[ ]:


data_all.shape


# In[ ]:


data_target = data_all['score']


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





# In[ ]:


data_all.shape


# In[ ]:


data_all['score'] = data_target


# In[ ]:


#df = data_all[data_all['score'].notnull()]


# In[ ]:


df = data_all.copy()


# In[ ]:


df.shape


# In[ ]:


df.info(verbose=True, null_counts=True)


# In[ ]:


'''

#每个字段前加上序号，解决列名同名问题
df = df.rename(columns={col: f"{i}_{col}" for i, col in enumerate(df.columns)})
import re
#去除字段名中汉字和常规符号以外的符号
df = df.rename(columns = lambda x:re.sub('[^A-Za-z0-9\u4e00-\u9fa5_]+', '', x))
'''


# In[ ]:





# In[ ]:


df.shape


# In[ ]:


newdf = df.copy()


# In[ ]:


#newdf['oneanswer'][newdf['oneanswer'] < 3] =1


# In[ ]:


#newdf['oneanswer'][newdf['oneanswer'] > 7] =0


# In[ ]:





# In[ ]:


#newdf = newdf[(newdf['oneanswer'] == 1) | (newdf['oneanswer'] ==0)]


# In[ ]:


#newdf = newdf.drop(['设备号','用户编码','上网账号','标准地址','详细地址','用户IP',  '用户MAC','地址','地市'], axis=1)
            


# In[ ]:





# In[ ]:





# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = newdf['score'].value_counts().index.values
y = newdf["score"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


newdf['dinner_type'] = newdf['dinner_type'].astype('category')
newdf['terminal_5g_type'] = newdf['terminal_5g_type'].astype('category')
newdf['model_id'] = newdf['model_id'].astype('category')
newdf['support_band'] = newdf['support_band'].astype('category')
newdf['ue_tac_id'] = newdf['ue_tac_id'].astype('category')
newdf['agegroup'] = newdf['agegroup'].astype('category')
newdf['datagroup'] = newdf['datagroup'].astype('category')
newdf['billgroup'] = newdf['billgroup'].astype('category')
newdf['volte_duragroup'] = newdf['volte_duragroup'].astype('category')
newdf['flowgroup'] = newdf['flowgroup'].astype('category')
newdf['call_out_timesgroup'] = newdf['call_out_timesgroup'].astype('category')
newdf['call_out_duragroup'] = newdf['call_out_duragroup'].astype('category')
newdf['call_in_timesgroup'] = newdf['call_in_timesgroup'].astype('category')
newdf['listed_pricegroup'] = newdf['listed_pricegroup'].astype('category')
newdf['user_lv'] = newdf['user_lv'].astype('category')
newdf['sex'] = newdf['sex'].astype('category')
newdf['user_status'] = newdf['user_status'].astype('category')
newdf['fuse_type'] = newdf['fuse_type'].astype('category')
newdf['service_type'] = newdf['service_type'].astype('category')
newdf['complaint_status'] = newdf['complaint_status'].astype('category')




test_data['dinner_type'] = test_data['dinner_type'].astype('category')
test_data['terminal_5g_type'] = test_data['terminal_5g_type'].astype('category')
test_data['model_id'] = test_data['model_id'].astype('category')
newdf['support_band'] = newdf['support_band'].astype('category')
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


# In[ ]:


newdf.info(verbose=True, null_counts=True)
from sklearn.model_selection import train_test_split
X=newdf
y=newdf['score']
train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.2,random_state=2022)
print(test_x.shape)
print(train_x.shape)
print(test_y.shape)


# In[ ]:


train_x['score'] = train_y


# In[ ]:





# In[ ]:


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


# In[ ]:


excluded_model_types = ['NN_TORCH','FASTAI']


# In[ ]:


predictor = TabularPredictor(label='score',eval_metric='rmse',problem_type='regression').fit(train_data=X ,excluded_model_types=excluded_model_types,num_bag_folds=10,num_stack_levels=4,num_bag_sets=10,) #,eval_metric='f1' ,hyperparameters='multimodal',eval_metric='roc_auc', num_bag_folds=8,num_stack_levels=3,num_bag_sets=1,num_bag_sets=2, verbosity = 3,num_stack_levels=3,ag_args_fit={'num_cpus': 20},hyperparameters = {'NN_TORCH': {'num_epochs': 500}, },#auto_stack=True,  num_bag_folds=5, num_bag_sets=3, num_stack_levels=3 ,,num_bag_folds=8,num_stack_levels=4,num_bag_sets=5,auto_stack=True,excluded_model_types=excluded_model_types,hyperparameters='multimodal',


# In[ ]:


#predictor=TabularPredictor.load("AutogluonModels/ag-20220918_024352/")

results = predictor.fit_summary()  


# In[ ]:


predictor=TabularPredictor.load("AutogluonModels/ag-20220918_024352/")
#预测数据
#test_data = test_data.drop(['msisdn'], axis=1)
pred_test=predictor.predict(test_data)#,model='LightGBM'predict_proba


# In[ ]:


print(pred_test)


# In[ ]:


#test_data['value'] = pred_test[1].apply(lambda x:1 if x>0.8 else 0)
test_data['value'] = pred_test


# In[ ]:


test_data['value'].to_csv('赛题1_day7_1.csv',index=False)


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = test_data['value'].value_counts().index.values
y = test_data['value'].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


hsdata = pd.read_csv('Day2_sub_2.csv')


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = hsdata['value'].value_counts().index.values
y = hsdata['value'].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


#test_data['value'] = pred_test
test_data['value'][test_data['value'] < 5] =1
test_data['value'][test_data['value'] > 5] =10

test_data[['value']].to_csv('Day7_sub_1.csv', index=False)


# In[ ]:


test_data['value'][test_data['value'] == 10].count()
test_data['value'][test_data['value'] == 1].count()


# In[ ]:


print(test_data['value'])


# In[ ]:


test_data['value'][test_data['value'] < 1] =10


# In[ ]:





# In[ ]:


high_tresh = pred['high_tresh']
mid_tresh = pred['mid_tresh']


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = pred['high_tresh'].value_counts().index.values
y = pred['high_tresh'].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = pred['mid_tresh'].value_counts().index.values
y = pred['mid_tresh'].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:





# In[ ]:


cy=confusion_matrix(high_tresh, test_y)
print("confusion_matrix:",cy)
dc=accuracy_score(high_tresh, test_y)
print("accuracy_score",dc)
recall=recall_score(high_tresh, test_y)
print("recall_score",recall)
f1=f1_score(high_tresh, test_y)
print("f1_score",f1)
precision=precision_score(high_tresh, test_y)
print("precision",precision)


# In[ ]:


cy=confusion_matrix(mid_tresh, test_y)
print("confusion_matrix:",cy)
dc=accuracy_score(mid_tresh, test_y)
print("accuracy_score",dc)
recall=recall_score(mid_tresh, test_y)
print("recall_score",recall)
f1=f1_score(mid_tresh, test_y)
print("f1_score",f1)
precision=precision_score(mid_tresh, test_y)
print("precision",precision)


# In[ ]:


#predictor.leaderboard(train_x, silent=True)


# In[ ]:


pd.options.display.max_rows = None


# In[ ]:


predictor.feature_importance(test_x)


# In[ ]:





# In[ ]:




