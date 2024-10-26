#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns


# In[ ]:


train_data = pd.read_csv("5G移动用户使用预测挑战赛公开数据/train.csv")
test_data = pd.read_csv("5G移动用户使用预测挑战赛公开数据/test.csv")


# In[ ]:


sns.heatmap(train_data.corr().round(3))


# In[ ]:


train_data.corr().round(3).target.iloc[:-1].plot(kind='barh', figsize=(10, 10))


# In[ ]:


train_data['target'].value_counts()


# In[ ]:


train_data.isnull().mean(0)


# In[ ]:


import lightgbm as lgb

m = lgb.LGBMClassifier()
m.fit(
    train_data.drop(['id', 'target'], axis=1),
    train_data['target']
)


# In[ ]:


pd.DataFrame(
    {
        "id": test_data['id'],
        "target": m.predict_proba(test_data.drop(['id'], axis=1))[:, 1].round(4)
    }
).to_csv('submit.csv', index=None)


# In[ ]:




