#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#1. 分类任务的LightGBM Baseline
import lightgbm as lgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 加载数据集
data = load_iris()
X, y = data.data, data.target

# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LightGBM参数设置
params = {
    'objective': 'multiclass',  # 目标函数，'multiclass'表示多分类任务
    'num_class': 3,  # 类别数（对于多分类任务需要指定）
    'boosting_type': 'gbdt',  # 提升类型，可选：'gbdt'（梯度提升决策树），'dart'，'goss'，'rf'
    'metric': 'multi_logloss',  # 评估指标，多分类使用'logloss'，可以设置多个
    'num_leaves': 31,  # 每棵树的最大叶子节点数，取值范围：[20, 100]，影响模型复杂度
    'learning_rate': 0.05,  # 学习率，常见取值范围：[0.01, 0.3]
    'feature_fraction': 0.8,  # 每次迭代中使用的特征比例，取值范围：[0.6, 1.0]，用于防止过拟合
    'bagging_fraction': 0.8,  # 数据采样比例，取值范围：[0.5, 1.0]，用于防止过拟合
    'bagging_freq': 5,  # 每多少次迭代进行bagging，0表示不使用bagging
    'max_depth': -1,  # 最大树深，-1表示没有限制，控制模型复杂度，常用取值：[3, 12]
    'min_data_in_leaf': 20,  # 一个叶子节点上最小的样本数，用于避免过拟合
}

# 创建LightGBM的数据集
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# 训练模型
model = lgb.train(params, train_data, valid_sets=[valid_data], num_boost_round=100, early_stopping_rounds=10)

# 对测试集进行预测
y_pred = model.predict(X_test, num_iteration=model.best_iteration)
y_pred_class = [list(pred).index(max(pred)) for pred in y_pred]

# 评估模型性能
accuracy = accuracy_score(y_test, y_pred_class)
print(f'Validation Accuracy: {accuracy:.2f}')

#2. 回归任务的LightGBM Baseline
import lightgbm as lgb
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 加载数据集
data = load_boston()
X, y = data.data, data.target

# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LightGBM参数设置
params = {
    'objective': 'regression',  # 目标函数，'regression'表示回归任务
    'boosting_type': 'gbdt',  # 提升类型，可选：'gbdt'（梯度提升决策树），'dart'，'goss'，'rf'
    'metric': 'rmse',  # 评估指标，常见的有'mse', 'rmse', 'mae'等
    'num_leaves': 31,  # 每棵树的最大叶子节点数，影响模型复杂度，取值范围：[20, 100]
    'learning_rate': 0.05,  # 学习率，常见取值范围：[0.01, 0.3]
    'feature_fraction': 0.8,  # 每次迭代中使用的特征比例，防止过拟合，取值范围：[0.6, 1.0]
    'bagging_fraction': 0.8,  # 数据采样比例，防止过拟合，取值范围：[0.5, 1.0]
    'bagging_freq': 5,  # 每多少次迭代进行bagging，0表示不使用bagging
    'max_depth': -1,  # 最大树深度，-1表示没有限制，常用取值：[3, 12]
    'min_data_in_leaf': 20,  # 一个叶子节点上的最小样本数，用于避免过拟合
}

# 创建LightGBM的数据集
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# 训练模型
model = lgb.train(params, train_data, valid_sets=[valid_data], num_boost_round=100, early_stopping_rounds=10)

# 对测试集进行预测
y_pred = model.predict(X_test, num_iteration=model.best_iteration)

# 评估模型性能
mse = mean_squared_error(y_test, y_pred)
print(f'Validation Mean Squared Error: {mse:.2f}')
'''
LightGBM 常用参数说明
以下是代码中常用到的LightGBM参数的详细说明：

objective：设置模型的目标函数。

'regression'：用于回归任务。
'binary'：用于二分类任务。
'multiclass'：用于多分类任务（需要设置num_class）。
boosting_type：提升方法。

'gbdt'：梯度提升决策树（Gradient Boosting Decision Tree），常用的选择。
'dart'：Dropouts meet Multiple Additive Regression Trees。
'goss'：Gradient-based One-Side Sampling。
'rf'：随机森林。
num_leaves：每棵树的最大叶子节点数。

取值范围通常为[20, 100]。值越大，模型越复杂，可能容易过拟合。
learning_rate：学习率。

通常设置为[0.01, 0.3]之间的小值。学习率较小时，需要更多的树，但模型可能更加稳健。
feature_fraction：每次迭代中使用的特征比例。

通常设置为[0.6, 1.0]。用于防止过拟合。
bagging_fraction：每次迭代中使用的数据比例。

通常设置为[0.5, 1.0]，通常结合bagging_freq使用，用于防止过拟合。
bagging_freq：Bagging的频率。

每n次迭代进行一次bagging操作。0表示不进行bagging。
max_depth：树的最大深度。

-1表示没有限制。一般控制在[3, 12]之间，用于防止过拟合。
min_data_in_leaf：一个叶子上最小的数据量。

防止生成过于细小的叶子节点，避免过拟合。常见取值范围为[10, 50]。
metric：评估指标。

'multi_logloss'：多分类的交叉熵损失。
'rmse'、'mae'等用于回归任务。
'''

