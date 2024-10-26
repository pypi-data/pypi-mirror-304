import pandas as pd
import numpy as np
from pycaret.regression import *

# 加载数据
# 假设数据包含 "customer_id", "features...", "traffic" 列，其中 "traffic" 表示用户的电信流量
data = pd.read_csv('telecom_traffic.csv')

# 数据预处理
# 填充缺失值（这里使用均值填充，也可以根据具体情况选择其他策略）
for column in data.columns:
    if data[column].isnull().sum() > 0:
        if data[column].dtype == 'object':
            data[column].fillna(data[column].mode()[0], inplace=True)
        else:
            data[column].fillna(data[column].mean(), inplace=True)

# 初始化PyCaret环境
# 使用所有参数的示例
setup(
    data=data, 
    target='traffic', 
    ignore_features=['customer_id'], 
    train_size=0.7, 
    normalize=True, 
    normalize_method='zscore', 
    transformation=True, 
    transformation_method='yeo-johnson', 
    handle_unknown_categorical=True, 
    unknown_categorical_method='most_frequent', 
    pca=False, 
    pca_method='linear', 
    feature_selection=True, 
    feature_selection_method='classic', 
    remove_multicollinearity=True, 
    multicollinearity_threshold=0.9, 
    bin_numeric_features=[], 
    polynomial_features=False, 
    trigonometry_features=False, 
    group_features=None, 
    feature_interaction=False, 
    feature_ratio=False, 
    fix_imbalance=False, 
    fix_imbalance_method=None, 
    data_split_shuffle=True, 
    data_split_stratify=False, 
    fold_strategy='kfold', 
    fold=10, 
    session_id=42, 
    silent=True, 
    use_gpu=False
)

# 比较所有模型
best_model = compare_models(
    fold=5, 
    round=4, 
    sort='R2', 
    n_select=3, 
    exclude=None, 
    include=None, 
    turbo=True
)

# 创建模型
model = create_model(
    estimator='rf', 
    fold=5, 
    round=4, 
    cross_validation=True, 
    verbose=True, 
    probability_threshold=None
)

# 调优模型
tuned_model = tune_model(
    estimator=model, 
    fold=5, 
    round=4, 
    n_iter=10, 
    optimize='R2', 
    custom_grid=None, 
    choose_better=False, 
    verbose=True
)

# 使用最佳模型进行预测
final_model = finalize_model(tuned_model)

# 对测试集或新数据进行预测
# 假设要预测的数据在 "new_data.csv"
new_data = pd.read_csv('new_data.csv')
predictions = predict_model(
    estimator=final_model, 
    data=new_data, 
    probability_threshold=0.5, 
    round=4, 
    verbose=True
)
print(predictions)
