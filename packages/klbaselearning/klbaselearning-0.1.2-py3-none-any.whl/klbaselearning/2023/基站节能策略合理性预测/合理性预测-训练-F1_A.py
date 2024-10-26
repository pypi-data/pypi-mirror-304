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

os.environ["NUMEXPR_MAX_THREADS"] = '20'


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# 导入数据  
print("Loading Data ... ")  
train_data = pd.read_csv('train_去重_时间特征_mean.csv')
test_data = pd.read_csv('test_去重_时间特征_mean.csv')
best_sub = pd.read_csv('The_best_sub.csv')
print("Done ... ")  


# In[ ]:


train_data = train_data.drop(['CI','day','dayPart','节能策略是否合理（0为不合理，1为合理）'], axis=1)
test_data = test_data.drop(['CI','day','dayPart','节能策略是否合理（0为不合理，1为合理）'], axis=1)


# In[ ]:


test_data.shape


# In[ ]:


test_data2 = test_data.copy()

test_data2['label'] = best_sub['1']


# In[ ]:


#best_sub[best_sub['1']>0.8].count()  #注"0.992"该数值由于上一次迭代的时候没做记录，但误差应该在0.0001-0.001之间


# In[ ]:


best_sub[best_sub['1']<0.15].count()  #注"0.009"该数值由于上一次迭代的时候没做记录了，但误差应该在0.0001-0.003之间


# In[ ]:


#new_test2 = test_data2[(test_data2['label'] > 0.8) | (test_data2['label'] < 0.2)] #具体数值由于上一次迭代的时候没做记录了，但误差应该在0.0001-0.003之间


# In[ ]:


new_test2 = test_data2[test_data2['label'] < 0.15] #具体数值由于上一次迭代的时候没做记录了，但误差应该在0.0001-0.003之间


# In[ ]:


#new_test2['label'][new_test2['label'] > 0.8] =1


# In[ ]:


new_test2['label'][new_test2['label'] < 0.15] =0


# In[ ]:


newdf = pd.concat([train_data.assign(is_train = 1),new_test2.assign(is_train = 0)],ignore_index=True) #合并train和test，并且用is_train进行标记

newdf = newdf.drop(['is_train'], axis=1)


# In[ ]:


newdf.info(verbose=True, null_counts=True)


# In[ ]:





# In[ ]:


#train_data = train_data.drop(['CI','Year','Month','DayOfWeek','DayOfYear','Minute','Second','MU_second','WeekOfYear'], axis=1)
#test_data = test_data.drop(['CI','Year','Month','DayOfWeek','DayOfYear','Minute','Second','MU_second','WeekOfYear'], axis=1)

#train_data = train_data.drop(['CI','day','dayPart','节能策略是否合理（0为不合理，1为合理）','time'], axis=1)
#test_data = test_data.drop(['CI','day','dayPart','time'], axis=1)


# In[ ]:


#data_all = train_data.copy()

data_all = newdf.copy()


# In[ ]:


data_all.shape


# In[ ]:


df_bak = data_all.copy()


# In[ ]:


#data_target = data_all['节能策略是否合理（0为不合理，1为合理）']
data_target = data_all['label']


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(12,12))
x = train_data['label'].value_counts().index.values
y = train_data["label"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


data_all.shape


# In[ ]:


data_all['label'] = data_target


# In[ ]:


df = data_all[data_all['label'].notnull()]


# In[ ]:


#df = data_all.copy()


# In[ ]:


df.shape


# In[ ]:





# In[ ]:


df.info(verbose=True, null_counts=True)


# In[ ]:


df.shape


# In[ ]:


newdf = df.copy()


# In[ ]:


#newdf['score'][newdf['score'] < 3] =1


# In[ ]:


#newdf['score'][newdf['score'] > 7] =0


# In[ ]:





# In[ ]:


#newdf = newdf[(newdf['score'] == 1) | (newdf['score'] ==0)]


# In[ ]:


#newdf = newdf.drop(['设备号','用户编码','上网账号','标准地址','详细地址','用户IP',  '用户MAC','地址','地市'], axis=1)
            


# In[ ]:


newdf['覆盖类型'] = newdf['覆盖类型'].astype('category')
newdf['覆盖场景'] = newdf['覆盖场景'].astype('category')
newdf['设备型号'] = newdf['设备型号'].astype('category')
newdf['补偿小区CI'] = newdf['补偿小区CI'].astype('category')
newdf['hour'] = newdf['hour'].astype('category')
newdf['weekday'] = newdf['weekday'].astype('category')
newdf['hour_section'] = newdf['hour_section'].astype('category')
#newdf['dayPart'] = newdf['dayPart'].astype('category')


test_data['覆盖类型'] = test_data['覆盖类型'].astype('category')
test_data['覆盖场景'] = test_data['覆盖场景'].astype('category')
test_data['设备型号'] = test_data['设备型号'].astype('category')
test_data['补偿小区CI'] = test_data['补偿小区CI'].astype('category')
test_data['hour'] = test_data['hour'].astype('category')
test_data['weekday'] = test_data['weekday'].astype('category')
test_data['hour_section'] = test_data['hour_section'].astype('category')
#test_data['dayPart'] = test_data['dayPart'].astype('category')



# In[ ]:


'''
newdf['覆盖类型'] = newdf['覆盖类型'].astype('category')
newdf['覆盖场景'] = newdf['覆盖场景'].astype('category')
newdf['设备型号'] = newdf['设备型号'].astype('category')
newdf['补偿小区CI'] = newdf['补偿小区CI'].astype('category')
newdf['Day'] = newdf['Day'].astype('category')
newdf['DayName'] = newdf['DayName'].astype('category')
newdf['Hour'] = newdf['Hour'].astype('category')
newdf['dayPart'] = newdf['dayPart'].astype('category')
'''
'''
test_data['覆盖类型'] = test_data['覆盖类型'].astype('category')
test_data['覆盖场景'] = test_data['覆盖场景'].astype('category')
test_data['设备型号'] = test_data['设备型号'].astype('category')
test_data['补偿小区CI'] = test_data['补偿小区CI'].astype('category')
test_data['Day'] = test_data['Day'].astype('category')
test_data['DayName'] = test_data['DayName'].astype('category')
test_data['Hour'] = test_data['Hour'].astype('category')
test_data['dayPart'] = test_data['dayPart'].astype('category')
'''


# In[ ]:


#newdf=newdf.fillna(0)
#test_data=test_data.fillna(0)


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = newdf['label'].value_counts().index.values
y = newdf["label"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


newdf.info(verbose=True, null_counts=True)
from sklearn.model_selection import train_test_split
X=newdf
y=newdf['label']
train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.2,random_state=2022)
print(test_x.shape)
print(train_x.shape)
print(test_y.shape)


# In[ ]:


train_x['label'] = train_y


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


#excluded_model_types = ['NN_TORCH','NN_FASTAI']
#eval_metric='f1_weighted'


# In[ ]:


predictor = TabularPredictor(label='label',eval_metric='f1_weighted').fit(train_data=X ,presets='best_quality', num_bag_folds=10, num_bag_sets=10, num_stack_levels=4) # num_bag_folds=8,num_stack_levels=3,num_bag_sets=1,num_bag_sets=2, verbosity = 3,num_stack_levels=3,ag_args_fit={'num_cpus': 20},hyperparameters = {'NN_TORCH': {'num_epochs': 500}, },#auto_stack=True,  num_bag_folds=5, num_bag_sets=3, num_stack_levels=3  #eval_metric='roc_auc'


# In[ ]:


results = predictor.fit_summary()  


# In[ ]:


#predictor=TabularPredictor.load("AutogluonModels/ag-20220912_021240")
'''
*** Summary of fit() ***
Estimated performance of each model:
                      model  score_val  pred_time_val     fit_time  pred_time_val_marginal  fit_time_marginal  stack_level  can_infer  fit_order
0       WeightedEnsemble_L5   0.915271      69.953944  7478.306790                0.024274           7.794599            5       True         50
1            XGBoost_BAG_L4   0.915227      68.921276  7465.664508                2.556023         201.592692            4       True         47
2       WeightedEnsemble_L3   0.914593      40.741064  5096.351064                0.041261           7.472069            3       True         26
3       WeightedEnsemble_L4   0.914556      54.927886  6201.464844                0.014463           5.151877            4       True         38
4     NeuralNetTorch_BAG_L3   0.914463      49.708189  5629.459257                5.323111         398.124239            3       True         36
5       WeightedEnsemble_L2   0.914234      18.791565  2593.633638                0.039804           9.560234            2       True         14
6      LightGBMLarge_BAG_L4   0.913775      67.734962  7442.490077                1.369709         178.418261            4       True         49
7   RandomForestGini_BAG_L4   0.913709      67.049243  7268.215044                0.683990           4.143228            4       True         41
8            XGBoost_BAG_L2   0.913640      24.459161  3503.976577                2.347610         371.624964            2       True         23
9    NeuralNetFastAI_BAG_L2   0.913533      26.821784  3509.698097                4.710233         377.346485            2       True         22
10   NeuralNetFastAI_BAG_L3   0.913533      49.164346  5605.267163                4.779268         373.932146            3       True         34
11          CatBoost_BAG_L2   0.913435      22.553539  3326.211859                0.441988         193.860247            2       True         19
12  RandomForestEntr_BAG_L2   0.913362      23.185019  3136.885408                1.073468           4.533795            2       True         18
13    NeuralNetTorch_BAG_L2   0.913288      27.697168  3574.128816                5.585617         441.777204            2       True         24
14           XGBoost_BAG_L3   0.913252      46.686315  5649.429996                2.301237         418.094978            3       True         35
15          CatBoost_BAG_L3   0.913246      44.811045  5424.256582                0.425967         192.921564            3       True         31
16  RandomForestEntr_BAG_L4   0.913013      67.373648  7268.919499                1.008394           4.847683            4       True         42
17          LightGBM_BAG_L4   0.912955      68.167994  7383.726045                1.802741         119.654228            4       True         40
18    ExtraTreesEntr_BAG_L2   0.912945      23.101859  3134.184126                0.990308           1.832513            2       True         21
19        LightGBMXT_BAG_L1   0.912862       1.926341   261.412921                1.926341         261.412921            1       True          3
20    ExtraTreesGini_BAG_L2   0.912849      23.344309  3134.131382                1.232758           1.779769            2       True         20
21    ExtraTreesGini_BAG_L4   0.912836      67.989594  7265.366983                1.624341           1.295167            4       True         44
22          CatBoost_BAG_L4   0.912768      66.908996  7429.657304                0.543743         165.585488            4       True         43
23   NeuralNetFastAI_BAG_L4   0.912744      71.830972  7754.189086                5.465719         490.117270            4       True         46
24        LightGBMXT_BAG_L2   0.912728      23.707860  3247.220716                1.596309         114.869103            2       True         15
25    ExtraTreesEntr_BAG_L4   0.912701      67.237549  7266.635502                0.872295           2.563685            4       True         45
26  RandomForestGini_BAG_L2   0.912643      22.859217  3137.099095                0.747666           4.747483            2       True         17
27    NeuralNetTorch_BAG_L4   0.912560      71.726569  7766.874484                5.361315         502.802667            4       True         48
28   NeuralNetFastAI_BAG_L1   0.912464       4.568176   453.783437                4.568176         453.783437            1       True         10
29     LightGBMLarge_BAG_L2   0.912365      23.954270  3583.034685                1.842719         450.683072            2       True         25
30        LightGBMXT_BAG_L3   0.912346      46.045994  5372.918433                1.660916         141.583416            3       True         27
31          LightGBM_BAG_L2   0.912234      23.816404  3268.280384                1.704853         135.928771            2       True         16
32          LightGBM_BAG_L3   0.912028      46.170790  5384.778895                1.785712         153.443878            3       True         28
33     LightGBMLarge_BAG_L3   0.911752      46.294036  5574.035845                1.908957         342.700827            3       True         37
34  RandomForestEntr_BAG_L3   0.911598      45.157122  5235.720312                0.772044           4.385295            3       True         30
35    ExtraTreesEntr_BAG_L3   0.911410      45.288309  5232.848217                0.903231           1.513199            3       True         33
36        LightGBMXT_BAG_L4   0.911358      68.207990  7361.567586                1.842736          97.495770            4       True         39
37          LightGBM_BAG_L1   0.911064       1.922750   218.361692                1.922750         218.361692            1       True          4
38          CatBoost_BAG_L1   0.910868       0.452191   325.257597                0.452191         325.257597            1       True          7
39    ExtraTreesGini_BAG_L3   0.910829      45.327627  5232.896573                0.942549           1.561556            3       True         32
40  RandomForestGini_BAG_L3   0.910692      45.562263  5235.810719                1.177185           4.475701            3       True         29
41     LightGBMLarge_BAG_L1   0.910504       1.966438   546.663002                1.966438         546.663002            1       True         13
42    NeuralNetTorch_BAG_L1   0.909544       5.257516   638.263313                5.257516         638.263313            1       True         12
43  RandomForestEntr_BAG_L1   0.909269       0.603494     1.106710                0.603494           1.106710            1       True          6
44           XGBoost_BAG_L1   0.909115       2.509154   681.984181                2.509154         681.984181            1       True         11
45  RandomForestGini_BAG_L1   0.909004       0.636096     2.572632                0.636096           2.572632            1       True          5
46    ExtraTreesGini_BAG_L1   0.907930       0.876044     1.330919                0.876044           1.330919            1       True          8
47    ExtraTreesEntr_BAG_L1   0.907767       1.030908     1.413571                1.030908           1.413571            1       True          9
48    KNeighborsUnif_BAG_L1   0.892364       0.188184     0.152025                0.188184           0.152025            1       True          1
49    KNeighborsDist_BAG_L1   0.891460       0.174260     0.049611                0.174260           0.049611            1       True          2
Number of models trained: 50
Types of models trained:
{'StackerEnsembleModel_XT', 'StackerEnsembleModel_KNN', 'WeightedEnsembleModel', 'StackerEnsembleModel_XGBoost', 'StackerEnsembleModel_NNFastAiTabular', 'StackerEnsembleModel_TabularNeuralNetTorch', 'StackerEnsembleModel_CatBoost', 'StackerEnsembleModel_RF', 'StackerEnsembleModel_LGB'}
Bagging used: True  (with 7 folds)
Multi-layer stack-ensembling used: True  (with 5 levels)
Feature Metadata (Processed):
(raw dtype, special dtypes):
('category', [])  :   7 | ['补偿小区CI', '覆盖类型', '覆盖场景', '设备型号', 'hour', ...]
('float', [])     : 183 | ['周边小区群数量', '周边小区群RRC连接平均数_群1', '周边小区群RRC连接平均数_群2', '周边小区群RRC连接平均数_群3', '周边小区群RRC连接平均数_群4', ...]
('int', ['bool']) :   1 | ['is_train__minimum']
Plot summary of models saved to file: AutogluonModels/ag-20220922_032953/SummaryOfModels.html
*** End of fit() summary ***
'''


# In[ ]:


predictor=TabularPredictor.load("AutogluonModels/ag-20220926_071308")
results = predictor.fit_summary()  


# In[ ]:


predictor=TabularPredictor.load("AutogluonModels/ag-20220926_071308")
#预测数据
pred_test=predictor.predict_proba(test_data)#,model='LightGBM'#predict_proba


# In[ ]:


print(pred_test)


# In[ ]:


#pred_test[1].to_csv('The_best_sub_F1_W.csv', index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


test_data['label'] = pred_test[1].apply(lambda x:1 if x>0.55 else 0) #[1 0] [4565 1837]


#test_data['label'] = pred_test
plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = test_data['label'].value_counts().index.values
y = test_data['label'].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


#test_data['label'] = pred_test[1].apply(lambda x:1 if x>0.5 else 0)


#test_data['label'] = pred_test[1]
test_data[['label']].to_csv('赛题2_Day20_融合_sub_0.55_1919.csv', index=False)

#pred_test[1].to_csv('The_best_sub.csv', index=False)


# In[ ]:


train_data2 = pd.read_csv('赛题2_Day1_sub_5_0.85796.csv')
plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = train_data2['label'].value_counts().index.values
y = train_data2['label'].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


new_test = test_data.copy()


# In[ ]:


new_test['value'][new_test['value'] < 8] =1


# In[ ]:


new_test['value'][new_test['value'] > 7] =10


# In[ ]:


plt.figure()
fig, ax = plt.subplots(figsize=(6,6))
x = new_test['value'].value_counts().index.values
y = new_test["value"].value_counts().values
print(x,y)
# Bar plot
# Order the bars descending on target mean
sns.barplot(ax=ax, x=x, y=y)
plt.ylabel('Number of values', fontsize=16)
plt.xlabel('is_attributed value', fontsize=16)
plt.savefig("标签分布.svg", format="svg")


# In[ ]:


new_test[['value']].to_csv('Day1_sub_5.csv', index=False)


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




