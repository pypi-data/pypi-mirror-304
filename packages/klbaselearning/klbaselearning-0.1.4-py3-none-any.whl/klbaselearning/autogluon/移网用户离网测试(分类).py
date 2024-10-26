#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from autogluon.tabular import TabularDataset,TabularPredictor
import os
import pandas as pd
import numpy as np
os.environ["NUMEXPR_MAX_THREADS"] = '20'


# In[ ]:


# 导入数据  
print("Loading Data ... ")  
df = pd.read_csv('../user_data/train_data_F.csv')#在特征工程代码中生成的中间文件
test_data = pd.read_csv('../user_data/test_data_F.csv')#在特征工程代码中生成的中间文件
best_sub = pd.read_csv('../user_data/best_sub_9704.csv')#注:best_sub_9704.csv为上一次最好提交结果，该CSV也为此模型在原始训练文件中跑出，但模型参数可能略有不同，分数0.9704（7月4日），在这个CSV基础上提取训练样本加入原训练集中，让模型学习更多的隐藏因子。


# In[ ]:


test_data3 = test_data.copy()
test_data2 = test_data.copy()
newdf = df.copy()
newdf = newdf.drop(['客户ID','is_train','平均丢弃数据呼叫数'], axis=1)#'平均丢弃数据呼叫数',


# In[ ]:


'''
newdf['地理区域'] = newdf['地理区域'].astype('category')
newdf['是否双频'] = newdf['是否双频'].astype('category')
newdf['是否翻新机'] = newdf['是否翻新机'].astype('category')
newdf['手机网络功能'] = newdf['手机网络功能'].astype('category')
newdf['婚姻状况'] = newdf['婚姻状况'].astype('category')
newdf['信息库匹配'] = newdf['信息库匹配'].astype('category')
newdf['新手机用户'] = newdf['新手机用户'].astype('category')
newdf['账户消费限额'] = newdf['账户消费限额'].astype('category')
newdf['信用卡指示器'] = newdf['信用卡指示器'].astype('category')
newdf['是否双频'] = newdf['是否双频'].astype('category')
'''


# In[ ]:


'''
newdf['过去三个月的平均每月使用分钟数bin'] = newdf['过去三个月的平均每月使用分钟数bin'].astype('category')
newdf['过去三个月的平均每月通话次数bin'] = newdf['过去三个月的平均每月通话次数bin'].astype('category')
newdf['过去三个月的平均月费用bin'] = newdf['过去三个月的平均月费用bin'].astype('category')
newdf['过去六个月的平均每月使用分钟数bin'] = newdf['过去六个月的平均每月使用分钟数bin'].astype('category')
newdf['过去六个月的平均每月通话次数bin'] = newdf['过去六个月的平均每月通话次数bin'].astype('category')
newdf['过去六个月的平均月费用bin'] = newdf['过去六个月的平均月费用bin'].astype('category')
newdf['平均未接语音呼叫数bin'] = newdf['平均未接语音呼叫数bin'].astype('category')
newdf['平均非高峰语音呼叫数bin'] = newdf['平均非高峰语音呼叫数bin'].astype('category')
newdf['使用高峰语音通话的平均不完整分钟数bin'] = newdf['使用高峰语音通话的平均不完整分钟数bin'].astype('category')
newdf['当前设备使用天数bin'] = newdf['当前设备使用天数bin'].astype('category')
newdf['当前手机价格bin'] = newdf['当前手机价格bin'].astype('category')
'''
#newdf = newdf.drop(['平均峰值数据调用次数','平均掉线或占线呼叫数','平均呼入和呼出高峰语音呼叫数','平均非高峰语音呼叫数','非高峰数据呼叫的平均数量','平均已完成呼叫数','平均呼叫转移呼叫数','平均呼叫等待呼叫数','一分钟内的平均呼入电话数','客户生命周期内平均月费用','过去三个月的平均月费用','平均三通电话数','平均接听语音电话数','使用客户服务电话的平均分钟数','平均超额费用','家庭成人人数','预计收入','在职总月数','家庭中唯一订阅者的数量','家庭活跃用户数','平均月费用','平均语音费用','平均客户服务电话次数','数据超载的平均费用','平均漫游呼叫数','平均掉线语音呼叫数','平均丢弃数据呼叫数','平均占线语音呼叫数','平均占线数据调用次数','平均未接语音呼叫数','未应答数据呼叫的平均次数','尝试数据调用的平均数','平均完成的语音呼叫数','完成数据调用的平均数','过去六个月的平均月费用'], axis=1)
#newdf = newdf.drop(['客户ID','平均峰值数据调用次数','平均掉线或占线呼叫数','平均呼入和呼出高峰语音呼叫数','平均非高峰语音呼叫数','非高峰数据呼叫的平均数量','地理区域','平均已完成呼叫数','平均呼叫转移呼叫数','平均呼叫等待呼叫数','账户消费限额','一分钟内的平均呼入电话数','客户生命周期内平均月费用','过去三个月的平均月费用','平均三通电话数','平均接听语音电话数','使用客户服务电话的平均分钟数','平均超额费用','是否翻新机','手机网络功能','婚姻状况','家庭成人人数','信息库匹配','预计收入','信用卡指示器','在职总月数','家庭中唯一订阅者的数量','家庭活跃用户数','新手机用户','平均月费用','平均语音费用','平均客户服务电话次数','数据超载的平均费用','平均漫游呼叫数','平均掉线语音呼叫数','平均丢弃数据呼叫数','平均占线语音呼叫数','平均占线数据调用次数','平均未接语音呼叫数','未应答数据呼叫的平均次数','尝试数据调用的平均数','是否双频','平均完成的语音呼叫数','完成数据调用的平均数','过去六个月的平均月费用'], axis=1)


# In[ ]:


newdf.info(verbose=True, null_counts=True)
from sklearn.model_selection import train_test_split
X=newdf
y=newdf['是否流失']
train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.0001,random_state=2022)
print(test_x.shape)
print(train_x.shape)
print(test_y.shape)


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


#注：训练时间较长，约为11个小时，将生成约31.5GB大小的模型文件夹
predictor = TabularPredictor(label='是否流失', eval_metric='roc_auc').fit(train_data=X,presets='best_quality',verbosity = 3,auto_stack=True,  num_bag_folds=10, num_bag_sets=10, num_stack_levels=3)  


# In[ ]:


results = predictor.fit_summary()   #8034#"AutogluonModels/ag-20220704_164359/"


# In[ ]:


pred_test=predictor.predict_proba(test_data)#,model='LightGBM'


# In[ ]:


test_data3['是否流失'] = pred_test[1]

test_data3[['客户ID','是否流失']].to_csv('../user_data/best_sub_9704.csv', index=False)

