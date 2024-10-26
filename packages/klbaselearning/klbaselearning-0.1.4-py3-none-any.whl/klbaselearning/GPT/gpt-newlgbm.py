import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score
import lightgbm as lgb

# 加载数据
# 假设数据包含 "customer_id", "features...", "target" 列，其中 "target" 表示用户是否流失
data = pd.read_csv('broadband_churn.csv')

# 数据预处理
# 填充缺失值（这里使用均值填充，也可以根据具体情况选择其他策略）
for column in data.columns:
    if data[column].isnull().sum() > 0:
        if data[column].dtype == 'object':
            data[column].fillna(data[column].mode()[0], inplace=True)
        else:
            data[column].fillna(data[column].mean(), inplace=True)

# 特征与标签分离
features = data.drop(columns=['customer_id', 'target'])
target = data['target']

# LightGBM参数设置
params = {
    'objective': 'binary',
    'boosting_type': 'gbdt',
    'metric': 'binary_logloss',
    'learning_rate': 0.05,
    'num_leaves': 31,
    'max_depth': -1,
    'min_data_in_leaf': 20,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1
}

# 5折交叉验证
kf = KFold(n_splits=5, shuffle=True, random_state=42)
oof_preds = np.zeros(features.shape[0])
oof_labels = np.zeros(features.shape[0])

for fold, (train_idx, val_idx) in enumerate(kf.split(features)):
    print(f'Fold {fold + 1}')
    X_train, X_val = features.iloc[train_idx], features.iloc[val_idx]
    y_train, y_val = target.iloc[train_idx], target.iloc[val_idx]
    
    # 创建LightGBM数据集
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
    
    # 训练模型
    model = lgb.train(params, train_data, valid_sets=[train_data, val_data],
                      num_boost_round=1000, early_stopping_rounds=50, verbose_eval=100)
    
    # 预测验证集
    val_preds = model.predict(X_val, num_iteration=model.best_iteration)
    val_preds_binary = (val_preds >= 0.5).astype(int)
    oof_preds[val_idx] = val_preds
    oof_labels[val_idx] = val_preds_binary

# 计算整体F1分数
f1 = f1_score(target, oof_labels)
print(f'Overall F1 Score: {f1:.4f}')
