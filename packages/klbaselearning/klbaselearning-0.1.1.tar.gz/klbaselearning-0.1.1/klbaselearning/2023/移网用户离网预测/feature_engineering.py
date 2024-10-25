#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
import pickle  
from sklearn.model_selection import train_test_split  
from sklearn import metrics
pd.set_option('display.max_columns',None)
warnings.filterwarnings("ignore")


# In[2]:


plt.rcParams['font.sans-serif'] = ['AR PL UMing CN'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False # 步骤二（解决坐标轴负数的负号显示问题）


# ## 一、导入数据

# In[3]:


# 导入数据  
print("Loading Data ... ")  
train_data = pd.read_csv('../xfdata/train.csv')
test_data = pd.read_csv('../xfdata/test.csv')


# ## 二、初步探索

# ### 1、 基本描述

# In[4]:


train_data.describe()


# In[5]:


test_data.describe()


# In[6]:


train_data.head()


# In[7]:


test_data.head()


# In[8]:


train_data.shape


# In[9]:


test_data.shape


# In[10]:


train_data.info(verbose=True, null_counts=True)


# In[11]:


test_data.info(verbose=True, null_counts=True)


# ### 2、 nuique、缺失值统计

# In[12]:


stats = []
for col in train_data.columns:
    stats.append((col,train_data[col].nunique(),
                  train_data[col].isnull().sum()*100 / train_data.shape[0],
                  train_data[col].value_counts(normalize=True,
                  dropna=False).values[0]*100,train_data[col].dtype))
    stats_df = pd.DataFrame(stats,columns=['Feature','Unique_values',
                            'Percentage of missing values',
                            'Percentage of values in the biggest category','type'])
stats_df.sort_values('Percentage of missing values',ascending=False)[:113]


# ### 3、特征工程

# In[13]:


train_data['是否翻新机'][train_data['是否翻新机']== -1] =1
test_data['是否翻新机'][test_data['是否翻新机']== -1] =1
train_data[train_data==-1]=np.nan
test_data[test_data==-1]=np.nan


# In[14]:


#train_data['当前手机价格']=train_data['当前手机价格'].fillna(train_data['当前手机价格'].mean())
#test_data['当前手机价格']=test_data['当前手机价格'].fillna(test_data['当前手机价格'].mean())


# In[15]:


#train_data['手机网络功能']=train_data['手机网络功能'].fillna(train_data['手机网络功能'].median())
#test_data['手机网络功能']=test_data['手机网络功能'].fillna(test_data['手机网络功能'].median())


# In[16]:


#train_data['婚姻状况']=train_data['婚姻状况'].fillna(train_data['手机网络功能'].median())
#test_data['婚姻状况']=test_data['婚姻状况'].fillna(test_data['手机网络功能'].median())


# In[17]:


#train_data['家庭成人人数']=train_data['家庭成人人数'].fillna(train_data['家庭成人人数'].median())
#test_data['家庭成人人数']=test_data['家庭成人人数'].fillna(test_data['家庭成人人数'].median())


# In[18]:


#train_data['信息库匹配']=train_data['信息库匹配'].fillna(train_data['信息库匹配'].median())
#test_data['信息库匹配']=test_data['信息库匹配'].fillna(test_data['信息库匹配'].median())


# In[19]:


#train_data['预计收入']=train_data['预计收入'].fillna(train_data['预计收入'].median())
#test_data['预计收入']=test_data['预计收入'].fillna(test_data['预计收入'].median())


# In[20]:


#train_data['信用卡指示器']=train_data['信用卡指示器'].fillna(train_data['信用卡指示器'].median())
#test_data['信用卡指示器']=test_data['信用卡指示器'].fillna(test_data['信用卡指示器'].median())


# In[21]:


#train_data['当前设备使用天数'][train_data['当前设备使用天数']< 0] =np.nan
#test_data['当前设备使用天数'][test_data['当前设备使用天数']< 0 ] =np.nan
#train_data['当前设备使用天数']=train_data['当前设备使用天数'].fillna(train_data['当前设备使用天数'].median())
#test_data['当前设备使用天数']=test_data['当前设备使用天数'].fillna(test_data['当前设备使用天数'].median())


# In[22]:


train_data['平均月费用'][train_data['平均月费用']< 0] =np.nan
test_data['平均月费用'][test_data['平均月费用']< 0 ] =np.nan
#train_data['平均月费用']=train_data['平均月费用'].fillna(train_data['平均月费用'].median())
#test_data['平均月费用']=test_data['平均月费用'].fillna(test_data['平均月费用'].median())


# In[23]:


train_data['家庭中唯一订阅者的数量'][train_data['家庭中唯一订阅者的数量'] > 13]=14
test_data['家庭中唯一订阅者的数量'][test_data['家庭中唯一订阅者的数量'] > 13]=14

train_data['家庭活跃用户数'][train_data['家庭活跃用户数']> 12]=13
test_data['家庭活跃用户数'][test_data['家庭活跃用户数']> 12]=13

train_data['当前设备使用天数'][train_data['当前设备使用天数'] < 0]=0
test_data['当前设备使用天数'][test_data['当前设备使用天数'] < 0]=0


# In[24]:


#fact_list = data_all['家庭中唯一订阅者的数量'].value_counts()[0:８]
#data_all['家庭中唯一订阅者的数量']=data_all['家庭中唯一订阅者的数量'].apply(lambda x:'其他' if x not in fact_list else x)

#fact_list = data_all['user_dinner'].value_counts()[0:140]
#data_all['user_dinner']=data_all['user_dinner'].apply(lambda x:'其他' if x not in fact_list else x)


# In[25]:


train_data_2 = train_data.copy()
test_data_2 = test_data.copy()


# In[26]:


#plt.figure(figsize=(50,50))
#plt.boxplot(x=train_data.values,labels=train_data.columns)
#plt.hlines([-7.5,7.5],0,40,colors='r')
#plt.show()


# In[27]:


'''
#构建新特征
train_data_2['RFM_3m'] = train_data_2['过去三个月的平均月费用']/(train_data_2['过去三个月的平均每月使用分钟数'] * train_data_2['过去三个月的平均每月通话次数'] )
train_data_2['RFM_6m'] = train_data_2['过去六个月的平均月费用']/(train_data_2['过去六个月的平均每月使用分钟数'] * train_data_2['过去六个月的平均每月通话次数'] )
train_data_2['RFM_sum'] = train_data_2['客户生命周期内的总费用']/(train_data_2['客户生命周期内的总通话次数'] * train_data_2['客户生命周期内的总使用分钟数'])
train_data_2['RFM_over'] =  train_data_2['计费调整后的总费用']/(train_data_2['计费调整后的总分钟数'] * train_data_2['计费调整后的呼叫总数'])

train_data_2['mv_3m'] = train_data_2['过去三个月的平均月费用']/train_data_2['过去三个月的平均每月使用分钟数'] 
train_data_2['mv_6m'] = train_data_2['过去六个月的平均月费用']/train_data_2['过去六个月的平均每月使用分钟数'] 
train_data_2['mv_sum'] = train_data_2['客户生命周期内的总费用']/train_data_2['客户生命周期内的总通话次数'] 
train_data_2['mv_over'] = train_data_2['计费调整后的总分钟数'] / train_data_2['计费调整后的呼叫总数']



train_data_2['3m_天数'] = train_data_2['过去三个月的平均月费用']/train_data_2['当前设备使用天数'] 
train_data_2['6m_天数'] = train_data_2['过去六个月的平均月费用']/train_data_2['当前设备使用天数']  
train_data_2['all_天数'] = train_data_2['客户生命周期内的总费用']/train_data_2['当前设备使用天数'] 
train_data_2['over_天数'] = train_data_2['计费调整后的总费用']/train_data_2['当前设备使用天数']
train_data_2['3m_分钟_all_次数'] = train_data_2['过去三个月的平均每月使用分钟数'] / train_data_2['客户整个生命周期内的平均每月通话次数']
train_data_2['6m_分钟_all_次数'] = train_data_2['过去六个月的平均每月使用分钟数'] / train_data_2['客户整个生命周期内的平均每月通话次数']
'''


# In[28]:


where_are_inf = np.isinf(train_data_2)
train_data_2[where_are_inf] = np.nan


# In[29]:


#train_data_2[np.isinf(train_data_2)] = np.nan


# In[30]:


'''
#构建新特征
test_data_2['RFM_3m'] = test_data_2['过去三个月的平均月费用']/(test_data_2['过去三个月的平均每月使用分钟数'] * test_data_2['过去三个月的平均每月通话次数'] )
test_data_2['RFM_6m'] = test_data_2['过去六个月的平均月费用']/(test_data_2['过去六个月的平均每月使用分钟数'] * test_data_2['过去六个月的平均每月通话次数'] )
test_data_2['RFM_sum'] = test_data_2['客户生命周期内的总费用']/(test_data_2['客户生命周期内的总通话次数'] * test_data_2['客户生命周期内的总使用分钟数'])
test_data_2['RFM_over'] =  test_data_2['计费调整后的总费用']/(test_data_2['计费调整后的总分钟数'] * test_data_2['计费调整后的呼叫总数'])

test_data_2['mv_3m'] = test_data_2['过去三个月的平均月费用']/test_data_2['过去三个月的平均每月使用分钟数'] 
test_data_2['mv_6m'] = test_data_2['过去六个月的平均月费用']/test_data_2['过去六个月的平均每月使用分钟数'] 
test_data_2['mv_sum'] = test_data_2['客户生命周期内的总费用']/test_data_2['客户生命周期内的总通话次数'] 
test_data_2['mv_over'] = test_data_2['计费调整后的总分钟数'] / test_data_2['计费调整后的呼叫总数']



test_data_2['3m_天数'] = test_data_2['过去三个月的平均月费用']/test_data_2['当前设备使用天数'] 
test_data_2['6m_天数'] = test_data_2['过去六个月的平均月费用']/test_data_2['当前设备使用天数']  
test_data_2['all_天数'] = test_data_2['客户生命周期内的总费用']/test_data_2['当前设备使用天数'] 
test_data_2['over_天数'] = test_data_2['计费调整后的总费用']/test_data_2['当前设备使用天数'] 
test_data_2['3m_分钟_all_次数'] = test_data_2['过去三个月的平均每月使用分钟数'] / test_data_2['客户整个生命周期内的平均每月通话次数']
test_data_2['6m_分钟_all_次数'] = test_data_2['过去六个月的平均每月使用分钟数'] / test_data_2['客户整个生命周期内的平均每月通话次数']
'''


# In[31]:


where_are_inf = np.isinf(test_data_2)
test_data_2[where_are_inf] = np.nan
#test_data_2[np.isinf(test_data_2)] = np.nan


# In[32]:


'''
#数值分箱
day_labels = [i for i in range(5)]
day_col = ['当前设备使用天数', '当前手机价格']
for col in day_col:
    train_data_2[col + "bin"] = pd.cut(train_data_2[col], 5, labels=day_labels)
'''


# In[33]:


'''
#数值分箱
day_labels = [i for i in range(5)]
day_col = ['当前设备使用天数', '当前手机价格']
for col in day_col:
    test_data_2[col + "bin"] = pd.cut(test_data_2[col], 5, labels=day_labels)
'''


# In[34]:


train_data_2.describe()


# In[35]:


stats = []
for col in train_data_2.columns:
    stats.append((col,train_data_2[col].nunique(),
                  train_data_2[col].isnull().sum()*100 / train_data_2.shape[0],
                  train_data_2[col].value_counts(normalize=True,
                  dropna=False).values[0]*100,train_data_2[col].dtype))
    stats_df = pd.DataFrame(stats,columns=['Feature','Unique_values',
                            'Percentage of missing values',
                            'Percentage of values in the biggest category','type'])
stats_df.sort_values('Percentage of missing values',ascending=False)[:113]


# In[36]:


#train_data=train_data.fillna(train_data.mean())
#test_data=test_data.fillna(test_data.mean())


# In[37]:


train_data_2.to_csv('../user_data/train_data_F.csv',index=False)
test_data_2.to_csv('../user_data/test_data_F.csv',index=False)


# In[ ]:




