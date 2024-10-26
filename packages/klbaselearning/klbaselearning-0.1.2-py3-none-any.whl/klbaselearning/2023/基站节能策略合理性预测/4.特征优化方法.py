#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 基础数据科学运算库
import numpy as np
import pandas as pd
import seaborn as sns


# 可视化库
#import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from pylab import rcParams
#import statsmodels.api as sm
from tqdm import tqdm

# 时间模块
import time

# sklearn库
# 数据预处理
from sklearn import preprocessing
from sklearn.compose import ColumnTransformer

# 实用函数
from sklearn.metrics import mean_absolute_error 
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate, KFold
from sklearn.preprocessing import StandardScaler

# 常用评估器
import xgboost as xgb
import lightgbm as lgb

# 网格搜索
from sklearn.model_selection import GridSearchCV

# re模块相关
import inspect, re

#内存清理库
import gc

#导入优化算法
import hyperopt
from hyperopt import hp, fmin, tpe, Trials, partial
#from hyperopt.early_stop import no_progress_loss
from datetime import date, timedelta

plt.rcParams['font.sans-serif'] = 'SimHei'  #显示中文
plt.rcParams['axes.unicode_minus'] = False  #显示负号
pd.set_option('display.max_row', None)
pd.set_option('display.max_columns', None)

#导入自定义模块
from fea_test import *
from features import *

get_ipython().run_line_magic('matplotlib', 'inline')

import warnings
warnings.filterwarnings('ignore')


# In[ ]:


train = pd.read_csv('train_df.csv', index_col=False)
test = pd.read_csv('test_df.csv', index_col=False)
train = train.drop(columns=['weekday'], axis=1, inplace=False)
test = test.drop(columns=['weekday'], axis=1, inplace=False)
#特征标注
# 离散字段
category_cols = ['周边小区群数量', 'day', 'hour', 'hour_section']

# 连续字段
numeric_cols = ['周边小区群RRC连接平均数_群1', '周边小区群RRC连接平均数_群2', '周边小区群RRC连接平均数_群3',
       '周边小区群RRC连接平均数_群4', '周边小区群RRC连接平均数_群5', '周边小区群RRC连接平均数_群6',
       '周边小区群RRC连接平均数_群7', '周边小区群RRC连接平均数_群8', '周边小区群RRC连接平均数_群9',
       '周边小区群RRC连接平均数_群10', 'RRC平均连接数_补偿小区', 'RRC连接最大数_补偿小区',
       '上行PRB平均利用率_补偿小区', '下行PRB平均利用率_补偿小区', 'PDCCH信道CCE占用率_补偿小区']

# 标签
target = 'label'
ID = 'CI'
time = 'time'
add_id = '补偿小区CI'

# 验证是否划分能完全
#assert len(category_cols) + len(numeric_cols) + 4 == train.shape[1]


# In[ ]:


# 5、平均值进行填充，后续有需要再进行优化处理。
num = ['周边小区群RRC连接平均数_群1', '周边小区群RRC连接平均数_群2', '周边小区群RRC连接平均数_群3',
       '周边小区群RRC连接平均数_群4', '周边小区群RRC连接平均数_群5', '周边小区群RRC连接平均数_群6',
       '周边小区群RRC连接平均数_群7', '周边小区群RRC连接平均数_群8', '周边小区群RRC连接平均数_群9',
       '周边小区群RRC连接平均数_群10', 'RRC平均连接数_补偿小区', 'RRC连接最大数_补偿小区',
       '上行PRB平均利用率_补偿小区', '下行PRB平均利用率_补偿小区', 'PDCCH信道CCE占用率_补偿小区']
for col in num:
    train[col] = train[col].fillna(train[col].mean())
    test[col] = test[col].fillna(test[col].mean())


# In[ ]:


features = train.drop(columns=[ID, target, time, add_id]).copy()
labels = train['label'].copy()


# In[ ]:


train.head()


# In[ ]:


train.corr()['label'].sort_values(ascending=False)


# ## 特征衍生测试

# In[ ]:


def features_test(features_train_new,
                  features_test_new,
                  X_train, 
                  X_test, 
                  y_train, 
                  y_test, 
                  category_cols, 
                  numeric_cols):
    """
    新特征测试函数
    
    :param features_train_new: 训练集衍生特征
    :param features_test_new: 测试集衍生特征
    :param X_train: 训练集特征
    :param X_test: 测试集特征
    :param y_train: 训练集标签
    :param y_test: 测试集标签   
    :param category_cols: 离散列名称
    :param numeric_cols: 连续列名称
    :return: result_df评估指标
    """
    
    # 数据准备
    # 如果是一个衍生特征，则将其转化为series
    if type(features_train_new) == np.ndarray:
        name = 'features_train_new'
        features_train_new = pd.Series(features_train_new, name=name)
        
    if type(features_test_new) == np.ndarray:
        name = 'features_test_new'
        features_test_new = pd.Series(features_test_new, name=name)    
    
    # 复制里散列、连续列的列名称
    category_cols = category_cols.copy()
    numeric_cols = numeric_cols.copy()

    # 修改衍生特征矩阵的index
    features_train_new.index = X_train.index
    features_test_new.index = X_test.index
    
    # 将衍生特征和原始特征进行拼接
    X_train = pd.concat([X_train, features_train_new], axis=1)
    X_test = pd.concat([X_test, features_test_new], axis=1)
    
    # 判断衍生特征是连续还是离散
    if type(features_train_new) == pd.DataFrame:
        for col in features_train_new:
            if features_train_new[col].nunique() >= 15:
                numeric_cols.append(col)
            else:
                category_cols.append(col)
    
    else:
        if features_train_new.nunique() >= 15:
            numeric_cols.append(name)
        else:
            category_cols.append(name)

        
    # print(category_cols)
    # 检验列是否划分完全
    assert len(category_cols) + len(numeric_cols) == X_train.shape[1]

    # 训练部分
    # 设置转化器流
    logistic_pre = ColumnTransformer([
        ('cat','passthrough', category_cols), 
        ('num', 'passthrough', numeric_cols)
    ])

    num_pre = ['passthrough', preprocessing.StandardScaler(), preprocessing.KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='kmeans')]

    # 实例化逻辑回归评估器
    logistic_model = logit_threshold(max_iter=int(1e8))

    # 设置机器学习流
    logistic_pipe = make_pipeline(logistic_pre, logistic_model)

    # 设置超参数空间
    logistic_param = [
        {'columntransformer__num':num_pre, 
         'logit_threshold__penalty': ['l1'],
         'logit_threshold__C': np.arange(0.1, 1.1, 0.1).tolist(), 
         'logit_threshold__solver': ['saga']}, 
        {'columntransformer__num':num_pre, 
         'logit_threshold__penalty': ['l2'], 
         'logit_threshold__C': np.arange(0.1, 1.1, 0.1).tolist(),
         'logit_threshold__solver': ['lbfgs', 'newton-cg', 'sag', 'saga']}, 
    ]

    # 实例化网格搜索评估器
    logistic_search = GridSearchCV(estimator = logistic_pipe,
                                   param_grid = logistic_param,
                                   scoring='accuracy',
                                   n_jobs = 12)

    # 输出时间
    logistic_search.fit(X_train, y_train)

    # 计算预测结果
    return(logistic_search.best_score_, logistic_search.best_params_)


# ## 1.多项式特征衍生
# 

# In[ ]:


#3阶多项式衍生
colNames = numeric_cols
X_train_ply, X_test_ply, colNames_train_new, colNames_test_new = Polynomial_Features(colNames=colNames, 
                                                                                     degree=3,
                                                                                     X_train=train, 
                                                                                     X_test=test)


# In[ ]:


X_train_ply.head()


# In[ ]:


#标准化
scaler = StandardScaler()
scaler.fit(X_train_ply)


# In[ ]:


X_train_ply = pd.DataFrame(scaler.transform(X_train_ply), columns=colNames_train_new)
X_train_ply.index = train.index
X_train_ply.head()


# In[ ]:


X_test_ply = pd.DataFrame(scaler.transform(X_test_ply), columns=colNames_test_new)
X_test_ply.index = test.index
X_test_ply.head()


# In[ ]:


# 然后进行数据集拼接
df_temp = pd.concat([X_train_ply, labels], axis=1)

df_temp.head()


# In[ ]:


df_corr = df_temp.corr()['label'].sort_values(ascending = False)


# In[ ]:


df_corr


# ### 2.交叉组合特征衍生
# 

# In[ ]:


# 查看每个分类变量的取值水平
for feature in train[category_cols]:
        print(f'{feature}: {train[feature].unique()}')


# In[ ]:


features_train_new_cross, features_test_new_cross, colNames_train_new_cross, colNames_test_new_cross = Cross_Combination(category_cols, train, test)


# In[ ]:


features_train_new_cross.head()


# In[ ]:


features_train_new_cross.shape


# In[ ]:


features_train_new_cross.index = train.index


# In[ ]:


df_temp = pd.concat([features_train_new_cross, labels], axis=1)


# In[ ]:


df_corr = df_temp.corr()['label'].sort_values(ascending = False)


# In[ ]:


df_corr.head(10)


# #### 3原始特征的多变量交叉组合
# 

# In[ ]:


colNames = ['周边小区群数量', '周边小区群RRC连接平均数_群1', '周边小区群RRC连接平均数_群2', '周边小区群RRC连接平均数_群3',
       '周边小区群RRC连接平均数_群4', '周边小区群RRC连接平均数_群5', '周边小区群RRC连接平均数_群6',
       '周边小区群RRC连接平均数_群7', '周边小区群RRC连接平均数_群8', '周边小区群RRC连接平均数_群9',
       '周边小区群RRC连接平均数_群10', 'RRC平均连接数_补偿小区', 'RRC连接最大数_补偿小区',
       '上行PRB平均利用率_补偿小区', '下行PRB平均利用率_补偿小区', 'PDCCH信道CCE占用率_补偿小区']
features_train_new_ori, features_test_new_ori, colNames_train_new_ori, colNames_test_new_ori = Cross_Combination(colNames, 
                                                                                                 train, 
                                                                                                 test, 
                                                                                                 multi=True)


# ### 4.分组统计特征
# 

# In[ ]:


# 创建容器
col_temp = category_cols.copy()
colNames_train_new_ = []
colNames_test_new_ = []
features_train_new_ = []
features_test_new_ = []

for i in range(len(col_temp)):
    keyCol = col_temp.pop(i)
    features_train1, features_test1, colNames_train, colNames_test = Group_Statistics(keyCol,
                                                                                      train,
                                                                                      test,
                                                                                      col_num=numeric_cols,
                                                                                      col_cat=col_temp, 
                                                                                      extension=True)
    
    colNames_train_new_.extend(colNames_train)
    colNames_test_new_.extend(colNames_test)
    features_train_new_.append(features_train1)
    features_test_new_.append(features_test1)
    
    col_temp = category_cols.copy()


# In[ ]:


features_train_new_ = pd.concat(features_train_new_, axis=1)
features_test_new_ = pd.concat(features_test_new_, axis=1)


# In[ ]:


features_train_new_.shape, features_test_new_.shape


# In[ ]:


features_train_new_.info


# In[ ]:





# In[ ]:


features_train_new_.to_csv('features_train_new.csv',index=False)
features_test_new_.to_csv('features_test_new_.csv',index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# ###  5多变量分组统计
# 

# In[ ]:


#多变量交叉组合作为KeyCol
col1 = ['周边小区群数量', 'day', 'hour']
col2 = ['RRC平均连接数_补偿小区', 'RRC连接最大数_补偿小区', '上行PRB平均利用率_补偿小区']
cl = col1 + col2

周边小区群数量               0.154843
day                   0.002379
PDCCH信道CCE占用率_补偿小区   -0.182437
hour                 -0.213269
hour_section         -0.228605
下行PRB平均利用率_补偿小区      -0.280600
周边小区群RRC连接平均数_群10    -0.302760
周边小区群RRC连接平均数_群9     -0.333258
周边小区群RRC连接平均数_群6     -0.334000
周边小区群RRC连接平均数_群1     -0.335118
周边小区群RRC连接平均数_群7     -0.336037
周边小区群RRC连接平均数_群4     -0.337131
周边小区群RRC连接平均数_群5     -0.337189
周边小区群RRC连接平均数_群3     -0.337432
周边小区群RRC连接平均数_群2     -0.337977
周边小区群RRC连接平均数_群8     -0.338049
RRC平均连接数_补偿小区        -0.341089
RRC连接最大数_补偿小区        -0.363951
上行PRB平均利用率_补偿小区      -0.380752
# In[ ]:


# 拼接数据集
n = len(cl)
# 创建容器
col_temp = []
colNames_train_news = []
colNames_test_news = []
features_train_news = []
features_test_news = []

# 多次循环、遍历三三组合
for i in range(n):
    for j in range(i+1, n):
        for k in range(j+1, n):
            col_temp.append(cl[i])
            col_temp.append(cl[j])
            col_temp.append(cl[k])
            features_train1, features_test1, colNames_train, colNames_test = Cross_Combination(col_temp, 
                                                                                               train, 
                                                                                               test, 
                                                                                               multi=True)
            
            colNames_train_news.extend(colNames_train)
            colNames_test_news.extend(colNames_test)
            features_train_news.append(features_train1)
            features_test_news.append(features_test1)
            
            col_temp = []

# 创建三变量交叉组合衍生数据集            
features_train_news = pd.concat(features_train_news, axis=1)
features_test_news = pd.concat(features_test_news, axis=1)

# 查看衍生数据集规模
print(features_train_news.shape)
print(features_test_news.shape)

# 组合标签
features_train_news.index = X_train.index
features_test_news.index = X_test.index
df_temp = pd.concat([features_train_news, y_train], axis=1)

# 挑选最重要的5个衍生特征
df_corr = df_temp.corr()['Churn'].sort_values(ascending = False)
new_col = list(np.abs(df_corr).sort_values(ascending = False)[1: 6].index)
print(new_col)

# 创建对应df
train_new_MC = features_train_news[new_col]
test_new_MC = features_test_news[new_col]


# In[ ]:


features_train_news.head


# #### 6原始数据集单变量目标编码
# 

# In[ ]:


# 定义标签
col_cat = [target]
print(col_cat)

# 创建容器
col_temp = category_cols.copy()
colNames_train_new = []
colNames_test_new = []
features_train_new = []
features_test_new = []

for keyCol in col_temp:
    features_train1, features_test1, colNames_train_new, colNames_test_new = Target_Encode(keyCol, 
                                                                                           train, 
                                                                                           labels,
                                                                                           test, 
                                                                                           col_cat=col_cat, 
                                                                                           extension=True)
    
    colNames_train_new.extend(colNames_train)
    colNames_test_new.extend(colNames_test)
    features_train_new.append(features_train1)
    features_test_new.append(features_test1)
    
    col_temp = category_cols.copy()


# In[ ]:


train_new_TE = pd.concat(features_train_new, axis=1)
test_new_TE = pd.concat(features_test_new, axis=1)


# In[ ]:


train_new_TE.shape, test_new_TE.shape


# ## 7.NLP特征衍生

# In[ ]:


# 所有离散变量名称
col_cat = category_cols

# 进行NLP特征衍生
features_train_new, features_test_new, colNames_train_new, colNames_test_new = NLP_Group_Stat(train, 
                                                                                              test, 
                                                                                              col_cat)


# In[ ]:


features_train_new.head


# In[ ]:





# In[ ]:





# In[ ]:




