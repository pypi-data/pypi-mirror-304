#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#1. 数据预处理模块
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# 假设从FTP服务器下载到的数据文件名为 'train.csv' 和 'test.csv'
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# 查看数据结构
print(train_data.head())

# 数据清洗
# 填充缺失值（这里用中位数填充）
train_data.fillna(train_data.median(), inplace=True)
test_data.fillna(test_data.median(), inplace=True)

# 假设有需要转换为数值的分类特征
for column in train_data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    train_data[column] = le.fit_transform(train_data[column])
    test_data[column] = le.transform(test_data[column])

# 分离特征和标签
X = train_data.drop(columns=['target'])  # 假设目标变量名为 'target'
y = train_data['target']

# 拆分训练集和验证集
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
test_data = scaler.transform(test_data)

#2. 分类任务 - 使用sklearn的随机森林
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 使用随机森林分类器
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 验证模型
y_valid_pred = clf.predict(X_valid)
accuracy = accuracy_score(y_valid, y_valid_pred)
print(f'Validation Accuracy: {accuracy:.2f}')

# 对测试数据进行推理
y_test_pred = clf.predict(test_data)

# 保存结果
submission = pd.DataFrame({
    'id': range(len(y_test_pred)),  # 假设需要一个 'id' 列来标识数据
    'target': y_test_pred
})
submission.to_csv('submission.csv', index=False)
#3. 回归任务 - 使用sklearn的线性回归
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 使用线性回归模型
reg = LinearRegression()
reg.fit(X_train, y_train)

# 验证模型
y_valid_pred = reg.predict(X_valid)
mse = mean_squared_error(y_valid, y_valid_pred)
print(f'Validation MSE: {mse:.2f}')

# 对测试数据进行推理
y_test_pred = reg.predict(test_data)

# 保存结果
submission = pd.DataFrame({
    'id': range(len(y_test_pred)),
    'target': y_test_pred
})
submission.to_csv('submission.csv', index=False)
#4. 聚类任务 - 使用K-Means
from sklearn.cluster import KMeans

# 使用K-Means进行聚类
kmeans = KMeans(n_clusters=3, random_state=42)  # 假设我们不知道类别数，可以尝试几个不同的值
kmeans.fit(X_train)

# 对测试数据进行聚类
y_test_pred = kmeans.predict(test_data)

# 保存结果
submission = pd.DataFrame({
    'id': range(len(y_test_pred)),
    'cluster': y_test_pred
})
submission.to_csv('submission.csv', index=False)
#5. 无监督学习 - 使用PCA降维
from sklearn.decomposition import PCA

# 使用PCA将数据降到2个主成分
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_valid_pca = pca.transform(X_valid)
test_data_pca = pca.transform(test_data)

# 将降维后的数据用于训练分类器
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_pca, y_train)

# 验证模型
y_valid_pred = clf.predict(X_valid_pca)
accuracy = accuracy_score(y_valid, y_valid_pred)
print(f'Validation Accuracy (PCA): {accuracy:.2f}')

# 对测试数据进行推理
y_test_pred = clf.predict(test_data_pca)

# 保存结果
submission = pd.DataFrame({
    'id': range(len(y_test_pred)),
    'target': y_test_pred
})
submission.to_csv('submission.csv', index=False)
#6. 结果上传到FTP服务器
from ftplib import FTP

# FTP连接信息
ftp_server = 'ftp.example.com'
ftp_user = 'your_username'
ftp_pass = 'your_password'

# 上传文件
ftp = FTP(ftp_server)
ftp.login(ftp_user, ftp_pass)

with open('submission.csv', 'rb') as f:
    ftp.storbinary('STOR /target_directory/submission.csv', f)

ftp.quit()
#1. 数据收集与读取
import pandas as pd

# 从CSV文件读取数据
data = pd.read_csv('data.csv')

# 从Excel文件读取数据
data = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 从SQL数据库读取数据
import sqlite3
conn = sqlite3.connect('example.db')
data = pd.read_sql_query("SELECT * FROM table_name", conn)
#2. 数据清洗与处理
# 处理缺失值
data.fillna(data.median(), inplace=True)  # 使用中位数填充缺失值

# 删除缺失值
data.dropna(inplace=True)

# 转换数据类型
data['column'] = data['column'].astype('float')

# 去除异常值（如Z-score大于3的点）
from scipy import stats
import numpy as np
data = data[(np.abs(stats.zscore(data.select_dtypes(include=['float', 'int']))) < 3).all(axis=1)]
#3. 特征工程
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

# 标签编码
label_encoder = LabelEncoder()
data['category_column'] = label_encoder.fit_transform(data['category_column'])

# 标准化特征
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data.select_dtypes(include=['float', 'int']))

# Min-Max归一化
minmax_scaler = MinMaxScaler()
data_normalized = minmax_scaler.fit_transform(data.select_dtypes(include=['float', 'int']))
#4. 特征选择
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier

# 使用方差选择法选择K个最优特征
X = data.drop(columns=['target'])
y = data['target']
X_new = SelectKBest(f_classif, k=5).fit_transform(X, y)

# 基于特征重要性（使用随机森林）
model = RandomForestClassifier()
model.fit(X, y)
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance', ascending=False)
print(feature_importance_df)
#5. 数据集拆分
from sklearn.model_selection import train_test_split

X = data.drop(columns=['target'])
y = data['target']

# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#6. 模型训练
from sklearn.ensemble import RandomForestClassifier

# 使用随机森林进行分类训练
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
#7. 模型评估
from sklearn.metrics import accuracy_score, mean_squared_error

# 对测试集进行预测
y_pred = model.predict(X_test)

# 分类任务的准确率
print("Accuracy:", accuracy_score(y_test, y_pred))

# 回归任务的均方误差（如果是回归任务）
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
#9. 模型保存与加载
import joblib

# 保存模型
joblib.dump(model, 'random_forest_model.pkl')

# 加载模型
loaded_model = joblib.load('random_forest_model.pkl')

# 使用加载的模型进行预测
y_loaded_pred = loaded_model.predict(X_test)
#10. 推理与结果保存
# 对测试数据进行推理
y_test_pred = model.predict(X_test)

# 保存结果
submission = pd.DataFrame({
    'id': range(len(y_test_pred)),  # 假设需要一个 'id' 列来标识数据
    'target': y_test_pred
})
submission.to_csv('submission.csv', index=False)
11. FTP 上传预测结果
from ftplib import FTP

# FTP服务器连接信息
ftp = FTP('ftp.example.com')
ftp.login(user='username', passwd='password')

# 上传结果文件
with open('submission.csv', 'rb') as file:
    ftp.storbinary('STOR /path/on/ftp/submission.csv', file)

ftp.quit()
#1. 多表合并操作
#1.1 内连接（Inner Join） 内连接是将两个表中满足连接条件的行合并，只保留两个表中共有的部分。内连接仅保留ID在两个表中均存在的行。因此，结果只包含ID=3和ID=4的行。
import pandas as pd

# 创建两个数据表
data1 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Score': [85, 92, 78, 90]
})

data2 = pd.DataFrame({
    'ID': [3, 4, 5, 6],
    'Subject': ['Math', 'English', 'Science', 'History'],
    'Grade': ['A', 'B', 'C', 'B']
})

# 使用内连接（根据ID列）
result_inner = pd.merge(data1, data2, on='ID', how='inner')
print("Inner Join Result:")
print(result_inner)
#1.2 左连接（Left Join）左连接保留左表中的所有数据，并将右表中符合条件的数据合并进来，右表中没有匹配的数据用NaN填充。左连接会保留data1中的所有行，如果data2中有匹配的ID，则将数据合并，否则填充NaN。
# 使用左连接（根据ID列）
result_left = pd.merge(data1, data2, on='ID', how='left')
print("\nLeft Join Result:")
print(result_left)
#1.4 全连接（Outer Join） 全连接保留两个表中的所有数据，缺失的部分用NaN填充。
# 使用全连接（根据ID列）
result_outer = pd.merge(data1, data2, on='ID', how='outer')
print("\nOuter Join Result:")
print(result_outer)
#2. 按列或按行合并
#有时候需要合并两个具有相同行或列的数据表，可以使用concat()。当两个数据表具有相同的行索引时，可以按列合并，增加新的特征。
# 按列合并两个表
concat_columns = pd.concat([data1, data2], axis=1)
print("\nConcatenate by Columns Result:")
print(concat_columns)
#当两个数据表的结构（列名）相同时，可以按行合并，堆叠数据。
# 创建两个具有相同列的数据表
data3 = pd.DataFrame({
    'ID': [5, 6],
    'Name': ['Eve', 'Frank'],
    'Score': [88, 75]
})

# 按行合并两个表
concat_rows = pd.concat([data1, data3], axis=0)
print("\nConcatenate by Rows Result:")
print(concat_rows)
#以下是一个结合多表操作进行机器学习任务的完整示例：
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 创建两个数据表（模拟比赛数据）
data_users = pd.DataFrame({
    'UserID': [1, 2, 3, 4],
    'Age': [24, 30, 22, 40],
    'Gender': ['F', 'M', 'M', 'F']
})

data_scores = pd.DataFrame({
    'UserID': [1, 2, 3, 5],
    'Score': [85, 92, 78, 70]
})

# 多表合并：根据UserID进行左连接
merged_data = pd.merge(data_users, data_scores, on='UserID', how='left')

# 处理缺失值
merged_data.fillna(merged_data.median(), inplace=True)

# 特征工程：标签编码
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
merged_data['Gender'] = label_encoder.fit_transform(merged_data['Gender'])

# 分离特征和标签
X = merged_data.drop(columns=['UserID', 'Score'])
y = merged_data['Score']

# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 使用随机森林进行训练
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 验证模型
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))













