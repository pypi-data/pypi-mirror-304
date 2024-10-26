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

#from autogluon.tabular import TabularDataset,TabularPredictor

os.environ["NUMEXPR_MAX_THREADS"] = '20'

from tsfresh import extract_features, extract_relevant_features, select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import ComprehensiveFCParameters

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# In[ ]:


# 导入数据  
print("Loading Data ... ")  
train_data = pd.read_csv('train_data.csv')
test_data = pd.read_csv('validation.csv')
kpi_data = pd.read_csv('Compensation KPI.csv')

print("Done ... ")  


# In[ ]:


#kpi_data.info


# In[ ]:


#数据聚合
#kpi_data.drop_duplicates(subset=['时间', '日期','补偿小区CI'],keep='first', inplace=True)
kpi_data['time'] = kpi_data['日期'].map(str) + "/" + kpi_data['时间'].map(str) 
kpi_data['time'] = pd.to_datetime(kpi_data['time'])
kpi_data = kpi_data.drop_duplicates().groupby(["time", "补偿小区CI"], as_index=False).mean()


train_data['time'] = pd.to_datetime(train_data['time'])
test_data['time'] = pd.to_datetime(test_data['time'])
#数据合并
train_data = pd.merge(train_data, kpi_data, on=['time', '补偿小区CI'], how='left')
test_data = pd.merge(test_data, kpi_data, on=['time', '补偿小区CI'], how='left')
#train_data.drop(['日期', '时间'], axis=1, inplace=True)
#test_data.drop(['日期', '时间'], axis=1, inplace=True)


# In[ ]:


train_data_2 = train_data.copy()


# In[ ]:





# In[ ]:


train_data['time'] = pd.to_datetime(train_data['time'])
test_data['time'] = pd.to_datetime(test_data['time'])


# In[ ]:


data_all = pd.concat([train_data.assign(is_train = 1),test_data.assign(is_train = 0)]) #合并train和test，并且用is_train进行标记
train = data_all['is_train'] == 1##提前进行标记
test  = data_all['is_train'] == 0


# In[ ]:


#data_all = data_all.fillna()


# In[ ]:


data_all.shape


# In[ ]:


data_all.info()


# In[ ]:


data_all_old=pd.DataFrame()
data_all_old['time'] = data_all['time']
data_all_old['CI'] = data_all['CI']
data_all_old['补偿小区CI'] = data_all['补偿小区CI']



data_all_old['覆盖类型'] = data_all['覆盖类型']
data_all_old['覆盖场景'] = data_all['覆盖场景']
data_all_old['设备型号'] = data_all['设备型号']
data_all_old['节能策略是否合理（0为不合理，1为合理）'] = data_all['节能策略是否合理（0为不合理，1为合理）']


# In[ ]:


#train_data.drop(['覆盖类型', '覆盖场景','设备型号','补偿小区CI','节能策略是否合理（0为不合理，1为合理）'], axis=1, inplace=True)
#test_data.drop(['覆盖类型', '覆盖场景','设备型号','补偿小区CI','周边小区群数量'], axis=1, inplace=True)
data_all.drop(['覆盖类型', '覆盖场景','设备型号','补偿小区CI','节能策略是否合理（0为不合理，1为合理）'], axis=1, inplace=True)
data_all = data_all.drop_duplicates().groupby(["time", "CI"], as_index=False).mean()


# In[ ]:


num = data_all.columns.values.tolist()
num.remove('CI')

for col in num:
    data_all[col] = data_all[col].fillna(data_all[col].mean())
    data_all[col] = data_all[col].fillna(data_all[col].mean())


# In[ ]:


data_all.info


# In[ ]:


#data_all.drop(['周边小区群数量', '周边小区群RRC连接平均数_群2','周边小区群RRC连接平均数_群3','周边小区群RRC连接平均数_群4','周边小区群RRC连接平均数_群5','周边小区群RRC连接平均数_群6','周边小区群RRC连接平均数_群7','周边小区群RRC连接平均数_群8','周边小区群RRC连接平均数_群9','周边小区群RRC连接平均数_群10','RRC平均连接数_补偿小区','RRC连接最大数_补偿小区','上行PRB平均利用率_补偿小区','下行PRB平均利用率_补偿小区','PDCCH信道CCE占用率_补偿小区'], axis=1, inplace=True)
#data_all.drop([ '周边小区群RRC连接平均数_群1','周边小区群RRC连接平均数_群2','周边小区群RRC连接平均数_群3','周边小区群RRC连接平均数_群4','周边小区群RRC连接平均数_群5','周边小区群RRC连接平均数_群6','周边小区群RRC连接平均数_群7','周边小区群RRC连接平均数_群8','周边小区群RRC连接平均数_群9','周边小区群RRC连接平均数_群10','RRC平均连接数_补偿小区','RRC连接最大数_补偿小区','上行PRB平均利用率_补偿小区','下行PRB平均利用率_补偿小区','PDCCH信道CCE占用率_补偿小区'], axis=1, inplace=True)


# In[ ]:





# In[ ]:


def missing (df):
    """
    计算每一列的缺失值及占比
    """
    missing_number = df.isnull().sum().sort_values(ascending=False)              # 每一列的缺失值求和后降序排序                  
    missing_percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)          # 每一列缺失值占比
    missing_values = pd.concat([missing_number, missing_percent], axis=1, keys=['Missing_Number', 'Missing_Percent'])      # 合并为一个DataFrame
    return missing_values


# In[ ]:


missing(data_all)


# In[ ]:


#data_all.rename(columns={"周边小区群数量": 'CI_count'}, inplace=True)
data_all = data_all.reset_index()


# In[ ]:


from tsfresh.feature_extraction import extract_features, MinimalFCParameters
settings = MinimalFCParameters()
extracted_features_3 = extract_features(data_all, column_id="CI", column_sort="time",default_fc_parameters=settings)
extracted_features_3.shape


# In[ ]:





# In[ ]:





# In[ ]:


data_all.to_csv('data_all_check.csv',index=False)
data_all = pd.read_csv('data_all_check.csv')


# In[ ]:


from tsfresh.feature_extraction import extract_features, ComprehensiveFCParameters
from tsfresh.utilities.dataframe_functions import impute
extract_features1 = extract_features(data_all, column_id='CI', column_sort='time')


# In[ ]:





# In[ ]:





# In[ ]:


extracted_features_3.shape


# In[ ]:





# In[ ]:


extracted_features_3.index.name = 'CI'
extracted_features_4 = extracted_features_3.reset_index()


# In[ ]:





# In[ ]:


data_all_new = pd.merge(data_all, extracted_features_4, on=['CI'], how='left')


# In[ ]:


data_all_new_1 = pd.merge(data_all_old,data_all_new, on=['time', 'CI'], how='left')


# In[ ]:


data_all_new_1.shape


# In[ ]:


label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all_new_1['覆盖类型'].values)))
data_all_new_1['覆盖类型']=label.transform(list(data_all_new_1['覆盖类型'].values))


# In[ ]:


label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all_new_1['覆盖场景'].values)))
data_all_new_1['覆盖场景']=label.transform(list(data_all_new_1['覆盖场景'].values))


# In[ ]:


label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all_new_1['设备型号'].values)))
data_all_new_1['设备型号']=label.transform(list(data_all_new_1['设备型号'].values))


# In[ ]:


label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all_new_1['补偿小区CI'].values)))
data_all_new_1['补偿小区CI']=label.transform(list(data_all_new_1['补偿小区CI'].values))


# In[ ]:


def findDayPart(x):
    if (x>22 and x <=23) or (x>=0 and x<=7):
        return 0 #NIGHT
    if x>7 and x<20:
        return 1 #MORNING
    if x>=20 and x<=22:
        return 2 #PEAKHOURS



# In[ ]:


def simple_fea_stats(data):
    data['time'] = pd.to_datetime(data['time'])
    #简单特征统计
    data['time'] = data['time'].values.astype('datetime64[s]') #format='%d/%m/%Y'
    #data['year'] = data['time'].dt.year
    data['month'] = data['time'].dt.month
    data['day'] = data['time'].dt.day
    data['hour'] = data['time'].dt.hour
    #data['minute'] = data['time'].dt.minute
    #data['quarte'] = data['time'].dt.quarter
    #data['weekofyear'] = data['time'].dt.isocalendar().week   #提取年当中的周数
    data['weekday'] = data['time'].dt.weekday + 1 #提取周几
    #data['weekend'] = (data['weekday'] > 5).astype(int) 
    data['hour_section'] = (data['hour'] // 6).astype(int)  #进一步创建小时所属每一天的周期，周期以6小时为划分依据：
    data['dayPart'] = data['hour'].apply(findDayPart)
    return data


# In[ ]:


data_all_new_1 = simple_fea_stats(data_all_new_1)


# In[ ]:


data_all_new_1['覆盖类型'] = data_all_new_1['覆盖类型'].astype('category')
data_all_new_1['覆盖场景'] = data_all_new_1['覆盖场景'].astype('category')
data_all_new_1['设备型号'] = data_all_new_1['设备型号'].astype('category')
data_all_new_1['补偿小区CI'] = data_all_new_1['补偿小区CI'].astype('category')
data_all_new_1['day'] = data_all_new_1['day'].astype('category')
data_all_new_1['hour'] = data_all_new_1['hour'].astype('category')
data_all_new_1['weekday'] = data_all_new_1['weekday'].astype('category')
data_all_new_1['hour_section'] = data_all_new_1['hour_section'].astype('category')
#data_all['dayPart'] = data_all['dayPart'].astype('category')

#data_all = data_all.drop(['Year','Month','DayOfWeek','DayOfYear','Minute','Second','MU_second','WeekOfYear'], axis=1)
data_all_new_1 = data_all_new_1.drop(['month'], axis=1)


# In[ ]:


new_train_data = data_all_new_1[data_all_new_1['is_train']== 1]
new_test_data  = data_all_new_1[data_all_new_1['is_train']== 0]

new_train_data = new_train_data.drop(['is_train'], axis=1)
new_test_data = new_test_data.drop(['is_train'], axis=1)

new_train_data['label'] = train_data_2['节能策略是否合理（0为不合理，1为合理）'] 
#写入本地
new_train_data.to_csv('train_去重_时间特征_mean.csv',index=False)
new_test_data.to_csv('test_去重_时间特征_mean.csv',index=False)


# In[ ]:





# In[ ]:




