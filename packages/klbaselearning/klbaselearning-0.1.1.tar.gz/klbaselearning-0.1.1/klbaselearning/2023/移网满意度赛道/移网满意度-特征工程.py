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
import featuretools as ft
#from autogluon.tabular import TabularDataset,TabularPredictor

os.environ["NUMEXPR_MAX_THREADS"] = '20'
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


# In[ ]:


# 导入数据  
print("Loading Data ... ")  
train_data = pd.read_csv('train_data.csv')
test_data = pd.read_csv('test_data.csv')


# In[ ]:


train_data.shape


# In[ ]:


test_data.shape


# In[ ]:


#处理部分异常值为空值
train_data[train_data==-1]=np.nan
test_data[test_data==-1]=np.nan


train_data['user_lv'][train_data['user_lv'] =='未评级']=0
test_data['user_lv'][test_data['user_lv'] =='未评级']=0


# In[ ]:


# NLP特征衍生函数
def NLP_Group_Statistics(features, 
                         col_cat, 
                         keyCol=None,
                         tfidf=True, 
                         countVec=True):
    """
    NLP特征衍生函数
    
    :param features: 原始数据集
    :param col_cat: 参与衍生的离散型变量，只能带入多个列
    :param keyCol: 分组参考的关键变量，输入字符串时代表按照单独列分组，输入list代表按照多个列进行分组
    :param tfidf: 是否进行tfidf计算  
    :param countVec: 是否进行CountVectorizer计算

    :return：NLP特征衍生后的新特征和新特征的名称
    """
    
    # 提取所有需要带入计算的特征名称和特征
    if keyCol != None:
        if type(keyCol) == str:
            keyCol = [keyCol]    
        colName_temp = keyCol.copy()
        colName_temp.extend(col_cat)
        features = features[colName_temp]
    else:
        features = features[col_cat]
    
    # 定义CountVectorizer计算和TF-IDF计算过程
    def NLP_Stat(features=features, 
                 col_cat=col_cat, 
                 keyCol=keyCol, 
                 countVec=countVec, 
                 tfidf=tfidf):
        """
        CountVectorizer计算和TF-IDF计算函数
        
        参数和外层函数参数完全一致
        返回结果需要注意，此处返回带有keyCol的衍生特征矩阵及特征名称
        """
        n = len(keyCol)
        col_cat = [x +'_' + '&'.join(keyCol) for x in col_cat]
        if tfidf == True:
            # 计算CountVectorizer
            features_new_cntv = features.groupby(keyCol).sum().reset_index()
            colNames_new_cntv = keyCol.copy()
            colNames_new_cntv.extend([x + '_cntv' for x in col_cat])
            features_new_cntv.columns = colNames_new_cntv
            
            # 计算TF-IDF
            transformer = TfidfTransformer()
            tfidf = transformer.fit_transform(features_new_cntv.iloc[:, n: ]).toarray()
            colNames_new_tfv = [x + '_tfidf' for x in col_cat]
            features_new_tfv = pd.DataFrame(tfidf, columns=colNames_new_tfv)
            
            if countVec == True:
                features_new = pd.concat([features_new_cntv, features_new_tfv], axis=1)
                colNames_new_cntv.extend(colNames_new_tfv)
                colNames_new = colNames_new_cntv
            else:
                colNames_new = keyCol + colNames_new_tfv
                features_new = pd.concat([features_new_cntv.iloc[:, :n], features_new_tfv], axis=1)
        
        # 如果只计算CountVectorizer时
        elif countVec == True:
            features_new_cntv = features.groupby(keyCol).sum().reset_index()
            colNames_new_cntv = keyCol.copy()
            colNames_new_cntv.extend([x + '_cntv' for x in col_cat])
            features_new_cntv.columns = colNames_new_cntv     
            
            colNames_new = colNames_new_cntv
            features_new = features_new_cntv
        
        return features_new, colNames_new
    
    # keyCol==None时对原始数据进行NLP特征衍生
    # 此时无需进行CountVectorizer计算
    if keyCol == None:
        if tfidf == True:
            transformer = TfidfTransformer()
            tfidf = transformer.fit_transform(features).toarray()
            colNames_new = [x + '_tfidf' for x in col_cat]
            features_new = pd.DataFrame(tfidf, columns=colNames_new)
    
    # keyCol!=None时对分组汇总后的数据进行NLP特征衍生
    else:
        n = len(keyCol)
        # 如果是依据单个特征取值进行分组
        if n == 1:
            features_new, colNames_new = NLP_Stat()
            # 将分组统计结果拼接回原矩阵
            features_new = pd.merge(features[keyCol[0]], features_new, how='left',on=keyCol[0])
            features_new = features_new.iloc[:, n: ]
            colNames_new = features_new.columns
            
        # 如果是多特征交叉分组
        else:
            features_new, colNames_new = NLP_Stat()
            # 在原数据集中生成合并主键
            features_key1, col1 = Multi_Cross_Combination(keyCol, features, OneHot=False)
            # 在衍生特征数据集中创建合并主键
            features_key2, col2 = Multi_Cross_Combination(keyCol, features_new, OneHot=False)
            features_key2 = pd.concat([features_key2, features_new], axis=1)
            # 将分组统计结果拼接回原矩阵
            features_new = pd.merge(features_key1, features_key2, how='left',on=col1)
            features_new = features_new.iloc[:, n+1: ]
            colNames_new = features_new.columns
        
    colNames_new = list(colNames_new)
            
    return features_new, colNames_new


#######################################################
## Part 3.高阶封装函数辅助函数

def Features_Padding(features_train_new, 
                     features_test_new, 
                     colNames_train_new, 
                     colNames_test_new):
    """
    特征零值填补函数
    
    :param features_train_new: 训练集衍生特征
    :param features_test_new: 测试集衍生特征
    :param colNames_train_new: 训练集衍生列名称
    :param colNames_test_new: 测试集衍生列名称
    
    :return：0值填补后的新特征和特征名称
    """
    if len(colNames_train_new) > len(colNames_test_new):
        sub_colNames = list(set(colNames_train_new) - set(colNames_test_new))
        
        for col in sub_colNames:
            features_test_new[col] = 0
        
        features_test_new = features_test_new[colNames_train_new]
        colNames_test_new = list(features_test_new.columns)
            
    elif len(colNames_train_new) < len(colNames_test_new):
        sub_colNames = list(set(colNames_test_new) - set(colNames_train_new))
        
        for col in sub_colNames:
            features_train_new[col] = 0
        
        features_train_new = features_train_new[colNames_test_new]
        colNames_train_new = list(features_train_new.columns)    
    assert colNames_train_new  == colNames_test_new
    return features_train_new, features_test_new, colNames_train_new, colNames_test_new        


def test_features(keyCol,
                  X_train, 
                  X_test,
                  features_train_new,
                  multi=False):
    """
    测试集特征填补函数
    
    :param keyCol: 分组参考的关键变量
    :param X_train: 训练集特征
    :param X_test: 测试集特征
    :param features_train_new: 训练集衍生特征
    :param multi: 是否多变量参与分组
    
    :return：分组统计衍生后的新特征和新特征的名称
    """
    
    # 创建主键
    # 创建带有主键的训练集衍生特征df
    # 创建只包含主键的test_key
    if multi == False:
        keyCol = keyCol
        features_train_new[keyCol] = X_train[keyCol].reset_index()[keyCol]
        test_key = pd.DataFrame(X_test[keyCol])
    else:
        train_key, train_col = Multi_Cross_Combination(colNames=keyCol, features=X_train, OneHot=False)
        test_key, test_col = Multi_Cross_Combination(colNames=keyCol, features=X_test, OneHot=False)
        assert train_col == test_col
        keyCol = train_col
        features_train_new[keyCol] = train_key[train_col].reset_index()[train_col]
        
    # 利用groupby进行去重
    features_test_or = features_train_new.groupby(keyCol).mean().reset_index()
    
    # 和测试集进行拼接
    features_test_new = pd.merge(test_key, features_test_or, on=keyCol, how='left')
    
    # 删除keyCol列，只保留新衍生的列
    features_test_new.drop([keyCol], axis=1, inplace=True)
    features_train_new.drop([keyCol], axis=1, inplace=True)
    
    # 输出列名称
    colNames_train_new = list(features_train_new.columns)
    colNames_test_new = list(features_test_new.columns)
    
    return features_train_new, features_test_new, colNames_train_new, colNames_test_new



# In[ ]:


def NLP_Group_Stat(X_train,
                   X_test,
                   col_cat, 
                   keyCol=None,
                   tfidf=True, 
                   countVec=True):
    
    """
    NLP特征衍生函数
    
    :param X_train: 训练集特征
    :param X_test: 测试集特征
    :param col_cat: 参与衍生的离散型变量，只能带入多个列
    :param keyCol: 分组参考的关键变量，输入字符串时代表按照单独列分组，输入list代表按照多个列进行分组
    :param tfidf: 是否进行tfidf计算  
    :param countVec: 是否进行CountVectorizer计算

    :return：NLP特征衍生后的新特征和新特征的名称
    """
    
    # 在训练集上进行NLP特征衍生
    features_train_new, colNames_train_new = NLP_Group_Statistics(features = X_train, 
                                                                  col_cat = col_cat, 
                                                                  keyCol = keyCol, 
                                                                  tfidf = tfidf, 
                                                                  countVec = countVec)
    # 如果不分组，则测试集单独计算NLP特征
    if keyCol == None:
        features_test_new, colNames_test_new = NLP_Group_Statistics(features = X_test, 
                                                                    col_cat = col_cat, 
                                                                    keyCol = keyCol, 
                                                                    tfidf = tfidf, 
                                                                    countVec = countVec)
    
    # 否则需要用训练集上统计结果应用于测试集
    else:
        if type(keyCol) == str:
            multi = False
        else:
            multi = True
        features_train_new, features_test_new, colNames_train_new, colNames_test_new = test_features(keyCol = keyCol, 
                                                                                                     X_train = X_train, 
                                                                                                     X_test = X_test, 
                                                                                                     features_train_new = features_train_new,
                                                                                                     multi = multi)
    
    # 如果训练集和测试集衍生特征不一致时
    if colNames_train_new != colNames_test_new:
        features_train_new, features_test_new, colNames_train_new, colNames_test_new = Features_Padding(features_train_new = features_train_new, 
                                                                                                        features_test_new = features_test_new, 
                                                                                                        colNames_train_new = colNames_train_new, 
                                                                                                        colNames_test_new = colNames_test_new)
        
        
    assert colNames_train_new  == colNames_test_new
    return features_train_new, features_test_new, colNames_train_new, colNames_test_new


# In[ ]:


##丢弃全为空值列
train_data = train_data.dropna(axis=1, how="all")
test_data = test_data.dropna(axis=1, how="all")

##丢弃重复值
train_data = train_data.drop_duplicates(subset=['msisdn'])


# In[ ]:


train_data.shape


# In[ ]:


test_data.shape


# In[ ]:


train_data['TCP连接成功率'] = train_data['tcp_conn_succ_times'] / train_data['tcp_conn_req_times'] 
test_data['TCP连接成功率'] = test_data['tcp_conn_succ_times'] / test_data['tcp_conn_req_times'] 

train_data['TCP上行失败率'] = train_data['tcp_ul_conn_fail_times'] / train_data['tcp_conn_req_times'] 
test_data['TCP上行失败率'] = test_data['tcp_ul_conn_fail_times'] / test_data['tcp_conn_req_times'] 

train_data['TCP下行失败率'] = train_data['tcp_dl_conn_fail_times'] / train_data['tcp_conn_req_times'] 
test_data['TCP下行失败率'] = test_data['tcp_dl_conn_fail_times'] / test_data['tcp_conn_req_times'] 

train_data['TCP连接总平均时长'] = train_data['tcp_conn_total_delay'] / train_data['tcp_conn_delay_stat_times'] 
test_data['TCP连接总平均时长'] = test_data['tcp_conn_total_delay'] / test_data['tcp_conn_delay_stat_times'] 

train_data['TCP上行RTT平均时延'] = train_data['tcp_ul_rtt_total_delay'] / train_data['tcp_ul_rtt_stat_times'] 
test_data['TCP上行RTT平均时延'] = test_data['tcp_ul_rtt_total_delay'] / test_data['tcp_ul_rtt_stat_times'] 

