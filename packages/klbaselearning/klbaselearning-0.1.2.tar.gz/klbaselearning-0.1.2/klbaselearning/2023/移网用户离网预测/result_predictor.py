#!/usr/bin/env python
# coding: utf-8

# In[1]:


from autogluon.tabular import TabularDataset,TabularPredictor
import os
import pandas as pd
import numpy as np
os.environ["NUMEXPR_MAX_THREADS"] = '20'


# In[2]:


# 导入数据  
print("Loading Data ... ")  
test_data = pd.read_csv('../user_data/test_data_F.csv')#在特征工程代码中生成的中间文件
test_data_2 = test_data.copy()


# In[3]:


test_data_2 = test_data_2.drop(['客户ID'], axis=1)


# In[4]:


predictor=TabularPredictor.load("../user_data/ag-20220707_184911_best97079")


# In[5]:


pred_test=predictor.predict_proba(test_data_2)#,model='LightGBM'


# In[6]:


test_data['是否流失'] = pred_test[1]

test_data[['客户ID','是否流失']].to_csv('../prediction_result/resul.csv', index=False)


# In[ ]:




