#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 导入珠宝数据集
from pycaret.datasets import get_data
# 根据数据集特征进行聚类
data = get_data('./datasets/jewellery')
# data = get_data('jewellery')


# In[ ]:


# 创建数据管道
from pycaret.clustering import ClusteringExperiment
s = ClusteringExperiment()
# normalize归一化数据
s.setup(data, normalize = True, verbose = False)
# 另一种数据管道创建方式
# from pycaret.clustering import *
# s = setup(data, normalize = True)


# In[ ]:


#PyCaret在聚类任务中提供create_model选择合适的方法来构建聚类模型，而不是全部比较。
kmeans = s.create_model('kmeans')
#create_model函数支持的聚类方法如下：
s.models()
print(kmeans)
# 查看聚类数
print(kmeans.n_clusters)


# In[ ]:


# jupyter环境下交互可视化展示
# s.evaluate_model(kmeans)


# In[ ]:


# 结果可视化 
# 'cluster' - Cluster PCA Plot (2d)
# 'tsne' - Cluster t-SNE (3d)
# 'elbow' - Elbow Plot
# 'silhouette' - Silhouette Plot
# 'distance' - Distance Plot
# 'distribution' - Distribution Plot
s.plot_model(kmeans, plot = 'elbow')


# In[ ]:


#为训练数据分配聚类标签：
result = s.assign_model(kmeans)
result.head()


# In[ ]:


#为新的数据进行标签分配：
predictions = s.predict_model(kmeans, data = data)
predictions.head()


# In[ ]:




