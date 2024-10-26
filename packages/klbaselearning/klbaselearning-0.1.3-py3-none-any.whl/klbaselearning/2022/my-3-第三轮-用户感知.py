#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.decomposition import PCA #主成分分析法
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
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
from sklearn.metrics import roc_auc_score, roc_curve,mean_squared_error
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
pd.set_option('display.max_columns',None)
warnings.filterwarnings("ignore")


# In[ ]:


# 导入数据  
print("Loading Data ... ")  
new_train_data = pd.read_csv('datasets/@huangzx23#fd1a8eafd2b79230d7853599248258a8/train.csv')
new_test_data = pd.read_csv('datasets/@huangzx23#fd1a8eafd2b79230d7853599248258a8/test.csv')
new_train_data = new_train_data.drop(['cell_most','is_user_new','flow_2g','flow_3g','flow_4g','is_voice_stable','net_speed','is_net_stable','is_net_cover','service_type','order_id','service_type','price','msisdn','cell_longest'], axis=1)
new_test_data = new_test_data.drop(['cell_most','is_user_new','flow_2g','flow_3g','flow_4g','is_voice_stable','net_speed','is_net_stable','is_net_cover','service_type','order_id','service_type','price','msisdn','cell_longest'], axis=1)


# In[ ]:


#合并字段
data_all = pd.concat([new_train_data.assign(is_train = 1),new_test_data.assign(is_train = 0)]) #合并train和test，并且用is_train进行标记
train = data_all['is_train'] == 1##提前进行标记
test  = data_all['is_train'] == 0
print('数据全集量是',len(data_all))
train_count = len(data_all[train])
print('训练集样本量是',train_count)
test_count = len(data_all[test])
print('测试集样本量是',test_count)
print('样本比例为：', train_count/test_count)


# In[ ]:


data_all.info(verbose=True, null_counts=True)


# In[ ]:


pd.set_option('display.max_rows',None)
data_all['user_sex'].value_counts()
data_all['complaint_theme']=data_all['complaint_theme'].fillna('0')


# In[ ]:


fact_list=data_all['user_dinner'].value_counts()[0:30]
data_all['user_dinner']=data_all['user_dinner'].apply(lambda x:'其他' if x not in fact_list else x)


# In[ ]:


label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['complaint_theme'].values)))
data_all['complaint_theme']=label.transform(list(data_all['complaint_theme'].values))


# In[ ]:


#######KNN填充缺失值
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=10)
data_all[['talklen_2g','talklen_3g','volte_talklen_out','volte_talklen_in','lte_uhttp_base_003_week','talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out','online_2g','online_3g','online_4g','online_5g','userp_count_003_2g','userp_count_003_3g','userp_count_003_4g','userp_count_006_2g','userp_count_006_3g','talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out','online_2g','online_3g','online_4g','online_5g','userp_count_003_2g','userp_count_003_3g','userp_count_003_4g','userp_count_006_2g','userp_count_006_3g','userp_count_006_4g','userp_count_010_2g','userp_count_010_3g','userp_count_010_4g','userp_count_009_2g','userp_count_009_3g','userp_count_009_4g','lte_uhttp_base_008_week','lte_uhttp_base_009_week','lte_uhttp_base_010_week','lte_uhttp_base_013_week','lte_uhttp_base_004_week','lte_uhttp_base_005_week','lte_uhttp_base_007_week','lte_uhttp_base_018_week','lte_uhttp_base_019_week','lte_uhttp_base_021_week','lte_uhttp_base_020_week','lte_uhttp_base_022_week','lte_uhttp_base_023_week','lte_uhttp_base_024_week','lte_uhttp_base_025_week','lte_uhttp_base_026_week','lte_uhttp_base_027_week','lte_uhttp_base_028_week','lte_uhttp_base_029_week','lte_uhttp_base_035_week','lte_uhttp_base_044_week','lte_uhttp_base_045_week','lte_uhttp_base_049_week','lte_uhttp_base_050_week','lte_uhttp_base_051_week','lte_uhttp_base_052_week','lte_uhttp_base_053_week','lte_uhttp_base_054_week','lte_ustreaming_base_007_week','lte_ustreaming_base_008_week','lte_ustreaming_base_009_week','lte_ustreaming_base_003_week','lte_ustreaming_base_004_week','lte_ustreaming_base_005_week','lte_ustreaming_base_006_week','lte_ustreaming_base_010_week','lte_ustreaming_base_011_week','lte_ustreaming_base_012_week','lte_ustreaming_base_013_week', 'lte_ustreaming_base_014_week','lte_ustreaming_base_015_week','lte_ustreaming_base_016_week']] = imputer.fit_transform(data_all[['talklen_2g','talklen_3g','volte_talklen_out','volte_talklen_in','lte_uhttp_base_003_week','talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out','online_2g','online_3g','online_4g','online_5g','userp_count_003_2g','userp_count_003_3g','userp_count_003_4g','userp_count_006_2g','userp_count_006_3g','talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out','online_2g','online_3g','online_4g','online_5g','userp_count_003_2g','userp_count_003_3g','userp_count_003_4g','userp_count_006_2g','userp_count_006_3g','userp_count_006_4g','userp_count_010_2g','userp_count_010_3g','userp_count_010_4g','userp_count_009_2g','userp_count_009_3g','userp_count_009_4g','lte_uhttp_base_008_week','lte_uhttp_base_009_week','lte_uhttp_base_010_week','lte_uhttp_base_013_week','lte_uhttp_base_004_week','lte_uhttp_base_005_week','lte_uhttp_base_007_week','lte_uhttp_base_018_week','lte_uhttp_base_019_week','lte_uhttp_base_021_week','lte_uhttp_base_020_week','lte_uhttp_base_022_week','lte_uhttp_base_023_week','lte_uhttp_base_024_week','lte_uhttp_base_025_week','lte_uhttp_base_026_week','lte_uhttp_base_027_week','lte_uhttp_base_028_week','lte_uhttp_base_029_week','lte_uhttp_base_035_week','lte_uhttp_base_044_week','lte_uhttp_base_045_week','lte_uhttp_base_049_week','lte_uhttp_base_050_week','lte_uhttp_base_051_week','lte_uhttp_base_052_week','lte_uhttp_base_053_week','lte_uhttp_base_054_week','lte_ustreaming_base_007_week','lte_ustreaming_base_008_week','lte_ustreaming_base_009_week','lte_ustreaming_base_003_week','lte_ustreaming_base_004_week','lte_ustreaming_base_005_week','lte_ustreaming_base_006_week','lte_ustreaming_base_010_week','lte_ustreaming_base_011_week','lte_ustreaming_base_012_week','lte_ustreaming_base_013_week', 'lte_ustreaming_base_014_week','lte_ustreaming_base_015_week','lte_ustreaming_base_016_week']])
print('train:success!')


# In[ ]:


new_train_data = data_all[data_all['is_train']== 1]
new_test_data  = data_all[data_all['is_train']== 0]

#new_train=new_train.astype('float64')
#new_test=new_test.astype('float64')

new_train_data = new_train_data.drop(['is_train'], axis=1)
new_test_data = new_test_data.drop(['value','is_train'], axis=1)

train_data=new_train_data
test_data=new_test_data


# In[ ]:


train_data.info(verbose=True, null_counts=True)
test_data.info(verbose=True, null_counts=True)


# In[ ]:


train_data_bak=train_data.copy()
test_data_bak=test_data.copy()


# In[ ]:


train_data.info(verbose=True, null_counts=True)
test_data.info(verbose=True, null_counts=True)


# In[ ]:


print('训练集样本量是',len(train_data))
print('测试集样本量是',len(test_data))

train_data['talk_count'] =np.sum(train_data[['talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out']],axis=1) #######################考虑分箱

train_data['online_all'] =np.sum(train_data[['online_2g','online_3g','online_4g','online_4g']],axis=1)   #######################考虑分箱

train_data['USERP_COUNT_1_1'] =np.sum(train_data[['userp_count_003_2g','userp_count_003_3g','userp_count_003_4g']],axis=1)   #######################考虑分箱

train_data['USERP_COUNT_1_1'] =np.sum(train_data[['userp_count_006_2g','userp_count_006_3g','userp_count_006_4g']],axis=1)  #######################考虑分箱

#train_data['USERP_COUNT_2'] =np.sum(train_data[['userp_count_010_2g','userp_count_010_3g','userp_count_010_4g',]],axis=1) / np.sum(train_data[['userp_count_009_2g','userp_count_009_3g','userp_count_009_4g']],axis=1) 

train_data['USERP_COUNT_2_1'] =train_data['userp_count_010_2g']/train_data['userp_count_009_2g']
train_data['USERP_COUNT_2_2'] =train_data['userp_count_010_3g']/train_data['userp_count_009_3g']
train_data['USERP_COUNT_2_3'] =train_data['userp_count_010_4g']/train_data['userp_count_009_4g']


# In[ ]:


print('训练集样本量是',len(test_data))
print('测试集样本量是',len(test_data))

test_data['talk_count'] =np.sum(test_data[['talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out']],axis=1) #######################考虑分箱

test_data['online_all'] =np.sum(test_data[['online_2g','online_3g','online_4g','online_4g']],axis=1)   #######################考虑分箱

test_data['USERP_COUNT_1_1'] =np.sum(test_data[['userp_count_003_2g','userp_count_003_3g','userp_count_003_4g']],axis=1)   #######################考虑分箱

test_data['USERP_COUNT_1_1'] =np.sum(test_data[['userp_count_006_2g','userp_count_006_3g','userp_count_006_4g']],axis=1)  #######################考虑分箱


# In[ ]:


train_data=train_data.drop(['is_lucknumber','talklen_2g','talklen_3g','volte_talklen_out','volte_talklen_in','lte_uhttp_base_003_week','talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out','online_2g','online_3g','online_4g',  
                            'online_5g','userp_count_003_2g','userp_count_003_3g','userp_count_003_4g','userp_count_006_2g','userp_count_006_3g','talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out','online_2g','online_3g',  
                            'online_4g','online_5g','userp_count_003_2g','userp_count_003_3g','userp_count_003_4g','userp_count_006_2g','userp_count_006_3g','userp_count_006_4g','userp_count_010_2g','userp_count_010_3g','userp_count_010_4g','userp_count_009_2g','userp_count_009_3g','userp_count_009_4g','lte_uhttp_base_008_week','lte_uhttp_base_009_week','lte_uhttp_base_010_week','lte_uhttp_base_013_week','lte_uhttp_base_004_week','lte_uhttp_base_005_week','lte_uhttp_base_007_week','lte_uhttp_base_018_week','lte_uhttp_base_019_week','lte_uhttp_base_021_week','lte_uhttp_base_020_week','lte_uhttp_base_022_week','lte_uhttp_base_023_week','lte_uhttp_base_024_week','lte_uhttp_base_025_week','lte_uhttp_base_026_week','lte_uhttp_base_027_week','lte_uhttp_base_028_week','lte_uhttp_base_029_week','lte_uhttp_base_035_week','lte_uhttp_base_044_week','lte_uhttp_base_045_week','lte_uhttp_base_049_week','lte_uhttp_base_050_week','lte_uhttp_base_051_week','lte_uhttp_base_052_week','lte_uhttp_base_053_week','lte_uhttp_base_054_week','lte_ustreaming_base_007_week','lte_ustreaming_base_008_week','lte_ustreaming_base_009_week','lte_ustreaming_base_003_week','lte_ustreaming_base_004_week','lte_ustreaming_base_005_week','lte_ustreaming_base_006_week','lte_ustreaming_base_010_week','lte_ustreaming_base_011_week','lte_ustreaming_base_012_week','lte_ustreaming_base_013_week', 'lte_ustreaming_base_014_week','lte_ustreaming_base_015_week','lte_ustreaming_base_016_week','user_status','used_4g','mzie_type','is_volte_sign','is_l900','used_2g','used_5g','cell_type','is_5g','rat','is_mix','miit_net','used_3g','is_dual'], axis=1)

test_data=test_data.drop(['is_lucknumber','talklen_2g','talklen_3g','volte_talklen_out','volte_talklen_in','lte_uhttp_base_003_week','talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out','online_2g','online_3g','online_4g','online_5g','userp_count_003_2g','userp_count_003_3g','userp_count_003_4g','userp_count_006_2g','userp_count_006_3g','talk_2g_count_in','talk_3g_count_in','talk_volte_count_in','talk_2g_count_out','talk_3g_count_out','talk_volte_count_out','online_2g','online_3g','online_4g','online_5g','userp_count_003_2g','userp_count_003_3g','userp_count_003_4g','userp_count_006_2g','userp_count_006_3g','userp_count_006_4g','userp_count_010_2g','userp_count_010_3g','userp_count_010_4g','userp_count_009_2g','userp_count_009_3g','userp_count_009_4g','lte_uhttp_base_008_week','lte_uhttp_base_009_week','lte_uhttp_base_010_week','lte_uhttp_base_013_week','lte_uhttp_base_004_week','lte_uhttp_base_005_week','lte_uhttp_base_007_week','lte_uhttp_base_018_week','lte_uhttp_base_019_week','lte_uhttp_base_021_week','lte_uhttp_base_020_week','lte_uhttp_base_022_week','lte_uhttp_base_023_week','lte_uhttp_base_024_week','lte_uhttp_base_025_week','lte_uhttp_base_026_week','lte_uhttp_base_027_week','lte_uhttp_base_028_week','lte_uhttp_base_029_week','lte_uhttp_base_035_week','lte_uhttp_base_044_week','lte_uhttp_base_045_week','lte_uhttp_base_049_week','lte_uhttp_base_050_week','lte_uhttp_base_051_week','lte_uhttp_base_052_week','lte_uhttp_base_053_week','lte_uhttp_base_054_week','lte_ustreaming_base_007_week','lte_ustreaming_base_008_week','lte_ustreaming_base_009_week','lte_ustreaming_base_003_week','lte_ustreaming_base_004_week','lte_ustreaming_base_005_week','lte_ustreaming_base_006_week','lte_ustreaming_base_010_week','lte_ustreaming_base_011_week','lte_ustreaming_base_012_week','lte_ustreaming_base_013_week', 'lte_ustreaming_base_014_week','lte_ustreaming_base_015_week','lte_ustreaming_base_016_week','user_status','used_4g','mzie_type','is_volte_sign','is_l900','used_2g','used_5g','cell_type','is_5g','rat','is_mix','miit_net','used_3g','is_dual'], axis=1)

'''
where_are_inf = np.isinf(train_data)
train_data[where_are_inf] = 0

where_are_inf = np.isinf(test_data)
test_data[where_are_inf] = 0
'''
train_data.to_csv('train_data_count.csv',index=False)
test_data.to_csv('test_data_count.csv',index=False)


# In[ ]:


print(np.isnan(train_data).any())
print(np.isnan(test_data).any())


# In[ ]:


####填充0值
train_data=train_data.fillna(0)
test_data=test_data.fillna(0)

print(np.isnan(train_data).any())
print(np.isnan(test_data).any())


# In[ ]:


# 目前只考虑通过相关性选择特征
#train_data.corr()['value'][abs(train_data.corr()['value'])!='K']


# In[ ]:


# 选择相关性大于0.05的作为候选特征参与训练，并加入我们认为比较重要的特征，总共66个特征参与训练
features = (train_data.corr()['value'][abs(train_data.corr()['value'])!='K']).index
features = features.values.tolist()
features.remove('value')
len(features)


# In[ ]:


'''
train_data['rat']= train_data['rat'].astype('category')
train_data['cell_type']= train_data['cell_type'].astype('category')
'''


# In[ ]:


# 生成数据和标签
target = train_data['value']
train_selected = train_data[features]
test = test_data[features]
feature_importance_df = pd.DataFrame()
oof = np.zeros(len(train_data))
predictions = np.zeros(len(test_data))


# In[ ]:


params = {'num_leaves': 9,
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
         'metric': 'mae',
         'verbosity': -1,
         'subsample': 0.81,
         'min_gain_to_split': 0.01077313523861969,
         'min_child_weight': 19.428902804238373,
         'num_threads': 4,
         'seed':2021}   
kfolds = KFold(n_splits=5,shuffle=True,random_state=15)
predictions = np.zeros(len(test))
cat=['is_5g_dinner','complaint_theme','complaint_channel','fact_name','user_dinner','user_sex','user_lv','is_voice_cover','is_volte','in_net_group','acct_charge_type','gprs_bytes_type','complaint_level'] 
for fold_n,(trn_index,val_index) in enumerate(kfolds.split(train_selected,target)):
    print("fold_n {}".format(fold_n))
    trn_data = lgb.Dataset(train_selected.iloc[trn_index],label=target.iloc[trn_index])
    val_data = lgb.Dataset(train_selected.iloc[val_index],label=target.iloc[val_index])
    num_round=30000
    clf = lgb.train(params, trn_data, num_round, valid_sets = [trn_data, val_data], verbose_eval=1000, early_stopping_rounds = 8000,categorical_feature=cat)
    oof[val_index] = clf.predict(train_selected.iloc[val_index], num_iteration=clf.best_iteration)
    predictions += clf.predict(test,num_iteration=clf.best_iteration)/5
    fold_importance_df = pd.DataFrame()
    fold_importance_df["feature"] = features
    fold_importance_df["importance"] = clf.feature_importance()
    fold_importance_df["fold"] = fold_n + 1
    feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)
    print("CV score: {:<8.5f}".format(mean_squared_error(target, oof)**0.5))


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
submision_lgb1['value'].to_csv('submision_lgb1.csv',index=False)


# In[ ]:


preds=pd.DataFrame(preds) 
preds.to_csv('new_preds.csv',index=False)


# In[ ]:


temp2=pd.DataFrame(preds)
result = temp2
result1 =result
result1['value']=0
numlist = np.array(result1)
gsl=np.argmax(numlist,axis=1)
#print(gsl)
i=0
k=len(gsl)
for i in range(k):
    result['value'][i]=gsl[i]+1


# In[ ]:


result1[['value']].to_csv('submit_B.csv',index=False)

