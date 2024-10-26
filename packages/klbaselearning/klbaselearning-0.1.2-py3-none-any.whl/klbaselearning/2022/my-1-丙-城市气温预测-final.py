#!/usr/bin/env python
# coding: utf-8

# <font color=black size=5 face=雅黑>**Step 1:导入函数工具箱**</font>
# 

# In[ ]:


from sklearn.decomposition import PCA #主成分分析法
import pandas as pd 
import numpy as np
from prophet import Prophet
from pandas.plotting import register_matplotlib_converters
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import filterData, delData, fillNanList, dropDuplicate,\
    handleOutlier, minMaxScale, cate2Num,standardizeData,\
    discrete, tran_math_function, minMaxScale, standardizeData,\
    onehot_map, map_dict_tran, binary_map, pca_selection,dfs_feature,\
    continue_time, discrete_time, statistics_time
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from statsmodels.tsa.stattools import *
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.linear_model import Ridge
from sklearn import linear_model


# <font color=black size=5 face=雅黑>**Step 2:读取数据**</font>
# 

# In[ ]:


#new_train_data = pd.read_csv('datasets/@huangzx23#3eb493098a9258fca92f4758cbbc0dcd/E_test.csv')
new_train_data = pd.read_csv('/home/bwfy/桌面/比赛赛集/E_test.csv')
A_train = pd.read_csv('/home/bwfy/桌面/比赛赛集/A.csv')
B_train = pd.read_csv('/home/bwfy/桌面/比赛赛集/B.csv')
C_train = pd.read_csv('/home/bwfy/桌面/比赛赛集/C.csv')
D_train = pd.read_csv('/home/bwfy/桌面/比赛赛集/D.csv')
new_train_data.head()


# <font color=black size=5 face=雅黑>**Step 3:数据预处理**</font>
# 

# <font color=black size=3 face=雅黑>**3.1:ADF平稳性检测**</font>
# 

# In[ ]:


new_train_data_1 =new_train_data.copy()


# In[ ]:


result1 = adfuller(new_train_data_1['AvgTemperature'])
result2 = adfuller(A_train['AvgTemperature'])
result3 = adfuller(B_train['AvgTemperature'])
result4 = adfuller(C_train['AvgTemperature'])
result5 = adfuller(D_train['AvgTemperature'])
print(result1)
print(result2)
print(result3)
print(result4)
print(result5)


# In[ ]:


print(result1)


# <font color=black size=3 face=雅黑>**Step 3.2:自相关图平稳性swim**</font>

# In[ ]:


fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)

ax1.plot(new_train_data_1['AvgTemperature'])
ax1.set_title('E_test')
plot_acf(new_train_data_1['AvgTemperature'], ax=ax2)
plot_pacf(new_train_data_1['AvgTemperature'], ax=ax3)
plt.show()


# In[ ]:


fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)

ax1.plot(A_train['AvgTemperature'])
ax1.set_title('A_train')
plot_acf(A_train['AvgTemperature'], ax=ax2)
plot_pacf(A_train['AvgTemperature'], ax=ax3)
plt.show()


# In[ ]:


fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)

ax1.plot(B_train['AvgTemperature'])
ax1.set_title('B_train')
plot_acf(B_train['AvgTemperature'], ax=ax2)
plot_pacf(B_train['AvgTemperature'], ax=ax3)
plt.show()


# In[ ]:


fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)

ax1.plot(C_train['AvgTemperature'])
ax1.set_title('C_train')
plot_acf(C_train['AvgTemperature'], ax=ax2)
plot_pacf(C_train['AvgTemperature'], ax=ax3)
plt.show()


# In[ ]:


fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)

ax1.plot(D_train['AvgTemperature'])
ax1.set_title('D_train')
plot_acf(D_train['AvgTemperature'], ax=ax2)
plot_pacf(D_train['AvgTemperature'], ax=ax3)
plt.show()


# <font color=black size=3 face=雅黑>**3.2:Box-Pierce检验平稳性swim**</font>

# In[ ]:


from statsmodels.stats.diagnostic import acorr_ljungbox
# 随机种子
np.random.seed(123)
# 生成白噪声序列
#white_noise=np.random.standard_normal(size=1000)
# 白噪声检验，想要查看QBP检验统计量的结果需要指定boxpierce参数为True
# 不指定boxpierce参数，默认返回QLB检验统计量的结果
res = acorr_ljungbox(new_train_data_1['AvgTemperature'], lags=24, boxpierce=True, return_df=True)
print(res)

# 根据检验统计量值查表
# from scipy import stats
# print(stats.chi2.sf(18.891607, 20))
#我们这里只看检验统计量下检验效果，即最后两列。可以可看到，各延迟阶数下的p值均小于0.05，拒绝原假设，序列非白噪声。


# <font color=black size=3 face=雅黑>**3.3 异常值处理**</font>

# In[ ]:


#格式化各数据集
new_train_data_1['ds']=new_train_data_1['Year'].astype('str').str.cat(new_train_data_1['Month'].astype('str'),sep='-')
new_train_data_1['ds']=new_train_data_1['ds'].astype('str').str.cat(new_train_data_1['Day'].astype('str'),sep='-')

A_train['ds']=A_train['Year'].astype('str').str.cat(A_train['Month'].astype('str'),sep='-')
A_train['ds']=A_train['ds'].astype('str').str.cat(A_train['Day'].astype('str'),sep='-')

B_train['ds']=B_train['Year'].astype('str').str.cat(B_train['Month'].astype('str'),sep='-')
B_train['ds']=B_train['ds'].astype('str').str.cat(B_train['Day'].astype('str'),sep='-')

C_train['ds']=C_train['Year'].astype('str').str.cat(C_train['Month'].astype('str'),sep='-')
C_train['ds']=C_train['ds'].astype('str').str.cat(C_train['Day'].astype('str'),sep='-')

D_train['ds']=D_train['Year'].astype('str').str.cat(D_train['Month'].astype('str'),sep='-')
D_train['ds']=D_train['ds'].astype('str').str.cat(D_train['Day'].astype('str'),sep='-')

import datetime
new_train_data_1['ds']=new_train_data_1['ds'].map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d '))
A_train['ds']=A_train['ds'].map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d '))
B_train['ds']=B_train['ds'].map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d '))
C_train['ds']=C_train['ds'].map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d '))
D_train['ds']=D_train['ds'].map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d '))

new_train_data_1.drop(["Month","Day","Year"],axis=1,inplace=True)
A_train.drop(["Month","Day","Year"],axis=1,inplace=True)
B_train.drop(["Month","Day","Year"],axis=1,inplace=True)
C_train.drop(["Month","Day","Year"],axis=1,inplace=True)
D_train.drop(["Month","Day","Year"],axis=1,inplace=True)


new_train_data_1.rename(columns={'AvgTemperature':'y'}, inplace=True)#将原来的命名修改为算法要求的命名
A_train.rename(columns={'AvgTemperature':'y'}, inplace=True)#将原来的命名修改为算法要求的命名
B_train.rename(columns={'AvgTemperature':'y'}, inplace=True)#将原来的命名修改为算法要求的命名
C_train.rename(columns={'AvgTemperature':'y'}, inplace=True)#将原来的命名修改为算法要求的命名
D_train.rename(columns={'AvgTemperature':'y'}, inplace=True)#将原来的命名修改为算法要求的命名


new_train_data_1.head()


# In[ ]:


print(new_train_data_1)


# In[ ]:


new_train_data_1 = new_train_data_1.drop_duplicates(subset=['ds']) #丢弃重复
A_train = A_train.drop_duplicates(subset=['ds']) #丢弃重复
B_train = B_train.drop_duplicates(subset=['ds']) #丢弃重复
C_train = C_train.drop_duplicates(subset=['ds']) #丢弃重复
D_train = D_train.drop_duplicates(subset=['ds']) #丢弃重复


# In[ ]:


print(new_train_data_1)


# In[ ]:


print(A_train)


# In[ ]:


#将异常值赋值为NAN
new_train_data_1['y']  = new_train_data_1['y'].where(new_train_data_1['y'] > 0 , np.nan)
A_train['y']  = A_train['y'].where(A_train['y'] > 0 , np.nan)
B_train['y']  = B_train['y'].where(B_train['y'] > 0 , np.nan)
C_train['y']  = C_train['y'].where(C_train['y'] > 0 , np.nan)
D_train['y']  = D_train['y'].where(D_train['y'] > 0 , np.nan)


# In[ ]:


new_train_data_1 = new_train_data_1.fillna(method = "bfill").fillna(method = "pad")
A_train = A_train.fillna(method = "bfill").fillna(method = "pad")
B_train = B_train.fillna(method = "bfill").fillna(method = "pad")
C_train = C_train.fillna(method = "bfill").fillna(method = "pad")
D_train = D_train.fillna(method = "bfill").fillna(method = "pad")


# In[ ]:


"""function to detect outliers based on the predictions of a model"""
def find_outliers(model, X, y, sigma=3):
    # predict y values using model
    try:
        y_pred = pd.Series(model.predict(X), index=y.index)
    # if predicting fails, try fitting the model first
    except:
        model.fit(X, y)
        y_pred = pd.Series(model.predict(X), index=y.index)
 
    # calculate residuals between the model prediction and true y values
    resid = y - y_pred
    mean_resid = resid.mean()
    std_resid = resid.std()
 
    # calculate z statistic, define outliers to be where |z|>sigma
    z = (resid - mean_resid) / std_resid
    #找出方差大于3的数据的索引，然后丢掉
    outliers = z[abs(z) > sigma].index
 
    # print and plot the results
    print('score=', model.score(X, y))
    
    print("mse=", mean_squared_error(y, y_pred))
    print('---------------------------------------')
 
    print('mean of residuals:', mean_resid)
    print('std of residuals:', std_resid)
    print('---------------------------------------')
 
    print(len(outliers), 'outliers:')
    print(outliers.tolist())
 
    plt.figure(figsize=(15, 5))
    ax_131 = plt.subplot(1,3,1)
    plt.plot(y,y_pred,'.')
    plt.plot(y.loc[outliers],y_pred.loc[outliers],'ro')
    plt.legend(['Accepted','Outlier'])
    plt.xlabel('y')
    plt.ylabel('y_pred');
    
    ax_132=plt.subplot(1,3,2)
    plt.plot(y,y-y_pred,'.')
    plt.plot(y.loc[outliers],y.loc[outliers]-y_pred.loc[outliers],'ro')
    plt.legend(['Accepted','Outlier'])
    plt.xlabel('y')
    plt.ylabel('y - y_pred');
    
    ax_133 = plt.subplot(1,3,3)
    z.plot.hist(bins=50,ax=ax_133)
    z.loc[outliers].plot.hist(color = 'r',bins = 50,ax = ax_133)
    plt.legend(['Accepted','Outlier'])
    plt.xlabel('z')
    plt.savefig('outliers.png')
    
    return outliers
 


# In[ ]:


X_train=new_train_data_1.iloc[:,0:-1]
y_train=new_train_data_1.iloc[:,-2]
outliers = find_outliers(Ridge(),X_train,y_train)


# In[ ]:


X_train=A_train.iloc[:,0:-1]
y_train=A_train.iloc[:,-2]
outliers = find_outliers(Ridge(),X_train,y_train)


# In[ ]:


X_train=B_train.iloc[:,0:-1]
y_train=B_train.iloc[:,-2]
outliers = find_outliers(Ridge(),X_train,y_train)
for col in outliers:
    B_train['y'][col]=np.nan


# In[ ]:


print(B_train)


# In[ ]:


X_train=C_train.iloc[:,0:-1]
y_train=C_train.iloc[:,-2]
outliers = find_outliers(Ridge(),X_train,y_train)
for col in outliers:
    C_train['y'][col]=np.nan


# In[ ]:


X_train=D_train.iloc[:,0:-1]
y_train=D_train.iloc[:,-2]
outliers = find_outliers(Ridge(),X_train,y_train)
for col in outliers:
    D_train['y'][col]=np.nan


# In[ ]:


new_train_data_1 = new_train_data_1.fillna(method = "bfill").fillna(method = "pad")
A_train = A_train.fillna(method = "bfill").fillna(method = "pad")
B_train = B_train.fillna(method = "bfill").fillna(method = "pad")
C_train = C_train.fillna(method = "bfill").fillna(method = "pad")
D_train = D_train.fillna(method = "bfill").fillna(method = "pad")


# In[ ]:


print(y_train)


# In[ ]:


print(new_train_data_1)


# In[ ]:


fig =plt.figure(figsize=(4,6))
sns.boxplot(new_train_data_1['y'],orient='v',width=0.5)


# In[ ]:


#A_train=handleOutlier(A_train)
fig =plt.figure(figsize=(4,6))
sns.boxplot(A_train['y'],orient='v',width=0.5)


# In[ ]:


#B_train=handleOutlier(B_train)
fig =plt.figure(figsize=(4,6))
sns.boxplot(B_train['y'],orient='v',width=0.5)


# In[ ]:


#C_train=handleOutlier(C_train)
fig =plt.figure(figsize=(4,6))
sns.boxplot(C_train['y'],orient='v',width=0.5)


# In[ ]:


#D_train=handleOutlier(D_train)
fig =plt.figure(figsize=(4,6))
sns.boxplot(D_train['y'],orient='v',width=0.5)


# In[ ]:


print(new_train_data_1['y'].max())
print(new_train_data_1['y'].min())


# In[ ]:


print(D_train)


# In[ ]:


new_train_data_1.head


# In[ ]:


new_train_data_1['add_A'] = np.nan
new_train_data_1['add_B'] = np.nan
new_train_data_1['add_C'] = np.nan
new_train_data_1['add_D'] = np.nan


# In[ ]:


train_y_new=pd.DataFrame()
train_y_new['ds'] = A_train['ds']
train_y_new['y'] = A_train['y']    
mapping = train_y_new.set_index('ds',).squeeze()
new_train_data_1['add_A'].fillna(new_train_data_1['ds'].map(mapping),inplace=True)


# In[ ]:


train_y_new=pd.DataFrame()
train_y_new['ds'] = C_train['ds']
train_y_new['y'] = C_train['y']    
mapping = train_y_new.set_index('ds',).squeeze()
new_train_data_1['add_C'].fillna(new_train_data_1['ds'].map(mapping),inplace=True)


# In[ ]:


train_y_new=pd.DataFrame()
train_y_new['ds'] = D_train['ds']
train_y_new['y'] = D_train['y']    
mapping = train_y_new.set_index('ds',).squeeze()
new_train_data_1['add_D'].fillna(new_train_data_1['ds'].map(mapping),inplace=True)


# In[ ]:


train_y_new=pd.DataFrame()
train_y_new['ds'] = B_train['ds']
train_y_new['y'] = B_train['y']    
mapping = train_y_new.set_index('ds',).squeeze()
new_train_data_1['add_B'].fillna(new_train_data_1['ds'].map(mapping),inplace=True)


# In[ ]:


print(new_train_data_1)


# In[ ]:


print(A_train)


# In[ ]:


#new_train_data['y'].loc[new_train_data['y'] < 1 ] = new_train_data['y'].mean()
print(new_train_data_1['y'].max())
print(new_train_data_1['y'].min())
#new_train_data[new_train_data['y'] < -50] = new_train_data.mean()


# In[ ]:


'''
train_data_2['y']=new_train_data['y']
feature_columns = [col for col in train_data_2.columns if col not in ['ds']]
min_max_scaler = preprocessing.MinMaxScaler()
min_max_scaler = min_max_scaler.fit(train_data_2[feature_columns])
train_data_scaler = min_max_scaler.transform(train_data_2[feature_columns])

train_data_scaler=pd.DataFrame(train_data_scaler)
train_data_scaler.rename(columns={0:'y'}, inplace = True)
train_data_scaler['ds']=new_train_data['ds']
train_data_scaler.head
'''


# In[ ]:


m =     Prophet(growth='linear',                            #趋势默认为线性增长'linear', 还有 'logistic'
       changepoints=None,                              # 默认不指定改变点，prophet会根据趋势自动搜寻潜在的改变点
       n_changepoints=25,                              #如果changepoints设置了，该参数不起作用；如果changepoints没有设置，那么改变点将在changepointrange范围内搜寻。默认设置为25
       changepoint_range=0.8,                    #changepoint_range: 范围0-1，表示改变点落在趋势中的可能的范围
       yearly_seasonality=True,                # 即数据存在年度周期性变化，拟合年度趋势。参数有'auto', 参数有'auto'、True和Fals
       weekly_seasonality=False,                    #同上
       #daily_seasonality=True,
       holidays=None,                                 #默认为None，如果要指定传入节假日数据，数据格式为dataframe，有两个指定的字段holiday和ds，其中holiday列的数据为字符串， ds列为date数据类型
       seasonality_mode='multiplicative',                   #趋势模式有'additive'和'multiplicative'，默认为加法'additive'
       seasonality_prior_scale=10,                  #趋势缩放系数，如果该参数大，会让后续趋势波动变大。如果系数较小，会抑制趋势甚至熨平趋势。默认参数设置为10
       #holidays_prior_scale=10.0,                     #类似于seasonalitypriorscale参数的作用，主要用于解释节假日对趋势波动幅度起到熨平或者加大波动强度对作用。默认也是10
       changepoint_prior_scale=0.5,                  # 类似于seasonalitypriorscale参数的作用，主要用于解释改变点对趋势波动幅度起到熨平或者加大波动强度对作用。默认是0.05
       mcmc_samples=0,                                #参数为整数。如果大于0， 模型使用贝叶斯推断；如果设置为0，使用最大后验概率估计（MAP）
       interval_width=0.8,                         #浮点数类型，为预测提供不确定性区间的宽度。如果mcmcsamples = 0，则模型使只使用MAP估计得出的趋势中的不确定性；如果mcmc.samples> 0，则将对所有模型参数进行积分，其中将包括季节性不确定性。
       uncertainty_samples=2000)                 #用于估计不确定性间隔的模拟次数，默认为1000
m.add_regressor('add_A')
m.add_regressor('add_B')
m.add_regressor('add_C')
m.add_regressor('add_D')

#new_train_data_1['cap'] = 92
#new_train_data_1['floor'] = 32 
m.add_seasonality(name='monthly', period=30.5, fourier_order=10)
forecast = m.fit(new_train_data_1).predict()
print("mse is",mean_squared_error(new_train_data_1['y'].values,forecast['yhat'].values[:len(new_train_data_1)]))


# In[ ]:


print(forecast)


# In[ ]:


def outlier_detection(forecast):
    index = np.where((forecast["yhat"] <= forecast["yhat_lower"])|
                     (forecast["yhat"] >= forecast["yhat_upper"]),True,False)
    return index
outlier_index = outlier_detection(forecast)
outlier_df = new_train_data_1[outlier_index]
print("异常值的数量为:",np.sum(outlier_index))


# In[ ]:


new_train_data_2 = new_train_data_1.copy()


# In[ ]:


#new_train_data_2 = new_train_data_2.drop(outlier_df.index) 删除index


# In[ ]:


from prophet.plot import add_changepoints_to_plot
fig = m.plot(forecast)
a = add_changepoints_to_plot(fig.gca(), m, forecast)


# In[ ]:


future  = m.make_future_dataframe(periods=1461,freq='d',include_history = True)
#from prophet.diagnostics import cross_validation
#df_cv = cross_validation(m, initial='2920 days', period='180 days', horizon = '365 days' )


# In[ ]:


#df_cv.head()
print(future)


# In[ ]:


#from prophet.diagnostics import performance_metrics
#df_p = performance_metrics(df_cv)
#df_p.head()


# In[ ]:


#from prophet.plot import plot_cross_validation_metric
#fig = plot_cross_validation_metric(df_cv, metric='mae')


# In[ ]:


print(future)


# In[ ]:


future['add_A'] = np.nan
future['add_B'] = np.nan
future['add_C'] = np.nan
future['add_D'] = np.nan


# In[ ]:


print(future)


# In[ ]:


future = A_train.copy()


# In[ ]:


print(future)


# In[ ]:


future.rename(columns={'y':'add_A'}, inplace=True)#将原来的命名修改为算法要求的命名
#future['add_A'] = A_train['y']
future['add_B'] = B_train['y']
future['add_C'] = C_train['y']
future['add_D'] = D_train['y']


# In[ ]:


#open_day='1995-01-01'
#close_day='2020-01-01'
#con1=future['ds']>=open_day
#con2=future['ds']<close_day
#future=future[con1&con2]


# In[ ]:


#future['add_A'] = A_train['y']


# In[ ]:


print(A_train)


# In[ ]:


#future['ds'] =future['ds'].apply(lambda x: x.strftime('%Y-%m-%d'))


# In[ ]:


print(future['ds'].dtype)


# In[ ]:


print(future['ds'].dtype)


# In[ ]:


#train_y_new1=pd.DataFrame()
#train_y_new1['ds'] = A_train['ds']
#train_y_new1['y'] = A_train['y']    
mapping = A_train.set_index('ds',).squeeze()
future['add_A'].fillna(future['ds'].map(mapping),inplace=True)


# In[ ]:


print(mapping)


# In[ ]:


#train_y_new1=pd.DataFrame()
#train_y_new1['ds'] = C_train['ds']
#train_y_new1['y'] = C_train['y']    
mapping = B_train.set_index('ds',).squeeze()
future['add_B'].fillna(future['ds'].map(mapping),inplace=True)


# In[ ]:


#train_y_new1=pd.DataFrame()
#train_y_new1['ds'] = D_train['ds']
#train_y_new1['y'] = D_train['y']    
mapping = C_train.set_index('ds',).squeeze()
future['add_C'].fillna(future['ds'].map(mapping),inplace=True)


# In[ ]:


#train_y_new1=pd.DataFrame()
#train_y_new1['ds'] = B_train['ds']
#train_y_new1['y'] = B_train['y']    
mapping = D_train.set_index('ds',).squeeze()
future['add_D'].fillna(future['ds'].map(mapping),inplace=True)


# In[ ]:


print(mapping)


# In[ ]:


print(future)


# In[ ]:


future = future.fillna(method = "bfill").fillna(method = "pad")


# In[ ]:


future.isnull().sum()


# In[ ]:


#future = m.make_future_dataframe(periods=1462,freq='d')
forecast = m.predict(future)


# In[ ]:


print( future)


# In[ ]:


forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# In[ ]:


fig1 = m.plot(forecast)


# In[ ]:


open_day='2016-01-01'
close_day='2020-01-01'
con1=forecast['ds']>=open_day
con2=forecast['ds']<close_day
forecast2=forecast[con1&con2]
forecast2.rename(columns={'yhat':'value'}, inplace=True)#将原来的命名修改为算法要求的命名
print(forecast2)


# In[ ]:


print(forecast2['value'].max())
print(forecast2['value'].min())


# In[ ]:


'''
forecast3=pd.DataFrame()
forecast3['value']=forecast2['value']
forecast3=min_max_scaler.inverse_transform(forecast3)

forecast3=pd.DataFrame(forecast3)
forecast3.rename(columns={0:'value'}, inplace = True)
forecast3.head
'''


# In[ ]:


forecast3 =forecast2.round(1)
forecast3['value'].to_csv('./weather_further_155.csv',index=False)


# In[ ]:


forecast_mean['c']=round(forecast_mean['c'],1)
forecast_mean['y']=round(forecast_mean['value'],1)

forecast3=pd.DataFrame()
forecast3['value'] = forecast_mean['c']
forecast3['value_2'] = forecast_mean['y']
forecast3.to_csv('./weather_further.csv',index=False)


# In[ ]:


print(forecast3['value'].max())
print(forecast3['value'].min())


# In[ ]:


print(forecast3['value_2'].max())
print(forecast3['value_2'].min())


# In[ ]:


forecast3['value_2'].to_csv('./weather_further_new.csv',index=False)

