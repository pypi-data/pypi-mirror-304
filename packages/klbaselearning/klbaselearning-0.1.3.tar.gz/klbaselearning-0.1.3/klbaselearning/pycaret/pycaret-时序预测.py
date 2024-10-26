#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 乘客时序数据
from pycaret.datasets import get_data
# 下载路径：https://raw.githubusercontent.com/sktime/sktime/main/sktime/datasets/data/Airline/Airline.csv
data = get_data('./datasets/airline')
# data = get_data('airline')


# In[ ]:


import pandas as pd
data['Date'] = pd.to_datetime(data['Date'])
# 并将Date设置为列号
data.set_index('Date', inplace=True)


# In[ ]:


from pycaret.time_series import TSForecastingExperiment
s = TSForecastingExperiment()
# fh: 用于预测的预测范围。默认值设置为1，即预测前方一点。,fold: 交叉验证中折数
s.setup(data, fh = 3, fold = 5, session_id = 0, verbose = False)
# from pycaret.time_series import *
# s = setup(data, fh = 3, fold = 5, session_id = 0)


# In[ ]:


#模型训练与评估
best = s.compare_models()



# In[ ]:


#数据展示

# jupyter环境下交互可视化展示
# plot参数支持：
# - 'ts' - Time Series Plot
# - 'train_test_split' - Train Test Split
# - 'cv' - Cross Validation
# - 'acf' - Auto Correlation (ACF)
# - 'pacf' - Partial Auto Correlation (PACF)
# - 'decomp' - Classical Decomposition
# - 'decomp_stl' - STL Decomposition
# - 'diagnostics' - Diagnostics Plot
# - 'diff' - Difference Plot
# - 'periodogram' - Frequency Components (Periodogram)
# - 'fft' - Frequency Components (FFT)
# - 'ccf' - Cross Correlation (CCF)
# - 'forecast' - "Out-of-Sample" Forecast Plot
# - 'insample' - "In-Sample" Forecast Plot
# - 'residuals' - Residuals Plot
# s.plot_model(best, plot = 'forecast', data_kwargs = {'fh' : 24})


# In[ ]:


#数据预测
# 使模型拟合包括测试样本在内的完整数据集
final_best = s.finalize_model(best)
s.predict_model(best, fh = 24)
s.save_model(final_best, 'final_best_model')