train_data['TCP下行RTT平均时延'] = train_data['tcp_dl_rtt_total_delay'] / train_data['tcp_dl_rtt_stat_times'] 
test_data['TCP下行RTT平均时延'] = test_data['tcp_dl_rtt_total_delay'] / test_data['tcp_dl_rtt_stat_times'] 

train_data['TCP RTT总次数'] = train_data['tcp_ul_rtt_stat_times'] + train_data['tcp_dl_rtt_stat_times'] 
test_data['TCP RTT总次数'] = test_data['tcp_ul_rtt_stat_times'] + test_data['tcp_dl_rtt_stat_times'] 

train_data['TCP RTT总时延'] = train_data['tcp_ul_rtt_total_delay'] + train_data['tcp_dl_rtt_total_delay'] 
test_data['TCP RTT总时延'] = test_data['tcp_ul_rtt_total_delay'] + test_data['tcp_dl_rtt_total_delay'] 

train_data['TCP RTT平均时延'] = train_data['TCP RTT总时延'] / train_data['TCP RTT总次数'] 
test_data['TCP RTT平均时延'] = test_data['TCP RTT总时延'] / test_data['TCP RTT总次数'] 

train_data['TCP乱序总包数'] = train_data['tcp_ul_disord_packet_num']+ train_data['tcp_dl_disord_packet_num'] 
test_data['TCP乱序总包数'] = test_data['tcp_ul_disord_packet_num']+ test_data['tcp_dl_disord_packet_num'] 

train_data['TCP重传总包数'] = train_data['tcp_ul_retrans_packet_num']+ train_data['tcp_dl_retrans_packet_num'] 
test_data['TCP重传总包数'] = test_data['tcp_ul_retrans_packet_num']+ test_data['tcp_dl_retrans_packet_num'] 

train_data['TCP总包数'] = train_data['tcp_ul_packet_num']+ train_data['tcp_dl_packet_num'] 
test_data['TCP总包数'] = test_data['tcp_ul_packet_num']+ test_data['tcp_dl_packet_num'] 


train_data['TCP乱序总比例'] = train_data['TCP乱序总包数'] / train_data['TCP总包数'] 
test_data['TCP乱序总比例'] = test_data['TCP乱序总包数'] / test_data['TCP总包数'] 

train_data['TCP上行乱序包比例'] = train_data['tcp_ul_disord_packet_num'] / train_data['tcp_ul_packet_num'] 
test_data['TCP上行乱序包比例'] = test_data['tcp_ul_disord_packet_num'] / test_data['tcp_ul_packet_num'] 

train_data['TCP下行乱序包比例'] = train_data['tcp_dl_disord_packet_num'] / train_data['tcp_dl_packet_num'] 
test_data['TCP下行乱序包比例'] = test_data['tcp_dl_disord_packet_num'] / test_data['tcp_dl_packet_num'] 

train_data['TCP重传总比例'] = train_data['TCP重传总包数'] / train_data['TCP总包数'] 
test_data['TCP重传总比例'] = test_data['TCP重传总包数'] / test_data['TCP总包数'] 

train_data['TCP上行重传比例'] = train_data['tcp_dl_retrans_packet_num'] / train_data['tcp_dl_packet_num'] 
test_data['TCP上行重传比例'] = test_data['tcp_dl_retrans_packet_num'] / test_data['tcp_dl_packet_num'] 

train_data['TCP重传次数比例'] = train_data['tcp_retrans_packet_num'] / train_data['tcp_conn_req_times'] 
test_data['TCP重传次数比例'] = test_data['tcp_retrans_packet_num'] / test_data['tcp_conn_req_times'] 

train_data['TCP连接建立超时比例'] = train_data['tcp_conn_delay_long_times'] / train_data['tcp_conn_req_times'] 
test_data['TCP连接建立超时比例'] = test_data['tcp_conn_delay_long_times'] / test_data['tcp_conn_req_times'] 

train_data['TCP重传比例低总数'] = train_data['tcp_ul_retrans_ratio_low_times']+train_data['tcp_dl_retrans_ratio_low_times'] 
test_data['TCP重传比例低总数'] = test_data['tcp_ul_retrans_ratio_low_times']+test_data['tcp_dl_retrans_ratio_low_times'] 

train_data['TCP重传比例低比例'] = train_data['TCP重传比例低总数'] / train_data['tcp_conn_req_times'] 
test_data['TCP重传比例低比例'] = test_data['TCP重传比例低总数'] / test_data['tcp_conn_req_times'] 

train_data['TCP上行重传比例低比例'] = train_data['tcp_ul_retrans_ratio_low_times'] / train_data['tcp_conn_req_times'] 
test_data['TCP上行重传比例低比例'] = test_data['tcp_ul_retrans_ratio_low_times'] / test_data['tcp_conn_req_times'] 

train_data['TCP下行重传比例低比例'] = train_data['tcp_dl_retrans_ratio_low_times'] / train_data['tcp_conn_req_times'] 
test_data['TCP下行重传比例低比例'] = test_data['tcp_dl_retrans_ratio_low_times'] / test_data['tcp_conn_req_times'] 

train_data['TCP RTT平均时延大于门限总次数'] = train_data['tcp_ul_avg_rtt_long_times']+ train_data['tcp_dl_avg_rtt_long_times'] 
test_data['TCP RTT平均时延大于门限总次数'] = test_data['tcp_ul_avg_rtt_long_times']+ test_data['tcp_dl_avg_rtt_long_times'] 

train_data['TCP RTT平均时延大于门限总比例'] = train_data['TCP RTT平均时延大于门限总次数'] / train_data['TCP RTT总次数'] 
test_data['TCP RTT平均时延大于门限总比例'] = test_data['TCP RTT平均时延大于门限总次数'] / test_data['TCP RTT总次数'] 

train_data['TCP RTT上行平均时延大于门限比例'] = train_data['tcp_ul_avg_rtt_long_times'] / train_data['TCP RTT总次数'] 
test_data['TCP RTT上行平均时延大于门限比例'] = test_data['tcp_ul_avg_rtt_long_times'] / test_data['TCP RTT总次数'] 

train_data['TCP RTT下行平均时延大于门限比例'] = train_data['tcp_dl_avg_rtt_long_times'] / train_data['TCP RTT总次数'] 
test_data['TCP RTT下行平均时延大于门限比例'] = test_data['tcp_dl_avg_rtt_long_times'] / test_data['TCP RTT总次数'] 

train_data['用户面异常比例'] = train_data['total_user_abnormal_times'] / train_data['total_user_times'] 
test_data['用户面异常比例'] = test_data['total_user_abnormal_times'] / test_data['total_user_times'] 

train_data['HTTP业务总流量'] = train_data['http_ul_traffic'] + train_data['http_dl_traffic'] 
test_data['HTTP业务总流量'] = test_data['http_ul_traffic'] + test_data['http_dl_traffic'] 

train_data['HTTP事务响应成功率'] = train_data['http_rsp_succ_times'] / train_data['http_req_times'] 
test_data['HTTP事务响应成功率'] = test_data['http_rsp_succ_times'] / test_data['http_req_times'] 

train_data['HTTP事务响应失败率'] = train_data['http_rsp_fail_times'] / train_data['http_req_times'] 
test_data['HTTP事务响应失败率'] = test_data['http_rsp_fail_times'] / test_data['http_req_times'] 

train_data['HTTP事务响应平均时延'] = train_data['http_rsp_total_delay'] / train_data['http_req_times'] 
test_data['HTTP事务响应平均时延'] = test_data['http_rsp_total_delay'] / test_data['http_req_times'] 

train_data['HTTP事务成功响应平均时延'] = train_data['http_rsp_total_delay'] / train_data['http_rsp_succ_times'] 
test_data['HTTP事务成功响应平均时延'] = test_data['http_rsp_total_delay'] / test_data['http_rsp_succ_times'] 

train_data['HTTP事务大流量包平均下载时长'] = train_data['http_dl_big_packet_total_traffic'] / train_data['http_dl_big_packet_total_delay'] 
test_data['HTTP事务大流量包平均下载时长'] = test_data['http_dl_big_packet_total_traffic'] / test_data['http_dl_big_packet_total_delay'] 

train_data['HTTP事务大流量包下载速率低于阈值比例'] = train_data['http_dl_big_packet_thrput_low_times'] / train_data['http_dl_big_packet_thrput_stat_times'] 
test_data['HTTP事务大流量包下载速率低于阈值比例'] = test_data['http_dl_big_packet_thrput_low_times'] / test_data['http_dl_big_packet_thrput_stat_times'] 

train_data['HTTP业务TCP RTT总时延'] = train_data['http_tcp_ul_rtt_total_delay'] +train_data['http_tcp_dl_rtt_total_delay'] 
test_data['HTTP业务TCP RTT总时延'] = test_data['http_tcp_ul_rtt_total_delay'] +test_data['http_tcp_dl_rtt_total_delay'] 

train_data['HTTP业务TCP RTT总次数'] = train_data['http_tcp_ul_rtt_stat_times'] + train_data['http_tcp_dl_rtt_stat_times'] 
test_data['HTTP业务TCP RTT总次数'] = test_data['http_tcp_ul_rtt_stat_times'] + test_data['http_tcp_dl_rtt_stat_times'] 

train_data['HTTP业务TCP RTT平均时延'] = train_data['HTTP业务TCP RTT总时延'] / train_data['HTTP业务TCP RTT总次数'] 
test_data['HTTP业务TCP RTT平均时延'] = test_data['HTTP业务TCP RTT总时延'] / test_data['HTTP业务TCP RTT总次数'] 

train_data['HTTP业务上行TCP RTT平均时延'] = train_data['http_tcp_ul_rtt_total_delay'] / train_data['http_tcp_ul_rtt_stat_times'] 
test_data['HTTP业务上行TCP RTT平均时延'] = test_data['http_tcp_ul_rtt_total_delay'] / test_data['http_tcp_ul_rtt_stat_times'] 

train_data['HTTP业务下行TCP RTT平均时延'] = train_data['http_tcp_dl_rtt_total_delay'] / train_data['http_tcp_dl_rtt_stat_times'] 
test_data['HTTP业务下行TCP RTT平均时延'] = test_data['http_tcp_dl_rtt_total_delay'] / test_data['http_tcp_dl_rtt_stat_times'] 

train_data['HTTP业务TCP连接建立总时长'] = train_data['http_tcp_ul_conn_total_delay'] + train_data['http_tcp_dl_conn_total_delay'] 
test_data['HTTP业务TCP连接建立总时长'] = test_data['http_tcp_ul_conn_total_delay'] + test_data['http_tcp_dl_conn_total_delay'] 

train_data['HTTP事务大流量包总流量'] = train_data['http_dl_big_packet_total_traffic'] + train_data['http_ul_big_packet_total_traffic'] 
test_data['HTTP事务大流量包总流量'] = test_data['http_dl_big_packet_total_traffic'] + test_data['http_ul_big_packet_total_traffic'] 

train_data['HTTP事务大流量包总时长'] = train_data['http_ul_big_packet_total_delay'] + train_data['http_dl_big_packet_total_delay'] 
test_data['HTTP事务大流量包总时长'] = test_data['http_ul_big_packet_total_delay'] + test_data['http_dl_big_packet_total_delay'] 

train_data['HTTP事务大流量包平均上传时长'] = train_data['http_ul_big_packet_total_traffic'] / train_data['http_ul_big_packet_total_delay'] 
test_data['HTTP事务大流量包平均上传时长'] = test_data['http_ul_big_packet_total_traffic'] / test_data['http_ul_big_packet_total_delay'] 

train_data['HTTP事务大流量包总平均时长'] = train_data['HTTP事务大流量包总流量'] / train_data['HTTP事务大流量包总时长'] 
test_data['HTTP事务大流量包总平均时长'] = test_data['HTTP事务大流量包总流量'] / test_data['HTTP事务大流量包总时长'] 

train_data['HTTPS业务总流量'] = train_data['https_ul_traffic'] + train_data['https_dl_traffic'] 
test_data['HTTPS业务总流量'] = test_data['https_ul_traffic'] + test_data['https_dl_traffic'] 

train_data['HTTPS业务平均流量'] = train_data['HTTPS业务总流量'] / train_data['https_service_times'] 
test_data['HTTPS业务平均流量'] = test_data['HTTPS业务总流量'] / test_data['https_service_times'] 

train_data['HTTPS上行业务次数'] = train_data['https_service_times'] - train_data['https_dl_service_times'] 
test_data['HTTPS上行业务次数'] = test_data['https_service_times'] - test_data['https_dl_service_times'] 

train_data['HTTS上行业务平均流量'] = train_data['https_ul_traffic'] / train_data['HTTPS上行业务次数'] 
test_data['HTTS上行业务平均流量'] = test_data['https_ul_traffic'] / test_data['HTTPS上行业务次数'] 

train_data['HTTS下行业务平均流量'] = train_data['https_dl_traffic'] / train_data['https_dl_service_times'] 
test_data['HTTS下行业务平均流量'] = test_data['https_dl_traffic'] / test_data['https_dl_service_times'] 

train_data['HTTPS上行TCP建立成功率'] = train_data['http_tcp_ul_conn_succ_times'] / train_data['https_tcp_conn_req_times'] 
test_data['HTTPS上行TCP建立成功率'] = test_data['http_tcp_ul_conn_succ_times'] / test_data['https_tcp_conn_req_times'] 

train_data['HTTPs下行TCP建立成功率'] = train_data['http_tcp_dl_conn_succ_times'] / train_data['https_tcp_conn_req_times'] 
test_data['HTTPs下行TCP建立成功率'] = test_data['http_tcp_dl_conn_succ_times'] / test_data['https_tcp_conn_req_times'] 

train_data['HTTPS业务总成功次数'] = train_data['http_tcp_ul_conn_succ_times'] + train_data['http_tcp_dl_conn_succ_times'] 
test_data['HTTPS业务总成功次数'] = test_data['http_tcp_ul_conn_succ_times'] + test_data['http_tcp_dl_conn_succ_times'] 

train_data['HTTPS业务总成功率'] = train_data['HTTPS业务总成功次数'] / train_data['https_tcp_conn_req_times'] 
test_data['HTTPS业务总成功率'] = test_data['HTTPS业务总成功次数'] / test_data['https_tcp_conn_req_times'] 

train_data['HTTP大页面下载平均时长'] = train_data['http_dl_big_page_total_traffic'] / train_data['http_dl_big_page_total_delay'] 
test_data['HTTP大页面下载平均时长'] = test_data['http_dl_big_page_total_traffic'] / test_data['http_dl_big_page_total_delay'] 

train_data['HTTP页面响应成功率'] = train_data['http_page_rsp_succ_times'] / train_data['http_page_req_times'] 
test_data['HTTP页面响应成功率'] = test_data['http_page_rsp_succ_times'] / test_data['http_page_req_times'] 

train_data['HTTP页面响应失败率'] = train_data['http_page_rsp_fail_times'] / train_data['http_page_req_times'] 
test_data['HTTP页面响应失败率'] = test_data['http_page_rsp_fail_times'] / test_data['http_page_req_times'] 

train_data['HTTP页面响应平均时延_1'] = train_data['http_page_rsp_total_delay'] / train_data['http_page_req_times'] 
test_data['HTTP页面响应平均时延_1'] = test_data['http_page_rsp_total_delay'] / test_data['http_page_req_times'] 

train_data['HTTP页面响应平均时延_2'] = train_data['http_page_rsp_total_delay'] / train_data['http_page_rsp_succ_times'] 
test_data['HTTP页面响应平均时延_2'] = test_data['http_page_rsp_total_delay'] / test_data['http_page_rsp_succ_times'] 

train_data['HTTP业务TCP建立失败次数'] = train_data['http_tcp_ul_conn_fail_times'] + train_data['http_tcp_dl_conn_fail_times'] 
test_data['HTTP业务TCP建立失败次数'] = test_data['http_tcp_ul_conn_fail_times'] + test_data['http_tcp_dl_conn_fail_times'] 

train_data['HTTP业务异常次数'] = train_data['http_tcp_ul_conn_fail_times'] + train_data['http_tcp_dl_conn_fail_times'] + train_data['http_tcp_conn_delay_long_times']+ train_data['http_tcp2fsttrans_delay_long_times']+ train_data['http_fstpkt_delay_long_times']+ train_data['http_ul_big_packet_thrput_low_times']
test_data['HTTP业务异常次数'] = test_data['http_tcp_ul_conn_fail_times'] + test_data['http_tcp_dl_conn_fail_times'] + test_data['http_tcp_conn_delay_long_times']+ test_data['http_tcp2fsttrans_delay_long_times']+ test_data['http_fstpkt_delay_long_times']+ test_data['http_ul_big_packet_thrput_low_times']

train_data['HTTP业务大流量包'] = train_data['http_ul_big_packet_num'] + train_data['http_dl_big_packet_num'] 
test_data['HTTP业务大流量包'] = test_data['http_ul_big_packet_num'] + test_data['http_dl_big_packet_num'] 

train_data['HTTPS业务TCP连接成功率'] = train_data['https_tcp_conn_succ_times'] / train_data['https_tcp_conn_req_times'] 
test_data['HTTPS业务TCP连接成功率'] = test_data['https_tcp_conn_succ_times'] / test_data['https_tcp_conn_req_times'] 

train_data['HTTPS业务TCP连接失败总数'] = train_data['https_tcp_ul_conn_fail_times'] +train_data['https_tcp_dl_conn_fail_times'] 
test_data['HTTPS业务TCP连接失败总数'] = test_data['https_tcp_ul_conn_fail_times'] +test_data['https_tcp_dl_conn_fail_times'] 

train_data['HTTPS业务TCP连接失败率'] = train_data['HTTPS业务TCP连接失败总数'] / train_data['https_tcp_conn_req_times'] 
test_data['HTTPS业务TCP连接失败率'] = test_data['HTTPS业务TCP连接失败总数'] / test_data['https_tcp_conn_req_times'] 

train_data['HTTPS业务上行TCP连接失败率'] = train_data['https_tcp_ul_conn_fail_times'] / train_data['https_tcp_conn_req_times'] 
test_data['HTTPS业务上行TCP连接失败率'] = test_data['https_tcp_ul_conn_fail_times'] / test_data['https_tcp_conn_req_times'] 

train_data['HTTPS业务下行TCP连接失败率'] = train_data['https_tcp_dl_conn_fail_times'] / train_data['https_tcp_conn_req_times'] 
test_data['HTTPS业务下行TCP连接失败率'] = test_data['https_tcp_dl_conn_fail_times'] / test_data['https_tcp_conn_req_times'] 

train_data['HTTPS业务TCP建链平均时延'] = train_data['https_tcp_conn_total_delay'] / train_data['https_tcp_conn_delay_stat_times'] 
test_data['HTTPS业务TCP建链平均时延'] = test_data['https_tcp_conn_total_delay'] / test_data['https_tcp_conn_delay_stat_times'] 

train_data['HTTPS业务TCP RTT总时延'] = train_data['https_tcp_ul_rtt_total_delay'] + train_data['https_tcp_dl_rtt_total_delay'] 
test_data['HTTPS业务TCP RTT总时延'] = test_data['https_tcp_ul_rtt_total_delay'] + test_data['https_tcp_dl_rtt_total_delay'] 

train_data['HTTPS业务TCP RTT总次数'] = train_data['https_tcp_ul_rtt_stat_times'] + train_data['https_tcp_dl_rtt_stat_times'] 
test_data['HTTPS业务TCP RTT总次数'] = test_data['https_tcp_ul_rtt_stat_times'] + test_data['https_tcp_dl_rtt_stat_times'] 

train_data['HTTPS业务TCP RTT平均时延'] = train_data['HTTPS业务TCP RTT总时延'] / train_data['HTTPS业务TCP RTT总次数'] 
test_data['HTTPS业务TCP RTT平均时延'] = test_data['HTTPS业务TCP RTT总时延'] / test_data['HTTPS业务TCP RTT总次数'] 

train_data['HTTPS上行业务TCP RTT平均时延'] = train_data['https_tcp_ul_rtt_total_delay'] / train_data['https_tcp_ul_rtt_stat_times'] 
test_data['HTTPS上行业务TCP RTT平均时延'] = test_data['https_tcp_ul_rtt_total_delay'] / test_data['https_tcp_ul_rtt_stat_times'] 

train_data['HTTPS下行业务TCP RTT平均时延'] = train_data['https_tcp_dl_rtt_total_delay'] / train_data['https_tcp_dl_rtt_stat_times'] 
test_data['HTTPS下行业务TCP RTT平均时延'] = test_data['https_tcp_dl_rtt_total_delay'] / test_data['https_tcp_dl_rtt_stat_times'] 

train_data['HTTPS业务TCP连接建立超时次数占比'] = train_data['https_tcp_conn_delay_long_times'] / train_data['https_tcp_conn_delay_stat_times'] 
test_data['HTTPS业务TCP连接建立超时次数占比'] = test_data['https_tcp_conn_delay_long_times'] / test_data['https_tcp_conn_delay_stat_times'] 

train_data['HTTPS业务TCP建立到首事务时延超大次数占比'] = train_data['https_tcp2fsttrans_delay_long_times'] / train_data['https_tcp_conn_delay_stat_times'] 
test_data['HTTPS业务TCP建立到首事务时延超大次数占比'] = test_data['https_tcp2fsttrans_delay_long_times'] / test_data['https_tcp_conn_delay_stat_times'] 

train_data['HTTPS业务首包时延超大次数占比'] = train_data['https_fstpkt_delay_long_times'] / train_data['https_tcp_conn_delay_stat_times'] 
test_data['HTTPS业务首包时延超大次数占比'] = test_data['https_fstpkt_delay_long_times'] / test_data['https_tcp_conn_delay_stat_times'] 

train_data['HTTPS业务连接失败占比'] = train_data['https_conn_fail_times'] / train_data['https_tcp_conn_delay_stat_times'] 
test_data['HTTPS业务连接失败占比'] = test_data['https_conn_fail_times'] / test_data['https_tcp_conn_delay_stat_times'] 

train_data['HTTPS业务大流量包速率低于阈值总次数'] = train_data['https_dl_big_packet_thrput_low_times'] + train_data['https_ul_big_packet_thrput_low_times'] 
test_data['HTTPS业务大流量包速率低于阈值总次数'] = test_data['https_dl_big_packet_thrput_low_times'] + test_data['https_ul_big_packet_thrput_low_times'] 

train_data['视频业务总流量'] = train_data['video_ul_traffic'] + train_data['video_dl_traffic'] 
test_data['视频业务总流量'] = test_data['video_ul_traffic'] + test_data['video_dl_traffic'] 

train_data['视频业务高清视频总流量'] = train_data['video_hd_ul_traffic'] + train_data['video_hd_dl_traffic'] 
test_data['视频业务高清视频总流量'] = test_data['video_hd_ul_traffic'] + test_data['video_hd_dl_traffic'] 

train_data['视频业务平均流量'] = train_data['视频业务总流量'] / train_data['video_xdr_count'] 
test_data['视频业务平均流量'] = test_data['视频业务总流量'] / test_data['video_xdr_count'] 


train_data['视频业务高清视频业务占比'] = train_data['视频业务高清视频总流量'] / train_data['视频业务总流量'] 
test_data['视频业务高清视频业务占比'] = test_data['视频业务高清视频总流量'] / test_data['视频业务总流量'] 

train_data['视频业务平均上行流量'] = train_data['video_ul_traffic'] / train_data['video_xdr_count'] 
test_data['视频业务平均上行流量'] = test_data['video_ul_traffic'] / test_data['video_xdr_count'] 

train_data['视频业务平均下行流量'] = train_data['video_dl_traffic'] / train_data['video_xdr_count'] 
test_data['视频业务平均下行流量'] = test_data['video_dl_traffic'] / test_data['video_xdr_count'] 

train_data['视频业务初始缓冲成功率'] = train_data['video_intbuffer_succ_times'] / train_data['video_intbuffer_req_times'] 
test_data['视频业务初始缓冲成功率'] = test_data['video_intbuffer_succ_times'] / test_data['video_intbuffer_req_times'] 

train_data['视频业务初始缓冲平均时长_1'] = train_data['video_intbuffer_suc_delay'] / train_data['video_intbuffer_req_times'] 
test_data['视频业务初始缓冲平均时长_1'] = test_data['video_intbuffer_suc_delay'] / test_data['video_intbuffer_req_times'] 

train_data['视频业务初始缓冲平均时长_2'] = train_data['video_intbuffer_suc_delay'] / train_data['video_intbuffer_succ_times'] 
test_data['视频业务初始缓冲平均时长_2'] = test_data['video_intbuffer_suc_delay'] / test_data['video_intbuffer_succ_times'] 

train_data['视频业务平均下载时长'] = train_data['video_dl_delay'] / train_data['video_dl_packets'] 
test_data['视频业务平均下载时长'] = test_data['video_dl_delay'] / test_data['video_dl_packets'] 

train_data['视频业务停顿时长占比'] = train_data['video_stall_duration'] / train_data['video_play_duration'] 
test_data['视频业务停顿时长占比'] = test_data['video_stall_duration'] / test_data['video_play_duration'] 

train_data['视频业务停顿平均时长'] = train_data['video_stall_duration'] / train_data['video_stall_num'] 
test_data['视频业务停顿平均时长'] = test_data['video_stall_duration'] / test_data['video_stall_num'] 

train_data['视频业务TCP RTT总时延'] = train_data['video_tcp_ul_rtt_total_delay'] + train_data['video_tcp_dl_rtt_total_delay'] 
test_data['视频业务TCP RTT总时延'] = test_data['video_tcp_ul_rtt_total_delay'] + test_data['video_tcp_dl_rtt_total_delay'] 

train_data['视频业务TCP RTT总次数'] = train_data['video_tcp_ul_rtt_stat_times'] / train_data['video_tcp_dl_rtt_stat_times'] 
test_data['视频业务TCP RTT总次数'] = test_data['video_tcp_ul_rtt_stat_times'] / test_data['video_tcp_dl_rtt_stat_times'] 

train_data['视频业务TCP RTT 平均时延'] = train_data['视频业务TCP RTT总时延'] / train_data['视频业务TCP RTT总次数'] 
test_data['视频业务TCP RTT 平均时延'] = test_data['视频业务TCP RTT总时延'] / test_data['视频业务TCP RTT总次数'] 

train_data['视频业务TCP 上行RTT平均时延'] = train_data['video_tcp_ul_rtt_total_delay'] / train_data['video_tcp_ul_rtt_stat_times'] 
test_data['视频业务TCP 上行RTT平均时延'] = test_data['video_tcp_ul_rtt_total_delay'] / test_data['video_tcp_ul_rtt_stat_times'] 

train_data['视频业务TCP 下行RTT平均时延'] = train_data['video_tcp_dl_rtt_total_delay'] / train_data['video_tcp_dl_rtt_stat_times'] 
test_data['视频业务TCP 下行RTT平均时延'] = test_data['video_tcp_dl_rtt_total_delay'] / test_data['video_tcp_dl_rtt_stat_times'] 

train_data['流媒体业务速率低于门限占比'] = train_data['video_dl_thrput_low_times'] / train_data['video_dl_thrput_codecrate_stat_times'] 
test_data['流媒体业务速率低于门限占比'] = test_data['video_dl_thrput_low_times'] / test_data['video_dl_thrput_codecrate_stat_times'] 

train_data['流媒体业务速率码率比大于阈值占比'] = train_data['video_dl_thrput_codecrate_good_times'] / train_data['video_dl_thrput_codecrate_stat_times'] 
test_data['流媒体业务速率码率比大于阈值占比'] = test_data['video_dl_thrput_codecrate_good_times'] / test_data['video_dl_thrput_codecrate_stat_times'] 

train_data['视频业务平均时长'] = train_data['video_total_dura'] / train_data['video_xdr_count'] 
test_data['视频业务平均时长'] = test_data['video_total_dura'] / test_data['video_xdr_count'] 

train_data['视频_1080P时长占比'] = train_data['video_delay_1080'] / train_data['video_total_dura'] 
test_data['视频_1080P时长占比'] = test_data['video_delay_1080'] / test_data['video_total_dura'] 

train_data['视频_1080P平均下载时长'] = train_data['video_dl_packets_1080'] / train_data['video_dl_delay_1080'] 
test_data['视频_1080P平均下载时长'] = test_data['video_dl_packets_1080'] / test_data['video_dl_delay_1080'] 

train_data['视频_1080P卡顿占比'] = train_data['video_stall_num_1080'] / train_data['video_intbuffer_req_times_1080'] 
test_data['视频_1080P卡顿占比'] = test_data['video_stall_num_1080'] / test_data['video_intbuffer_req_times_1080'] 

train_data['视频_1080P播放成功占比'] = train_data['video_intbuffer_succ_times_1080'] / train_data['video_intbuffer_req_times_1080'] 
test_data['视频_1080P播放成功占比'] = test_data['video_intbuffer_succ_times_1080'] / test_data['video_intbuffer_req_times_1080'] 

train_data['视频业务平均下载时长'] = train_data['video_dl_packets_valid'] / train_data['video_dl_delay_valid'] 
test_data['视频业务平均下载时长'] = test_data['video_dl_packets_valid'] / test_data['video_dl_delay_valid'] 

train_data['IM业务TCP连接占比'] = train_data['im_tcp_conn_req_times'] / train_data['im_xdr_count'] 
test_data['IM业务TCP连接占比'] = test_data['im_tcp_conn_req_times'] / test_data['im_xdr_count'] 

train_data['IM业务TCP连接成功率'] = train_data['im_tcp_conn_succ_times'] / train_data['im_tcp_conn_req_times'] 
test_data['IM业务TCP连接成功率'] = test_data['im_tcp_conn_succ_times'] / test_data['im_tcp_conn_req_times'] 

train_data['IM业务TCP建立失败总次数'] = train_data['im_tcp_ul_conn_fail_times'] + train_data['im_tcp_dl_conn_fail_times'] 
test_data['IM业务TCP建立失败总次数'] = test_data['im_tcp_ul_conn_fail_times'] + test_data['im_tcp_dl_conn_fail_times'] 

train_data['IM业务TCP上行建立失败率'] = train_data['im_tcp_ul_conn_fail_times'] / train_data['im_tcp_conn_req_times'] 
test_data['IM业务TCP上行建立失败率'] = test_data['im_tcp_ul_conn_fail_times'] / test_data['im_tcp_conn_req_times'] 

train_data['IM业务TCP下行建立失败率'] = train_data['im_tcp_dl_conn_fail_times'] / train_data['im_tcp_conn_req_times'] 
test_data['IM业务TCP下行建立失败率'] = test_data['im_tcp_dl_conn_fail_times'] / test_data['im_tcp_conn_req_times'] 

train_data['IM业务TCP连接建立平均时长_1'] = train_data['im_tcp_conn_total_delay'] / train_data['im_tcp_conn_req_times'] 
test_data['IM业务TCP连接建立平均时长_1'] = test_data['im_tcp_conn_total_delay'] / test_data['im_tcp_conn_req_times'] 

train_data['IM业务TCP连接建立平均时长_2'] = train_data['im_tcp_conn_total_delay'] / train_data['im_tcp_conn_succ_times'] 
test_data['IM业务TCP连接建立平均时长_2'] = test_data['im_tcp_conn_total_delay'] / test_data['im_tcp_conn_succ_times'] 

train_data['IM业务总流量'] = train_data['im_ul_traffic'] + train_data['im_dl_traffic'] 
test_data['IM业务总流量'] = test_data['im_ul_traffic'] + test_data['im_dl_traffic'] 

train_data['IM业务TCP RTT总次数'] = train_data['im_tcp_ul_rtt_stat_times'] + train_data['im_tcp_dl_rtt_stat_times'] 
test_data['IM业务TCP RTT总次数'] = test_data['im_tcp_ul_rtt_stat_times'] + test_data['im_tcp_dl_rtt_stat_times'] 

train_data['IM业务TCP RTT总时延'] = train_data['im_tcp_ul_rtt_total_delay'] + train_data['im_tcp_dl_rtt_total_delay'] 
test_data['IM业务TCP RTT总时延'] = test_data['im_tcp_ul_rtt_total_delay'] + test_data['im_tcp_dl_rtt_total_delay'] 

train_data['IM业务TCP RTT平均时延'] = train_data['IM业务TCP RTT总时延'] / train_data['IM业务TCP RTT总次数'] 
test_data['IM业务TCP RTT平均时延'] = test_data['IM业务TCP RTT总时延'] / test_data['IM业务TCP RTT总次数'] 

train_data['IM业务TCP RTT上行平均时延'] = train_data['im_tcp_ul_rtt_total_delay'] / train_data['im_tcp_ul_rtt_stat_times'] 
test_data['IM业务TCP RTT上行平均时延'] = test_data['im_tcp_ul_rtt_total_delay'] / test_data['im_tcp_ul_rtt_stat_times'] 

train_data['IM业务TCP RTT下行平均时延'] = train_data['im_tcp_dl_rtt_stat_times'] / train_data['im_tcp_dl_rtt_total_delay'] 
test_data['IM业务TCP RTT下行平均时延'] = test_data['im_tcp_dl_rtt_stat_times'] / test_data['im_tcp_dl_rtt_total_delay'] 

train_data['IM业务TCP平均RTT大于门限的次数'] = train_data['im_tcp_ul_avg_rtt_long_times'] + train_data['im_tcp_dl_avg_rtt_long_times'] 
test_data['IM业务TCP平均RTT大于门限的次数'] = test_data['im_tcp_ul_avg_rtt_long_times'] + test_data['im_tcp_dl_avg_rtt_long_times'] 

train_data['IM业务TCP平均RTT大于门限占比'] = train_data['IM业务TCP平均RTT大于门限的次数'] / train_data['IM业务TCP RTT总次数'] 
test_data['IM业务TCP平均RTT大于门限占比'] = test_data['IM业务TCP平均RTT大于门限的次数'] / test_data['IM业务TCP RTT总次数'] 

train_data['IM业务TCP平均上行RTT大于门限占比'] = train_data['im_tcp_ul_avg_rtt_long_times'] / train_data['im_tcp_ul_rtt_stat_times'] 
test_data['IM业务TCP平均上行RTT大于门限占比'] = test_data['im_tcp_ul_avg_rtt_long_times'] / test_data['im_tcp_ul_rtt_stat_times'] 

train_data['IM业务TCP平均下行RTT大于门限占比'] = train_data['im_tcp_dl_avg_rtt_long_times'] / train_data['im_tcp_dl_rtt_stat_times'] 
test_data['IM业务TCP平均下行RTT大于门限占比'] = test_data['im_tcp_dl_avg_rtt_long_times'] / test_data['im_tcp_dl_rtt_stat_times'] 

train_data['IM业务登录成功率'] = train_data['im_login_succ_times'] / train_data['im_login_req_times'] 
test_data['IM业务登录成功率'] = test_data['im_login_succ_times'] / test_data['im_login_req_times'] 

train_data['IM业务文本发送成功率'] = train_data['im_sendtext_succ_times'] / train_data['im_sendtext_req_times'] 
test_data['IM业务文本发送成功率'] = test_data['im_sendtext_succ_times'] / test_data['im_sendtext_req_times'] 

train_data['IM业务图片发送成功率'] = train_data['im_sendpic_succ_times'] / train_data['im_sendpic_req_times'] 
test_data['IM业务图片发送成功率'] = test_data['im_sendpic_succ_times'] / test_data['im_sendpic_req_times'] 

train_data['IM业务视频发送成功率'] = train_data['im_sendvideo_succ_times'] / train_data['im_sendvideo_req_times'] 
test_data['IM业务视频发送成功率'] = test_data['im_sendvideo_succ_times'] / test_data['im_sendvideo_req_times'] 

train_data['IM业务上行总记录数'] = train_data['im_tcp_ul_rtt_stat_times_0_30'] + train_data['im_tcp_ul_rtt_stat_times_30_60'] + train_data['im_tcp_ul_rtt_stat_times_larger_60']
test_data['IM业务上行总记录数'] = test_data['im_tcp_ul_rtt_stat_times_0_30'] + test_data['im_tcp_ul_rtt_stat_times_30_60'] + test_data['im_tcp_ul_rtt_stat_times_larger_60']

train_data['IM业务上行RTT时间0到30毫秒XDR占比'] = train_data['im_tcp_ul_rtt_stat_times_0_30'] / train_data['IM业务上行总记录数'] 
test_data['IM业务上行RTT时间0到30毫秒XDR占比'] = test_data['im_tcp_ul_rtt_stat_times_0_30'] / test_data['IM业务上行总记录数'] 

