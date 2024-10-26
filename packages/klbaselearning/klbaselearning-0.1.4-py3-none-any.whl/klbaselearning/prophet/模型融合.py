#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import pandas as pd 
import numpy as np
from prophet import Prophet
from pandas.plotting import register_matplotlib_converters
import warnings
import datetime
from scipy import stats
#import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
get_ipython().run_line_magic('matplotlib', 'inline')
#from fbprophet.plot import add_changepoints_to_plot
#from fbprophet.diagnostics import cross_validation
#from fbprophet.plot import plot_cross_validation_metric
#from fbprophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation
from prophet.plot import add_changepoints_to_plot
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import performance_metrics
warnings.filterwarnings("ignore")
import os
#os.environ['NUMEXPR_MAX_THREADS'] = '64'

from neuralprophet import NeuralProphet, set_log_level


# In[ ]:


###best 0.7+0.3

new_train_data_best= pd.read_csv('best_1.9.csv')
new_train_data_prophet = pd.read_csv('predict_day17_1_best_3.35973.csv')
new_data_2in1_1  = new_train_data_best*0.7 + new_train_data_prophet*0.3

new_data_2in1_1.to_csv('D20_加权_best_prophet_Trynew_1.csv',index=False) #2.85



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


###best 0.7+0.3
'''
new_train_data_best= pd.read_csv('best_1.9.csv')
new_train_data_prophet = pd.read_csv('predict_day17_1_best_3.35973.csv')
new_data_2in1_1  = new_train_data_best*0.7 + new_train_data_prophet*0.3

new_data_2in1_1.to_csv('D20_加权_best_prophet_Trynew_1.csv',index=False)
'''

