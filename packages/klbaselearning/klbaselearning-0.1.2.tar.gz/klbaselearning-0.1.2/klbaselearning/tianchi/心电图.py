#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

# 加载数据集
data = pd.read_csv('ecg_data.csv')  # 假设数据文件为 'ecg_data.csv'
print(data.head())

# 假设数据包含多个特征列和目标列 'target'，0表示正常，1表示异常
X = data.drop(columns=['target'])
y = data['target']

# 检查缺失值并填充
X.fillna(X.median(), inplace=True)
# 添加统计特征作为模型输入特征
X['mean'] = X.mean(axis=1)
X['std'] = X.std(axis=1)
X['max'] = X.max(axis=1)
X['min'] = X.min(axis=1)

# 进一步可以使用滑动窗口提取特征、频域分析（FFT）、小波变换等进行特征提取
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LightGBM参数设置
params = {
    'objective': 'binary',  # 二分类任务
    'boosting_type': 'gbdt',  # GBDT作为提升方法
    'metric': 'binary_error',  # 评价指标为分类错误率
    'num_leaves': 31,  # 每棵树的最大叶子节点数
    'learning_rate': 0.05,  # 学习率
    'feature_fraction': 0.9  # 每次迭代中使用的特征比例
}

# 转换数据为LightGBM数据集
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# 训练LightGBM模型
model = lgb.train(params, train_data, valid_sets=[valid_data], num_boost_round=100, early_stopping_rounds=10)

# 对测试集进行预测
y_pred_prob = model.predict(X_test, num_iteration=model.best_iteration)
y_pred = [1 if prob > 0.5 else 0 for prob in y_pred_prob]

# 评估模型性能
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print(f'F1 Score: {f1:.2f}')



#基于LSTM的心电分类模型 Baseline（简化版）
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# 准备数据，假设我们已经将数据标准化为 NumPy 数组
X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.long)
X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.long)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 定义LSTM模型
class ECG_LSTM(nn.Module):
    def __init__(self):
        super(ECG_LSTM, self).__init__()
        self.lstm = nn.LSTM(input_size=X_train.shape[1], hidden_size=50, num_layers=2, batch_first=True)
        self.fc = nn.Linear(50, 2)  # 输出二分类

    def forward(self, x):
        h0 = torch.zeros(2, x.size(0), 50)  # 隐藏层初始化
        c0 = torch.zeros(2, x.size(0), 50)  # 记忆单元初始化
        out, _ = self.lstm(x, (h0, c0))
        out = out[:, -1, :]
        out = self.fc(out)
        return out

# 初始化模型、损失函数和优化器
model = ECG_LSTM()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练LSTM模型
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        outputs = model(X_batch.unsqueeze(1))  # 需要增加一个维度作为时间步长
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