train_data['IM业务上行RTT时间30到60毫秒XDR记录占比'] = train_data['im_tcp_ul_rtt_stat_times_30_60'] / train_data['IM业务上行总记录数'] 
test_data['IM业务上行RTT时间30到60毫秒XDR记录占比'] = test_data['im_tcp_ul_rtt_stat_times_30_60'] / test_data['IM业务上行总记录数'] 

train_data['IM业务上行RTT时间大于60毫秒XDR记录占比'] = train_data['im_tcp_ul_rtt_stat_times_larger_60'] / train_data['IM业务上行总记录数'] 
test_data['IM业务上行RTT时间大于60毫秒XDR记录占比'] = test_data['im_tcp_ul_rtt_stat_times_larger_60'] / test_data['IM业务上行总记录数'] 

train_data['IM业务下行总记录数'] = train_data['im_tcp_dl_rtt_stat_times_0_50'] + train_data['im_tcp_dl_rtt_stat_times_50_150'] + train_data['im_tcp_dl_rtt_stat_times_larger_150']
test_data['IM业务下行总记录数'] = test_data['im_tcp_dl_rtt_stat_times_0_50'] + test_data['im_tcp_dl_rtt_stat_times_50_150'] + test_data['im_tcp_dl_rtt_stat_times_larger_150']

train_data['IM业务下行RTT时间0到50毫秒xdr占比'] = train_data['im_tcp_dl_rtt_stat_times_0_50'] / train_data['IM业务下行总记录数'] 
test_data['IM业务下行RTT时间0到50毫秒xdr占比'] = test_data['im_tcp_dl_rtt_stat_times_0_50'] / test_data['IM业务下行总记录数'] 

train_data['IM业务下行RTT时间50到150毫秒xdr占比'] = train_data['im_tcp_dl_rtt_stat_times_50_150'] / train_data['IM业务下行总记录数'] 
test_data['IM业务下行RTT时间50到150毫秒xdr占比'] = test_data['im_tcp_dl_rtt_stat_times_50_150'] / test_data['IM业务下行总记录数'] 

train_data['IM业务下行RTT时间大于150毫秒xdr占比'] = train_data['im_tcp_dl_rtt_stat_times_larger_150'] / train_data['IM业务下行总记录数'] 
test_data['IM业务下行RTT时间大于150毫秒xdr占比'] = test_data['im_tcp_dl_rtt_stat_times_larger_150'] / test_data['IM业务下行总记录数'] 

train_data['IM业务支付RTT总时延'] = train_data['im_pay_dl_rtt_total_delay'] + train_data['im_pay_ul_rtt_total_delay'] 
test_data['IM业务支付RTT总时延'] = test_data['im_pay_dl_rtt_total_delay'] + test_data['im_pay_ul_rtt_total_delay'] 

train_data['IM业务支付超时次数'] = train_data['im_pay_ul_avg_rtt_long_times'] + train_data['im_pay_dl_avg_rtt_long_times'] 
test_data['IM业务支付超时次数'] = test_data['im_pay_ul_avg_rtt_long_times'] + test_data['im_pay_dl_avg_rtt_long_times'] 


train_data['Game业务TCP连接成功率'] = train_data['game_tcp_conn_succ_times'] / train_data['game_tcp_conn_req_times'] 
test_data['Game业务TCP连接成功率'] = test_data['game_tcp_conn_succ_times'] / test_data['game_tcp_conn_req_times'] 

train_data['Game业务TCP建立失败次数'] = train_data['game_tcp_ul_conn_fail_times'] + train_data['game_tcp_dl_conn_fail_times'] 
test_data['Game业务TCP建立失败次数'] = test_data['game_tcp_ul_conn_fail_times'] + test_data['game_tcp_dl_conn_fail_times'] 

train_data['Game业务TCP建立失败率'] = train_data['Game业务TCP建立失败次数'] / train_data['game_tcp_conn_req_times'] 
test_data['Game业务TCP建立失败率'] = test_data['Game业务TCP建立失败次数'] / test_data['game_tcp_conn_req_times'] 

train_data['Game业务TCP连接建立平均时长_1'] = train_data['game_tcp_conn_total_delay'] / train_data['game_tcp_conn_succ_times'] 
test_data['Game业务TCP连接建立平均时长_1'] = test_data['game_tcp_conn_total_delay'] / test_data['game_tcp_conn_succ_times'] 

train_data['Game业务TCP连接建立平均时长_2'] = train_data['game_tcp_conn_total_delay'] / train_data['game_tcp_conn_req_times'] 
test_data['Game业务TCP连接建立平均时长_2'] = test_data['game_tcp_conn_total_delay'] / test_data['game_tcp_conn_req_times'] 

train_data['Game业务总流量'] = train_data['game_ul_traffic'] + train_data['game_dl_traffic'] 
test_data['Game业务总流量'] = test_data['game_ul_traffic'] + test_data['game_dl_traffic'] 

train_data['Game业务持续平均时长'] = train_data['game_total_dura'] / train_data['game_dura_stat_times'] 
test_data['Game业务持续平均时长'] = test_data['game_total_dura'] / test_data['game_dura_stat_times'] 

train_data['Game业务对战平均时长'] = train_data['game_battle_total_dura'] / train_data['game_battle_stat_times'] 
test_data['Game业务对战平均时长'] = test_data['game_battle_total_dura'] / test_data['game_battle_stat_times'] 

train_data['Game业务对战时长占比'] = train_data['game_battle_total_dura'] / train_data['game_total_dura'] 
test_data['Game业务对战时长占比'] = test_data['game_battle_total_dura'] / test_data['game_total_dura'] 

train_data['Game业务TCP RTT总时延'] = train_data['game_tcp_ul_rtt_total_delay'] + train_data['game_tcp_dl_rtt_total_delay'] 
test_data['Game业务TCP RTT总时延'] = test_data['game_tcp_ul_rtt_total_delay'] + test_data['game_tcp_dl_rtt_total_delay'] 

train_data['Game业务TCP RTT总次数'] = train_data['game_tcp_ul_rtt_stat_times'] + train_data['game_tcp_dl_rtt_stat_times'] 
test_data['Game业务TCP RTT总次数'] = test_data['game_tcp_ul_rtt_stat_times'] + test_data['game_tcp_dl_rtt_stat_times'] 

train_data['Game业务TCP RTT平均时延'] = train_data['Game业务TCP RTT总时延'] / train_data['Game业务TCP RTT总次数'] 
test_data['Game业务TCP RTT平均时延'] = test_data['Game业务TCP RTT总时延'] / test_data['Game业务TCP RTT总次数'] 

train_data['Game业务TCP上行 RTT平均时延'] = train_data['game_tcp_ul_rtt_total_delay'] / train_data['game_tcp_ul_rtt_stat_times'] 
test_data['Game业务TCP上行 RTT平均时延'] = test_data['game_tcp_ul_rtt_total_delay'] / test_data['game_tcp_ul_rtt_stat_times'] 

train_data['Game业务TCP下行 RTT平均时延'] = train_data['game_tcp_dl_rtt_total_delay'] / train_data['game_tcp_dl_rtt_stat_times'] 
test_data['Game业务TCP下行 RTT平均时延'] = test_data['game_tcp_dl_rtt_total_delay'] / test_data['game_tcp_dl_rtt_stat_times'] 

train_data['Game业务上行RTT记录总数'] = train_data['game_tcp_ul_rtt_stat_times_0_30'] + train_data['game_tcp_ul_rtt_stat_times_30_60'] + train_data['game_tcp_ul_rtt_stat_times_larger_60']
test_data['Game业务上行RTT记录总数'] = test_data['game_tcp_ul_rtt_stat_times_0_30'] + test_data['game_tcp_ul_rtt_stat_times_30_60'] + test_data['game_tcp_ul_rtt_stat_times_larger_60']

train_data['Game业务上行RTT时间0到30毫秒XDR记录占比'] = train_data['game_tcp_ul_rtt_stat_times_0_30'] / train_data['Game业务上行RTT记录总数'] 
test_data['Game业务上行RTT时间0到30毫秒XDR记录占比'] = test_data['game_tcp_ul_rtt_stat_times_0_30'] / test_data['Game业务上行RTT记录总数'] 

train_data['Game业务上行RTT时间30到60毫秒XDR记录占比'] = train_data['game_tcp_ul_rtt_stat_times_30_60'] / train_data['Game业务上行RTT记录总数'] 
test_data['Game业务上行RTT时间30到60毫秒XDR记录占比'] = test_data['game_tcp_ul_rtt_stat_times_30_60'] / test_data['Game业务上行RTT记录总数'] 

train_data['Game业务上行RTT时间大于60毫秒XDR记录占比'] = train_data['game_tcp_ul_rtt_stat_times_larger_60'] / train_data['Game业务上行RTT记录总数'] 
test_data['Game业务上行RTT时间大于60毫秒XDR记录占比'] = test_data['game_tcp_ul_rtt_stat_times_larger_60'] / test_data['Game业务上行RTT记录总数'] 

train_data['Game业务下行RTT记录数'] = train_data['game_tcp_dl_rtt_stat_times_0_50'] + train_data['game_tcp_dl_rtt_stat_times_50_150'] + train_data['game_tcp_dl_rtt_stat_times_larger_150']
test_data['Game业务下行RTT记录数'] = test_data['game_tcp_dl_rtt_stat_times_0_50'] + test_data['game_tcp_dl_rtt_stat_times_50_150'] + test_data['game_tcp_dl_rtt_stat_times_larger_150']

train_data['Game业务下行RTT时间0到50毫秒xdr条数占比'] = train_data['game_tcp_dl_rtt_stat_times_0_50'] / train_data['Game业务下行RTT记录数'] 
test_data['Game业务下行RTT时间0到50毫秒xdr条数占比'] = test_data['game_tcp_dl_rtt_stat_times_0_50'] / test_data['Game业务下行RTT记录数'] 

train_data['Game业务下行RTT时间50到150毫秒xdr占比'] = train_data['game_tcp_dl_rtt_stat_times_50_150'] / train_data['Game业务下行RTT记录数'] 
test_data['Game业务下行RTT时间50到150毫秒xdr占比'] = test_data['game_tcp_dl_rtt_stat_times_50_150'] / test_data['Game业务下行RTT记录数'] 

train_data['Game业务下行RTT时间大于150毫秒xdr条数占比'] = train_data['game_tcp_dl_rtt_stat_times_larger_150'] / train_data['Game业务下行RTT记录数'] 
test_data['Game业务下行RTT时间大于150毫秒xdr条数占比'] = test_data['game_tcp_dl_rtt_stat_times_larger_150'] / test_data['Game业务下行RTT记录数'] 

train_data['Game业务UDP平均包间隔总和'] = train_data['game_udp_ul_avg_interval_total'] + train_data['game_udp_dl_avg_interval_total'] 
test_data['Game业务UDP平均包间隔总和'] = test_data['game_udp_ul_avg_interval_total'] + test_data['game_udp_dl_avg_interval_total'] 

train_data['Game业务登录成功率'] = train_data['game_login_succ_times'] / train_data['game_login_req_times'] 
test_data['Game业务登录成功率'] = test_data['game_login_succ_times'] / test_data['game_login_req_times'] 

train_data['Game业务TCPRTT超时次数'] = train_data['game_tcp_ul_avg_rtt_long_times'] + train_data['game_tcp_dl_avg_rtt_long_times'] 
test_data['Game业务TCPRTT超时次数'] = test_data['game_tcp_ul_avg_rtt_long_times'] + test_data['game_tcp_dl_avg_rtt_long_times'] 

train_data['DNS查询成功率'] = train_data['dns_qurey_succ_times'] / train_data['dns_qurey_req_times'] 
test_data['DNS查询成功率'] = test_data['dns_qurey_succ_times'] / test_data['dns_qurey_req_times'] 

train_data['DNS查询失败率'] = train_data['dns_query_fail_times'] / train_data['dns_qurey_req_times'] 
test_data['DNS查询失败率'] = test_data['dns_query_fail_times'] / test_data['dns_qurey_req_times'] 

train_data['DNS查询平均时延_1'] = train_data['dns_qurey_total_delay'] / train_data['dns_qurey_req_times'] 
test_data['DNS查询平均时延_1'] = test_data['dns_qurey_total_delay'] / test_data['dns_qurey_req_times'] 

train_data['DNS查询平均时延_2'] = train_data['dns_qurey_total_delay'] / train_data['dns_qurey_succ_times'] 
test_data['DNS查询平均时延_2'] = test_data['dns_qurey_total_delay'] / test_data['dns_qurey_succ_times'] 

train_data['Game业务UDP平均抖动量总和'] = train_data['game_udp_ul_avg_jitter_total'] + train_data['game_udp_dl_avg_jitter_total'] 
test_data['Game业务UDP平均抖动量总和'] = test_data['game_udp_ul_avg_jitter_total'] + test_data['game_udp_dl_avg_jitter_total'] 

train_data['DNS查询时长超长占比'] = train_data['dns_qurey_delay_beyond_times'] / train_data['dns_qurey_req_times'] 
test_data['DNS查询时长超长占比'] = test_data['dns_qurey_delay_beyond_times'] / test_data['dns_qurey_req_times'] 

train_data['Game业务UDP平均抖动量统计计数'] = train_data['game_udp_ul_avg_jitter_times'] +train_data['game_udp_dl_avg_jitter_times'] 
test_data['Game业务UDP平均抖动量统计计数'] = test_data['game_udp_ul_avg_jitter_times'] +test_data['game_udp_dl_avg_jitter_times'] 

train_data['Game业务UDP平均抖动量'] = train_data['Game业务UDP平均抖动量总和'] / train_data['Game业务UDP平均抖动量统计计数'] 
test_data['Game业务UDP平均抖动量'] = test_data['Game业务UDP平均抖动量总和'] / test_data['Game业务UDP平均抖动量统计计数'] 

train_data['Game业务UDP上行平均抖动量'] = train_data['game_udp_ul_avg_jitter_total'] / train_data['game_udp_ul_avg_jitter_times'] 
test_data['Game业务UDP上行平均抖动量'] = test_data['game_udp_ul_avg_jitter_total'] / test_data['game_udp_ul_avg_jitter_times'] 

train_data['Game业务卡顿局占比'] = train_data['game_stall_times'] / train_data['game_login_succ_times'] 
test_data['Game业务卡顿局占比'] = test_data['game_stall_times'] / test_data['game_login_succ_times'] 

train_data['IM业务平均时长'] = train_data['im_xdr_dura'] / train_data['im_service_succ_times'] 
test_data['IM业务平均时长'] = test_data['im_xdr_dura'] / test_data['im_service_succ_times'] 

train_data['IM业务登录平均时延'] = train_data['im_login_succ_total_delay'] / train_data['im_service_succ_times'] 
test_data['IM业务登录平均时延'] = test_data['im_login_succ_total_delay'] / test_data['im_service_succ_times'] 

train_data['HTTP事务传输平均时长'] = train_data['http_trans_dura'] / train_data['http_tcp_conn_req_times'] 
test_data['HTTP事务传输平均时长'] = test_data['http_trans_dura'] / test_data['http_tcp_conn_req_times'] 

train_data['HTTP业务平均持续时长'] = train_data['http_total_dura'] / train_data['http_tcp_conn_req_times'] 
test_data['HTTP业务平均持续时长'] = test_data['http_total_dura'] / test_data['http_tcp_conn_req_times'] 

train_data['视频业务0级卡顿占比'] = train_data['video_service_level0_stall_times'] / train_data['video_service_succ_times'] 
test_data['视频业务0级卡顿占比'] = test_data['video_service_level0_stall_times'] / test_data['video_service_succ_times'] 

train_data['视频业务1级卡顿占比'] = train_data['video_service_level1_stall_times'] / train_data['video_service_succ_times'] 
test_data['视频业务1级卡顿占比'] = test_data['video_service_level1_stall_times'] / test_data['video_service_succ_times'] 

train_data['视频业务2级卡顿次数'] = train_data['video_service_level2_stall_times'] / train_data['video_service_succ_times'] 
test_data['视频业务2级卡顿次数'] = test_data['video_service_level2_stall_times'] / test_data['video_service_succ_times'] 

train_data['Game业务UDP平均包间隔统计次数'] = train_data['game_udp_ul_avg_interval_times'] + train_data['game_udp_dl_avg_interval_times'] 
test_data['Game业务UDP平均包间隔统计次数'] = test_data['game_udp_ul_avg_interval_times'] + test_data['game_udp_dl_avg_interval_times'] 

train_data['IM业务支付总次数'] = train_data['im_pay_ul_rtt_stat_times'] + train_data['im_pay_dl_rtt_stat_times'] 
test_data['IM业务支付总次数'] = test_data['im_pay_ul_rtt_stat_times'] + test_data['im_pay_dl_rtt_stat_times'] 

train_data['HTTPS业务大流量包流量'] = train_data['https_ul_big_packet_total_traffic'] + train_data['https_dl_big_packet_total_traffic'] 
test_data['HTTPS业务大流量包流量'] = test_data['https_ul_big_packet_total_traffic'] + test_data['https_dl_big_packet_total_traffic'] 

train_data['HTTPS业务大流量包时长'] = train_data['https_ul_big_packet_total_delay'] + train_data['https_dl_big_packet_total_delay'] 
test_data['HTTPS业务大流量包时长'] = test_data['https_ul_big_packet_total_delay'] + test_data['https_dl_big_packet_total_delay'] 

train_data['HTTPS业务大流量包上行平均流量'] = train_data['https_ul_big_packet_total_traffic'] + train_data['https_ul_big_packet_total_delay'] 
test_data['HTTPS业务大流量包上行平均流量'] = test_data['https_ul_big_packet_total_traffic'] + test_data['https_ul_big_packet_total_delay'] 

train_data['平均主叫时长'] = train_data['call_out_dura'] / train_data['call_out_times'] 
test_data['平均主叫时长'] = test_data['call_out_dura'] / test_data['call_out_times'] 

train_data['平均被叫时长'] = train_data['call_in_dura'] / train_data['call_in_times'] 
test_data['平均被叫时长'] = test_data['call_in_dura'] / test_data['call_in_times'] 

train_data['电频统计'] = train_data['under105'] + train_data['under110'] + train_data['under115']
test_data['电频统计'] = test_data['under105'] + test_data['under110'] + test_data['under115']

train_data['电频小于-105占比'] = train_data['under105'] / train_data['电频统计'] 
test_data['电频小于-105占比'] = test_data['under105'] / test_data['电频统计'] 

train_data['电频小于-110占比'] = train_data['under110'] / train_data['电频统计'] 
test_data['电频小于-110占比'] = test_data['under110'] / test_data['电频统计'] 

train_data['电频小于-115占比'] = train_data['under115'] / train_data['电频统计'] 
test_data['电频小于-115占比'] = test_data['under115'] / test_data['电频统计'] 


# In[ ]:


train_data['date']= pd.to_datetime(train_data['open_date'].astype(str))
train_data['date2']= pd.to_datetime("2022-07-01")
train_data['在网日期'] = train_data['date2'] - train_data['date']
train_data['在网日期'] = train_data['在网日期'].astype(str)
train_data['在网日期'] = train_data['在网日期'].apply(lambda x:x[:-5])
train_data['在网日期'] = train_data['在网日期'].astype('int64')
train_data = train_data.drop(['date','date2'], axis=1)


test_data['date']= pd.to_datetime(test_data['open_date'].astype(str))
test_data['date2']= pd.to_datetime("2022-07-01")
test_data['在网日期'] = test_data['date2'] - test_data['date']
test_data['在网日期'] = test_data['在网日期'].astype(str)
test_data['在网日期'] = test_data['在网日期'].apply(lambda x:x[:-5])
test_data['在网日期'] = test_data['在网日期'].astype('int64')
test_data = test_data.drop(['date','date2'], axis=1)



# In[ ]:


print(train_data['在网日期'].max())


# In[ ]:


combine=[train_data]
for dataset in combine:
    dataset.loc[dataset['在网日期']<=90,'datagroup']='1'
    dataset.loc[(dataset['在网日期'] > 90) & (dataset['在网日期'] <= 365), 'datagroup'] = '2'
    dataset.loc[(dataset['在网日期'] > 365) & (dataset['在网日期'] <= 730), 'datagroup'] = '3'
    dataset.loc[(dataset['在网日期'] > 730) & (dataset['在网日期'] <= 1095), 'datagroup'] = '4'
    dataset.loc[(dataset['在网日期'] > 1095) & (dataset['在网日期'] <= 1825), 'datagroup'] = '5'
    dataset.loc[ dataset['在网日期'] > 1825, 'datagroup'] = '6'


# In[ ]:


combine=[test_data]
for dataset in combine:
    dataset.loc[dataset['在网日期']<=90,'datagroup']='1'
    dataset.loc[(dataset['在网日期'] > 90) & (dataset['在网日期'] <= 365), 'datagroup'] = '2'
    dataset.loc[(dataset['在网日期'] > 365) & (dataset['在网日期'] <= 730), 'datagroup'] = '3'
    dataset.loc[(dataset['在网日期'] > 730) & (dataset['在网日期'] <= 1095), 'datagroup'] = '4'
    dataset.loc[(dataset['在网日期'] > 1095) & (dataset['在网日期'] <= 1825), 'datagroup'] = '5'
    dataset.loc[ dataset['在网日期'] > 1825, 'datagroup'] = '6'


# In[ ]:


combine=[train_data]

for dataset in combine:
    dataset.loc[dataset['bill']<=0,'billgroup']='1'
    dataset.loc[(dataset['bill'] > 0) & (dataset['bill'] <= 50), 'billgroup'] = '2'
    dataset.loc[(dataset['bill'] > 50) & (dataset['bill'] <= 100), 'billgroup'] = '3'
    dataset.loc[(dataset['bill'] > 100) & (dataset['bill'] <= 200), 'billgroup'] = '4'
    dataset.loc[(dataset['bill'] > 200) & (dataset['bill'] <= 400), 'billgroup'] = '5'
    dataset.loc[ dataset['bill'] > 400, 'billgroup'] = '6'


# In[ ]:


combine=[test_data]

for dataset in combine:
    dataset.loc[dataset['bill']<=0,'billgroup']='1'
    dataset.loc[(dataset['bill'] > 0) & (dataset['bill'] <= 50), 'billgroup'] = '2'
    dataset.loc[(dataset['bill'] > 50) & (dataset['bill'] <= 100), 'billgroup'] = '3'
    dataset.loc[(dataset['bill'] > 100) & (dataset['bill'] <= 200), 'billgroup'] = '4'
    dataset.loc[(dataset['bill'] > 200) & (dataset['bill'] <= 400), 'billgroup'] = '5'
    dataset.loc[ dataset['bill'] > 400, 'billgroup'] = '6'


# In[ ]:


combine=[train_data]

for dataset in combine:
    dataset.loc[dataset['volte_dura']<=0,'volte_duragroup']='1'
    dataset.loc[(dataset['volte_dura'] > 0) & (dataset['volte_dura'] <= 100), 'volte_duragroup'] = '2'
    dataset.loc[(dataset['volte_dura'] > 100) & (dataset['volte_dura'] <= 400), 'volte_duragroup'] = '3'
    dataset.loc[(dataset['volte_dura'] > 400) & (dataset['volte_dura'] <= 700), 'volte_duragroup'] = '4'
    dataset.loc[(dataset['volte_dura'] > 700) & (dataset['volte_dura'] <= 1000), 'volte_duragroup'] = '5'
    dataset.loc[ dataset['volte_dura'] > 1000, 'volte_duragroup'] = '6'


# In[ ]:


combine=[test_data]

for dataset in combine:
    dataset.loc[dataset['volte_dura']<=0,'volte_duragroup']='1'
    dataset.loc[(dataset['volte_dura'] > 0) & (dataset['volte_dura'] <= 100), 'volte_duragroup'] = '2'
    dataset.loc[(dataset['volte_dura'] > 100) & (dataset['volte_dura'] <= 400), 'volte_duragroup'] = '3'
    dataset.loc[(dataset['volte_dura'] > 400) & (dataset['volte_dura'] <= 700), 'volte_duragroup'] = '4'
    dataset.loc[(dataset['volte_dura'] > 700) & (dataset['volte_dura'] <= 1000), 'volte_duragroup'] = '5'
    dataset.loc[ dataset['volte_dura'] > 1000, 'volte_duragroup'] = '6'


# In[ ]:


combine=[train_data]

for dataset in combine:
    dataset.loc[dataset['flow']<=1,'flowgroup']='1'
    dataset.loc[(dataset['flow'] > 1) & (dataset['flow'] <= 50), 'flowgroup'] = '2'
    dataset.loc[(dataset['flow'] > 50) & (dataset['flow'] <= 500), 'flowgroup'] = '3'
    dataset.loc[(dataset['flow'] > 500) & (dataset['flow'] <= 5000), 'flowgroup'] = '4'
    dataset.loc[(dataset['flow'] > 5000) & (dataset['flow'] <= 10000), 'flowgroup'] = '5'
    dataset.loc[(dataset['flow'] > 10000) & (dataset['flow'] <= 20000), 'flowgroup'] = '6'
    dataset.loc[ dataset['flow'] > 20000, 'flowgroup'] = '7'


# In[ ]:


combine=[test_data]

for dataset in combine:
    dataset.loc[dataset['flow']<=1,'flowgroup']='1'
    dataset.loc[(dataset['flow'] > 1) & (dataset['flow'] <= 50), 'flowgroup'] = '2'
    dataset.loc[(dataset['flow'] > 50) & (dataset['flow'] <= 500), 'flowgroup'] = '3'
    dataset.loc[(dataset['flow'] > 500) & (dataset['flow'] <= 5000), 'flowgroup'] = '4'
    dataset.loc[(dataset['flow'] > 5000) & (dataset['flow'] <= 10000), 'flowgroup'] = '5'
    dataset.loc[(dataset['flow'] > 10000) & (dataset['flow'] <= 20000), 'flowgroup'] = '6'
    dataset.loc[ dataset['flow'] > 20000, 'flowgroup'] = '7'


# In[ ]:


combine=[train_data]

for dataset in combine:
    dataset.loc[dataset['call_out_times']<=0,'call_out_timesgroup']='1'
    dataset.loc[(dataset['call_out_times'] > 0) & (dataset['call_out_times'] <= 10), 'call_out_timesgroup'] = '2'
    dataset.loc[(dataset['call_out_times'] > 10) & (dataset['call_out_times'] <= 50), 'call_out_timesgroup'] = '3'
    dataset.loc[(dataset['call_out_times'] > 50) & (dataset['call_out_times'] <= 100), 'call_out_timesgroup'] = '4'
    dataset.loc[(dataset['call_out_times'] > 100) & (dataset['call_out_times'] <= 150), 'call_out_timesgroup'] = '5'
    dataset.loc[ dataset['call_out_times'] > 150, 'call_out_timesgroup'] = '6'


# In[ ]:


combine=[test_data]

for dataset in combine:
    dataset.loc[dataset['call_out_times']<=0,'call_out_timesgroup']='1'
    dataset.loc[(dataset['call_out_times'] > 0) & (dataset['call_out_times'] <= 10), 'call_out_timesgroup'] = '2'
    dataset.loc[(dataset['call_out_times'] > 10) & (dataset['call_out_times'] <= 50), 'call_out_timesgroup'] = '3'
    dataset.loc[(dataset['call_out_times'] > 50) & (dataset['call_out_times'] <= 100), 'call_out_timesgroup'] = '4'
    dataset.loc[(dataset['call_out_times'] > 100) & (dataset['call_out_times'] <= 150), 'call_out_timesgroup'] = '5'
    dataset.loc[ dataset['call_out_times'] > 150, 'call_out_timesgroup'] = '6'


# In[ ]:


combine=[train_data]

for dataset in combine:
    dataset.loc[dataset['call_out_dura']<=0,'call_out_duragroup']='1'
    dataset.loc[(dataset['call_out_dura'] > 0) & (dataset['call_out_dura'] <= 50), 'call_out_duragroup'] = '2'
    dataset.loc[(dataset['call_out_dura'] > 50) & (dataset['call_out_dura'] <= 200), 'call_out_duragroup'] = '3'
    dataset.loc[(dataset['call_out_dura'] > 200) & (dataset['call_out_dura'] <= 500), 'call_out_duragroup'] = '4'
    dataset.loc[(dataset['call_out_dura'] > 500) & (dataset['call_out_dura'] <= 1000), 'call_out_duragroup'] = '5'
    dataset.loc[(dataset['call_out_dura'] > 1000) & (dataset['call_out_dura'] <= 2000), 'call_out_duragroup'] = '6'
    dataset.loc[ dataset['call_out_dura'] > 2000, 'call_out_duragroup'] = '7'


# In[ ]:


combine=[test_data]

for dataset in combine:
    dataset.loc[dataset['call_out_dura']<=0,'call_out_duragroup']='1'
    dataset.loc[(dataset['call_out_dura'] > 0) & (dataset['call_out_dura'] <= 50), 'call_out_duragroup'] = '2'
    dataset.loc[(dataset['call_out_dura'] > 50) & (dataset['call_out_dura'] <= 200), 'call_out_duragroup'] = '3'
    dataset.loc[(dataset['call_out_dura'] > 200) & (dataset['call_out_dura'] <= 500), 'call_out_duragroup'] = '4'
    dataset.loc[(dataset['call_out_dura'] > 500) & (dataset['call_out_dura'] <= 1000), 'call_out_duragroup'] = '5'
    dataset.loc[(dataset['call_out_dura'] > 1000) & (dataset['call_out_dura'] <= 2000), 'call_out_duragroup'] = '6'
    dataset.loc[ dataset['call_out_dura'] > 2000, 'call_out_duragroup'] = '7'


# In[ ]:


combine=[train_data]
for dataset in combine:
    dataset.loc[dataset['call_in_times']<=0,'call_in_timesgroup']='1'
    dataset.loc[(dataset['call_in_times'] > 0) & (dataset['call_in_times'] <= 10), 'call_in_timesgroup'] = '2'
    dataset.loc[(dataset['call_in_times'] > 10) & (dataset['call_in_times'] <= 50), 'call_in_timesgroup'] = '3'
    dataset.loc[(dataset['call_in_times'] > 50) & (dataset['call_in_times'] <= 100), 'call_in_timesgroup'] = '4'
    dataset.loc[(dataset['call_in_times'] > 100) & (dataset['call_in_times'] <= 150), 'call_in_timesgroup'] = '5'
    dataset.loc[ dataset['call_in_times'] > 150, 'call_in_timesgroup'] = '6'


# In[ ]:


combine=[test_data]
for dataset in combine:
    dataset.loc[dataset['call_in_times']<=0,'call_in_timesgroup']='1'
    dataset.loc[(dataset['call_in_times'] > 0) & (dataset['call_in_times'] <= 10), 'call_in_timesgroup'] = '2'
    dataset.loc[(dataset['call_in_times'] > 10) & (dataset['call_in_times'] <= 50), 'call_in_timesgroup'] = '3'
    dataset.loc[(dataset['call_in_times'] > 50) & (dataset['call_in_times'] <= 100), 'call_in_timesgroup'] = '4'
    dataset.loc[(dataset['call_in_times'] > 100) & (dataset['call_in_times'] <= 150), 'call_in_timesgroup'] = '5'
    dataset.loc[ dataset['call_in_times'] > 150, 'call_in_timesgroup'] = '6'


# In[ ]:


combine=[train_data]

for dataset in combine:
    dataset.loc[dataset['call_in_dura']<=0,'call_in_duragroup']='1'
    dataset.loc[(dataset['call_in_dura'] > 0) & (dataset['call_in_dura'] <= 50), 'call_in_duragroup'] = '2'
    dataset.loc[(dataset['call_in_dura'] > 50) & (dataset['call_in_dura'] <= 200), 'call_in_duragroup'] = '3'
    dataset.loc[(dataset['call_in_dura'] > 200) & (dataset['call_in_dura'] <= 500), 'call_in_duragroup'] = '4'
    dataset.loc[(dataset['call_in_dura'] > 500) & (dataset['call_in_dura'] <= 1000), 'call_in_duragroup'] = '5'
    dataset.loc[(dataset['call_in_dura'] > 1000) & (dataset['call_in_dura'] <= 2000), 'call_in_duragroup'] = '6'
    dataset.loc[ dataset['call_in_dura'] > 2000, 'call_in_duragroup'] = '7'


# In[ ]:


combine=[test_data]

for dataset in combine:
    dataset.loc[dataset['call_in_dura']<=0,'call_in_duragroup']='1'
    dataset.loc[(dataset['call_in_dura'] > 0) & (dataset['call_in_dura'] <= 50), 'call_in_duragroup'] = '2'
    dataset.loc[(dataset['call_in_dura'] > 50) & (dataset['call_in_dura'] <= 200), 'call_in_duragroup'] = '3'
    dataset.loc[(dataset['call_in_dura'] > 200) & (dataset['call_in_dura'] <= 500), 'call_in_duragroup'] = '4'
    dataset.loc[(dataset['call_in_dura'] > 500) & (dataset['call_in_dura'] <= 1000), 'call_in_duragroup'] = '5'
    dataset.loc[(dataset['call_in_dura'] > 1000) & (dataset['call_in_dura'] <= 2000), 'call_in_duragroup'] = '6'
    dataset.loc[ dataset['call_in_dura'] > 2000, 'call_in_duragroup'] = '7'


# In[ ]:


combine=[train_data]

for dataset in combine:
    dataset.loc[dataset['listed_price']<=1000,'listed_pricegroup']='1'
    dataset.loc[(dataset['listed_price'] > 1000) & (dataset['listed_price'] <= 2000), 'listed_pricegroup'] = '2'
    dataset.loc[(dataset['listed_price'] > 2000) & (dataset['listed_price'] <= 3000), 'listed_pricegroup'] = '3'
    dataset.loc[(dataset['listed_price'] > 3000) & (dataset['listed_price'] <= 5000), 'listed_pricegroup'] = '4'
    dataset.loc[(dataset['listed_price'] > 5000) & (dataset['listed_price'] <= 7000), 'listed_pricegroup'] = '5'
    dataset.loc[(dataset['listed_price'] > 7000) & (dataset['listed_price'] <= 10000), 'listed_pricegroup'] = '6'
    dataset.loc[ dataset['listed_price'] > 10000, 'listed_pricegroup'] = '7'


# In[ ]:


combine=[test_data]

for dataset in combine:
    dataset.loc[dataset['listed_price']<=1000,'listed_pricegroup']='1'
    dataset.loc[(dataset['listed_price'] > 1000) & (dataset['listed_price'] <= 2000), 'listed_pricegroup'] = '2'
    dataset.loc[(dataset['listed_price'] > 2000) & (dataset['listed_price'] <= 3000), 'listed_pricegroup'] = '3'
    dataset.loc[(dataset['listed_price'] > 3000) & (dataset['listed_price'] <= 5000), 'listed_pricegroup'] = '4'
    dataset.loc[(dataset['listed_price'] > 5000) & (dataset['listed_price'] <= 7000), 'listed_pricegroup'] = '5'
    dataset.loc[(dataset['listed_price'] > 7000) & (dataset['listed_price'] <= 10000), 'listed_pricegroup'] = '6'
    dataset.loc[ dataset['listed_price'] > 10000, 'listed_pricegroup'] = '7'


# In[ ]:


combine=[train_data]

for dataset in combine:
    dataset.loc[dataset['age']<=16,'agegroup']='1'
    dataset.loc[(dataset['age'] > 16) & (dataset['age'] <= 23), 'agegroup'] = '2'
    dataset.loc[(dataset['age'] > 23) & (dataset['age'] <= 30), 'agegroup'] = '3'
    dataset.loc[(dataset['age'] > 30) & (dataset['age'] <= 40), 'agegroup'] = '4'
    dataset.loc[(dataset['age'] > 40) & (dataset['age'] <= 60), 'agegroup'] = '5'
    dataset.loc[ dataset['age'] > 60, 'agegroup'] = '6'


# In[ ]:


combine=[test_data]

for dataset in combine:
    dataset.loc[dataset['age']<=16,'agegroup']='1'
    dataset.loc[(dataset['age'] > 16) & (dataset['age'] <= 23), 'agegroup'] = '2'
    dataset.loc[(dataset['age'] > 23) & (dataset['age'] <= 30), 'agegroup'] = '3'
    dataset.loc[(dataset['age'] > 30) & (dataset['age'] <= 40), 'agegroup'] = '4'
    dataset.loc[(dataset['age'] > 40) & (dataset['age'] <= 60), 'agegroup'] = '5'
    dataset.loc[ dataset['age'] > 60, 'agegroup'] = '6'


# In[ ]:





# In[ ]:


data_all = pd.concat([train_data.assign(is_train = 1),test_data.assign(is_train = 0)]) #合并train和test，并且用is_train进行标记
train = data_all['is_train'] == 1##提前进行标记
test  = data_all['is_train'] == 0


# In[ ]:





# In[ ]:


data_all['sex']=test_data['sex'].fillna(0)


# In[ ]:


data_all.replace([np.inf, -np.inf], np.nan, inplace=True)
#new_test_data.replace([np.inf, -np.inf], np.nan, inplace=True)


# In[ ]:


fact_list = data_all['ue_tac_id'].value_counts()[0:30]
data_all['ue_tac_id']=data_all['ue_tac_id'].apply(lambda x:'其他' if x not in fact_list else x)

fact_list = data_all['model_id'].value_counts()[0:30]
data_all['model_id']=data_all['model_id'].apply(lambda x:'其他' if x not in fact_list else x)

fact_list = data_all['support_band'].value_counts()[0:30]
data_all['support_band']=data_all['support_band'].apply(lambda x:'其他' if x not in fact_list else x)


# In[ ]:


label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['dinner_type'].values)))
data_all['dinner_type']=label.transform(list(data_all['dinner_type'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['terminal_5g_type'].values)))
data_all['terminal_5g_type']=label.transform(list(data_all['terminal_5g_type'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['model_id'].values)))
data_all['model_id']=label.transform(list(data_all['model_id'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['ue_tac_id'].values)))
data_all['ue_tac_id']=label.transform(list(data_all['ue_tac_id'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['user_lv'].values)))
data_all['user_lv']=label.transform(list(data_all['user_lv'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['sex'].values)))
data_all['sex']=label.transform(list(data_all['sex'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['user_status'].values)))
data_all['user_status']=label.transform(list(data_all['user_status'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['service_type'].values)))
data_all['service_type']=label.transform(list(data_all['service_type'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['complaint_status'].values)))
data_all['complaint_status']=label.transform(list(data_all['complaint_status'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['support_band'].values)))
data_all['support_band']=label.transform(list(data_all['support_band'].values))

label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['svc_id'].values)))
data_all['svc_id']=label.transform(list(data_all['svc_id'].values))


label = preprocessing.LabelEncoder()
label.fit(np.unique(list(data_all['model_name'].values)))
data_all['model_name']=label.transform(list(data_all['model_name'].values))


# In[ ]:


#删除不同列名相同的数值的特征
def drop_duplicate_cols(df):
    uniq, idxs = np.unique(df, return_index=True, axis=1)
    return pd.DataFrame(uniq, index=df.index, columns=df.columns[idxs])


# In[ ]:


'''
transformer = TfidfTransformer(smooth_idf=False)
tfidf = transformer.fit_transform(data_all[['user_lv','model_name', 'terminal_5g_type']])
tfidf.toarray()
'''


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


'''
data_all['dinner_type'] = data_all['dinner_type'].astype('category')
data_all['terminal_5g_type'] = data_all['terminal_5g_type'].astype('category')
data_all['model_id'] = data_all['model_id'].astype('category')
data_all['support_band'] = data_all['support_band'].astype('category')
data_all['ue_tac_id'] = data_all['ue_tac_id'].astype('category')
data_all['agegroup'] = data_all['agegroup'].astype('category')
data_all['datagroup'] = data_all['datagroup'].astype('category')
data_all['billgroup'] = data_all['billgroup'].astype('category')
data_all['volte_duragroup'] = data_all['volte_duragroup'].astype('category')
data_all['flowgroup'] = data_all['flowgroup'].astype('category')
data_all['call_out_timesgroup'] = data_all['call_out_timesgroup'].astype('category')
data_all['call_out_duragroup'] = data_all['call_out_duragroup'].astype('category')
data_all['call_in_timesgroup'] = data_all['call_in_timesgroup'].astype('category')
data_all['listed_pricegroup'] = data_all['listed_pricegroup'].astype('category')
data_all['user_lv'] = data_all['user_lv'].astype('category')
data_all['sex'] = data_all['sex'].astype('category')
data_all['user_status'] = data_all['user_status'].astype('category')
data_all['fuse_type'] = data_all['fuse_type'].astype('category')
data_all['service_type'] = data_all['service_type'].astype('category')
data_all['complaint_status'] = data_all['complaint_status'].astype('category')
'''


# In[ ]:


#from autogluon.features.generators import AutoMLPipelineFeatureGenerator


# In[ ]:





# In[ ]:


#data_all['support_band'] = train_temp['service_type']


# In[ ]:


# REF - https://www.kaggle.com/shahnawazakhtar/using-features-from-label-categories-csv
def vectorize(train, test, columns, fillMissing):
    data = pd.concat((train, test), axis=0, ignore_index=True)
    data = data[columns].astype(np.str).apply(lambda x: " ".join(s for s in x), axis=1).fillna(fillMissing)
    print(data.shape)
    split_len = len(train)

    # TF-IDF Feature
    print("TfidfVectorizer for", columns)
    vectorizer = TfidfVectorizer(min_df=1)
    data = vectorizer.fit_transform(data)

    train = data[:split_len, :]
    test = data[split_len:, :]
    return train, test


def vectorizeOHE(train, test, columns, fillMissing):
    data = pd.concat((train, test), axis=0, ignore_index=True)
    data = data[columns].astype(np.str).apply(lambda x: " ".join(s for s in x), axis=1).fillna(fillMissing)
    print(data.shape)
    split_len = len(train)

    # OHE Feature
    print("One Hot Encoding for", columns)
    vectorizer = CountVectorizer(min_df=1)
    data = vectorizer.fit_transform(data)

    train = data[:split_len, :]
    test = data[split_len:, :]
    return train, test


# In[ ]:


new_train_data = data_all[data_all['is_train']== 1]
new_test_data  = data_all[data_all['is_train']== 0]


# In[ ]:


new_train_data.shape


# In[ ]:


new_test_data.shape


# In[ ]:





# In[ ]:


#nlp特征信息提取
col_cat = ['user_lv','model_name', 'terminal_5g_type']
features_train_new, features_test_new, colNames_train_new, colNames_test_new = NLP_Group_Stat(X_train = new_train_data, 
                                                                                              X_test = new_test_data, 
                                                                                              col_cat = col_cat)


# In[ ]:


new_train_data = pd.concat([new_train_data, features_train_new], axis=1)
new_test_data = pd.concat([new_test_data, features_test_new], axis=1)


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


# In[ ]:


new_train_data['NLP'] = new_train_data['support_band']

new_test_data['NLP'] = new_test_data['support_band']


# In[ ]:


Xtr_NLP, Xte_NLP = vectorizeOHE(new_train_data, new_test_data, ["NLP"], "missing")


# In[ ]:


print(Xtr_NLP)


# In[ ]:


Xtr_NLP_pd = pd.DataFrame(Xtr_NLP)
Xte_NLP_pd = pd.DataFrame(Xte_NLP)


# In[ ]:


new_train_data = new_train_data.drop(['NLP'], axis=1)
new_test_data = new_test_data.drop(['NLP'], axis=1)


# In[ ]:


new_train_data = pd.concat([new_train_data, Xtr_NLP_pd], axis=1)
new_test_data = pd.concat([new_test_data, Xte_NLP_pd], axis=1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#new_train_data['score'][train_data['score'] < 3] =1
#new_train_data['score'][train_data['score'] > 7] =0


# In[ ]:


'''
feature_generator = AutoMLPipelineFeatureGenerator()
label = 'score'
X_train = new_train_data.drop(labels=[label], axis=1)
y_train = new_train_data[label]
X_train_transformed = feature_generator.fit_transform(X=X_train, y=y_train)
X_test_transformed = feature_generator.transform(new_test_data)
'''


# In[ ]:





# In[ ]:


new_train_data = new_train_data.drop(['open_date','is_train','im_sendaudio_req_times','im_sendaudio_succ_times','im_pay_dl_rtt_total_delay','im_pay_ul_rtt_total_delay','im_pay_ul_avg_rtt_long_times','im_pay_dl_avg_rtt_long_times','tcp_dl_server_probe_lost_pkt','tcp_dl_user_probe_lost_pkt','tcp_ul_user_probe_lost_pkt','tcp_ul_server_probe_lost_pkt','tcp_ul_rtt_long_times','tcp_dl_rtt_long_times','traffic_23g','im_pay_ul_rtt_stat_times','im_pay_dl_rtt_stat_times','https_dl_big_packet_total_delay','model_name','open_date','user_type','is_lucknumber','prepay_tag','net_certificates_type','is_standy'], axis=1)
new_test_data = new_test_data.drop(['open_date','is_train','score','im_sendaudio_req_times','im_sendaudio_succ_times','im_pay_dl_rtt_total_delay','im_pay_ul_rtt_total_delay','im_pay_ul_avg_rtt_long_times','im_pay_dl_avg_rtt_long_times','tcp_dl_server_probe_lost_pkt','tcp_dl_user_probe_lost_pkt','tcp_ul_user_probe_lost_pkt','tcp_ul_server_probe_lost_pkt','tcp_ul_rtt_long_times','tcp_dl_rtt_long_times','traffic_23g','im_pay_ul_rtt_stat_times','im_pay_dl_rtt_stat_times','https_dl_big_packet_total_delay','model_name','open_date','user_type','is_lucknumber','prepay_tag','net_certificates_type','is_standy'], axis=1)
#X_train_transformed['score'] = new_train_data['score']


# In[ ]:


#train_data['score'][train_data['score'] == 1] =1
#new_train_data['score'][train_data['score'] < 3] =0
#new_train_data['score'][train_data['score'] > 7]=1
#new_train_data = new_train_data[(new_train_data['score'] == 1) | (new_train_data['score'] ==0)]


# In[ ]:


#new_train_data = new_train_data.fillna(0)
#new_test_data = new_train_data.fillna(0)


# In[ ]:





# In[ ]:





# In[ ]:


new_train_data.to_csv('X_train_transformed_918.csv',index=False)
new_test_data.to_csv('X_test_transformed_918.csv',index=False)


# In[ ]:


#new_train_data = new_train_data.drop(['is_train','listed_price','bill','volte_dura','flow','call_out_times','call_out_dura','call_in_times','call_in_dura','msisdn','http_rsp_delay_long_times','age','svc_id','im_sendaudio_req_times','im_sendaudio_succ_times','im_pay_dl_rtt_total_delay','im_pay_ul_rtt_total_delay','im_pay_ul_avg_rtt_long_times','im_pay_dl_avg_rtt_long_times','tcp_dl_server_probe_lost_pkt','tcp_dl_user_probe_lost_pkt','tcp_ul_user_probe_lost_pkt','tcp_ul_server_probe_lost_pkt','tcp_ul_rtt_long_times','tcp_dl_rtt_long_times','traffic_23g','im_pay_ul_rtt_stat_times','im_pay_dl_rtt_stat_times','https_dl_big_packet_total_delay','model_name','open_date','user_type','is_lucknumber','prepay_tag','net_certificates_type','is_standy'], axis=1)
#new_test_data = new_test_data.drop(['is_train','score','listed_price','bill','volte_dura','flow','call_out_times','call_out_dura','call_in_times','call_in_dura','msisdn','http_rsp_delay_long_times','age','svc_id','im_sendaudio_req_times','im_sendaudio_succ_times','im_pay_dl_rtt_total_delay','im_pay_ul_rtt_total_delay','im_pay_ul_avg_rtt_long_times','im_pay_dl_avg_rtt_long_times','tcp_dl_server_probe_lost_pkt','tcp_dl_user_probe_lost_pkt','tcp_ul_user_probe_lost_pkt','tcp_ul_server_probe_lost_pkt','tcp_ul_rtt_long_times','tcp_dl_rtt_long_times','traffic_23g','im_pay_ul_rtt_stat_times','im_pay_dl_rtt_stat_times','https_dl_big_packet_total_delay','model_name','open_date','user_type','is_lucknumber','prepay_tag','net_certificates_type','is_standy'], axis=1)
##new_train_data = new_train_data.drop(['is_train'], axis=1)


# In[ ]:


#new_train_data.replace([np.inf, -np.inf], np.nan, inplace=True)
#new_test_data.replace([np.inf, -np.inf], np.nan, inplace=True)


# In[ ]:


#new_train_data.to_csv('train_data_new_913.csv',index=False)
#new_test_data.to_csv('test_data_new_913.csv',index=False)





# In[ ]:




