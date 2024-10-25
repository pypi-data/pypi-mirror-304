#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 加载保险费用示例数据集
from pycaret.datasets import get_data
data = get_data(dataset='./datasets/insurance', verbose=False)
# 从网络下载
# data = get_data(dataset='insurance', verbose=False)


# In[ ]:


# 创建数据管道
from pycaret.regression import RegressionExperiment
s = RegressionExperiment()
# 预测charges列
s.setup(data, target = 'charges', session_id = 0)
# 另一种数据管道创建方式
# from pycaret.regression import *
# s = setup(data, target = 'charges', session_id = 0)


# In[ ]:


# 评估各类模型
best = s.compare_models()


# In[ ]:


print(best)


# In[ ]:


GradientBoostingRegressor(alpha=0.9, ccp_alpha=0.0, criterion='friedman_mse',
                          init=None, learning_rate=0.1, loss='squared_error',
                          max_depth=3, max_features=None, max_leaf_nodes=None,
                          min_impurity_decrease=0.0, min_samples_leaf=1,
                          min_samples_split=2, min_weight_fraction_leaf=0.0,
                          n_estimators=100, n_iter_no_change=None,
                          random_state=0, subsample=1.0, tol=0.0001,
                          validation_fraction=0.1, verbose=0, warm_start=False)

