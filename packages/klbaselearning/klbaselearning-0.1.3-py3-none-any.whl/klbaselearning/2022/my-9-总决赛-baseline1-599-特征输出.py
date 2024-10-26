#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import os
import re
import time
from sklearn.metrics import confusion_matrix
from sklearn.metrics.classification import log_loss
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from scipy.sparse import hstack
from scipy.sparse import csr_matrix
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.calibration import CalibratedClassifierCV
from tqdm import tqdm
import joblib
from sklearn.externals import joblib as jobl
from joblib import dump
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, BatchNormalization,Input,PReLU
from keras.utils import np_utils
#from keras.optimizers import adam_v2
from keras.models import Model
#from keras.optimizers import Adagrad
import datetime
from keras.models import load_model
from IPython.display import Image
from keras.callbacks import EarlyStopping,TensorBoard


# In[ ]:


print("# Loading Data")
ageGenderTrain = pd.read_csv('train_age.csv', dtype={'device_id':np.str})
newtrain = pd.read_csv('predictions_lgb_040.csv', dtype={'device_id':np.str})
ageGenderTest = pd.read_csv('test_age.csv', dtype={'device_id':np.str})
phoneBrand = pd.read_csv('phone_device_model.csv', dtype={'device_id':np.str})

eventsData = pd.read_csv('events.csv', parse_dates=['timestamp'], dtype={'device_id':np.str, 'event_id':np.str})
appEventsData = pd.read_csv('app_events.csv', dtype={'app_id':np.str, 'event_id':np.str})
labelCat = pd.read_csv('app_data.csv', dtype={'category':np.str,'app_id':np.str})
print("# Data Loaded")


# In[ ]:


#ageGenderTrain = ageGenderTrain[ageGenderTrain['value']<75]


# In[ ]:


'''
combine=[ageGenderTrain]

for dataset in combine:
    dataset.loc[dataset['value']<=14,'group']='13'
    dataset.loc[(dataset['value'] > 14) & (dataset['value'] <= 16), 'group'] = '16'

sns.countplot('value', hue='value', data=ageGenderTrain)
'''


# In[ ]:


ageGenderTrain.to_csv('train_data_all.csv',index=False)


# In[ ]:


phoneBrand.drop_duplicates(subset='device_id', keep='first',inplace=True)


# In[ ]:


#fact_list=labelCat['category'].value_counts()[0:85]
#labelCat['category']=labelCat['category'].apply(lambda x:'else' if x not in fact_list else x)


# In[ ]:


print("Train Size:", ageGenderTrain.shape)
print("Test Size:", ageGenderTest.shape)
trainrec = ageGenderTrain.shape[0]
testrec = ageGenderTest.shape[0]
ageGenderTrain.head()


# In[ ]:


trainEventData = ageGenderTrain.loc[ageGenderTrain.device_id.isin(eventsData.device_id)]
testEventData = ageGenderTest.loc[ageGenderTest.device_id.isin(eventsData.device_id)]


# In[ ]:


uBrands = phoneBrand.phone_brand.nunique()
uModels = phoneBrand.device_model.nunique()
uEvents = eventsData.event_id.nunique()
uCats = labelCat.category.nunique()
print(uBrands, uModels, uEvents, uCats)


# In[ ]:


# REF - https://www.kaggle.com/shahnawazakhtar/using-features-from-label-categories-csv
def vectorize(train, test, columns, fillMissing):
    data = pd.concat((train, test), axis=0, ignore_index=True)
    data = data[columns].astype(np.str).apply(lambda x: " ".join(s for s in x), axis=1).fillna(fillMissing)
    print(data.shape)
    split_len = len(train)
    # TF-IDF Feature
    print("TfidfVectorizer for", columns)
    vectorizer = TfidfVectorizer(min_df=1)
    data = vectorizer.fit_transform(data)

    train = data[:split_len, :]
    test = data[split_len:, :]
    return train, test


# In[ ]:


def vectorizeOHE(train, test, columns, fillMissing):
    data = pd.concat((train, test), axis=0, ignore_index=True)
    data = data[columns].astype(np.str).apply(lambda x: " ".join(s for s in x), axis=1).fillna(fillMissing)
    print(data.shape)
    split_len = len(train)
    # OHE Feature
    print("One Hot Encoding for", columns)
    vectorizer = CountVectorizer(min_df=1)
    data = vectorizer.fit_transform(data)
    train = data[:split_len, :]
    test = data[split_len:, :]
    return train, test


# In[ ]:


print("--Handling Labels Categories")
#---------------------------------------------------------------------------
labelCat = labelCat.fillna('unknown')
labelCat.drop_duplicates(keep='first', inplace=True)
#---------------------------------------------------------------------------
labelCat["category"] = labelCat["category"].apply(lambda x: " ".join(str(x).replace("-"," ").replace("/"," ").replace("("," ").replace(")"," ").split()))
labelCat.category = labelCat.category.apply(lambda x: "Cat:"+str(x))
categories = labelCat.groupby('app_id')['category'].apply(lambda x: " ".join(s for s in x))
labelCat = labelCat.drop('category', axis=1)


# In[ ]:


eventsData['timestamp2'] = pd.to_datetime(eventsData['timestamp'])


# In[ ]:


eventsData['hour'] = eventsData['timestamp2'].dt.hour


# In[ ]:


time_large = eventsData.groupby('device_id')['hour'].apply(lambda x: max(x))


# In[ ]:


eventsData = eventsData.drop(['timestamp2'], axis=1)


# In[ ]:


time_small = eventsData.groupby('device_id')['hour'].apply(lambda x: min(x))


# In[ ]:


from collections import Counter
time_most = eventsData.groupby('device_id')['hour'].apply(lambda x: Counter(x).most_common(1)[0][0])


# In[ ]:


trainEventData["time_large"] = trainEventData["device_id"].map(time_large)
testEventData["time_large"] = testEventData["device_id"].map(time_large)


# In[ ]:


trainEventData["time_small"] = trainEventData["device_id"].map(time_small)
testEventData["time_small"] = testEventData["device_id"].map(time_small)


# In[ ]:


trainEventData["time_most"] = trainEventData["device_id"].map(time_most)
testEventData["time_most"] = testEventData["device_id"].map(time_most)


# In[ ]:


trainEventData.head()


# In[ ]:


#---------------------------------------------------------------------------
print("----APP-EVENTS")
appEventsData["category"] = appEventsData["app_id"].map(categories)
categories = appEventsData.groupby("event_id")["category"].apply(lambda x: " ".join(str(s) for s in x))

appEventsData = appEventsData.drop('category', axis=1)
#---------------------------------------------------------------------------


# In[ ]:


#---------------------------------------------------------------------------
print("----EVENTS")
eventsData["category"] = eventsData["event_id"].map(categories)
categories = eventsData.groupby("device_id")["category"].apply(lambda x: " ".join(str(s) for s in x))

eventsData = eventsData.drop('category', axis=1)
#---------------------------------------------------------------------------


# In[ ]:


#---------------------------------------------------------------------------
print("----TRAIN-TEST Merge")
#ageGenderTrain["category"] = ageGenderTrain["device_id"].map(categories)
#ageGenderTest["category"] = ageGenderTest["device_id"].map(categories)
trainEventData["category"] = trainEventData["device_id"].map(categories)
testEventData["category"] = testEventData["device_id"].map(categories)

#---------------------------------------------------------------------------
del categories
#---------------------------------------------------------------------------
trainEventData.head()


# In[ ]:


trainEventData['catCnt'] = trainEventData.category.apply(lambda x: list(set(str(x).split('Cat:'))))
#trainEventData.category = trainEventData.catCnt.astype(str)
trainEventData.catCnt = trainEventData.catCnt.str.len()
trainEventData.catCnt = trainEventData.catCnt.fillna(0)

testEventData['catCnt'] = testEventData.category.apply(lambda x: list(set(str(x).split('Cat:'))))
#testEventData.category = testEventData.catCnt.astype(str)
testEventData.catCnt = testEventData.catCnt.str.len()
testEventData.catCnt = testEventData.catCnt.fillna(0)

trainEventData.head()


# In[ ]:


vectorizer=StandardScaler()
vectorizer.fit(trainEventData['catCnt'].values.reshape(-1,1))

Xtr_lCatCnt = vectorizer.transform(trainEventData['catCnt'].values.reshape(-1,1))
Xte_lCatCnt = vectorizer.transform(testEventData['catCnt'].values.reshape(-1,1))

print("Train Category-Count Shape: ",Xtr_lCatCnt.shape)
print("Test Category-Count Shape: ",Xte_lCatCnt.shape)


# In[ ]:


vectorizer=StandardScaler()
vectorizer.fit(trainEventData['time_large'].values.reshape(-1,1))

Xtr_time_large = vectorizer.transform(trainEventData['time_large'].values.reshape(-1,1))
Xte_ltime_large = vectorizer.transform(testEventData['time_large'].values.reshape(-1,1))

print("Train Category-Count Shape: ",Xtr_time_large.shape)
print("Test Category-Count Shape: ",Xte_ltime_large.shape)


# In[ ]:


vectorizer=StandardScaler()
vectorizer.fit(trainEventData['time_most'].values.reshape(-1,1))

Xtr_time_most = vectorizer.transform(trainEventData['time_most'].values.reshape(-1,1))
Xte_time_most = vectorizer.transform(testEventData['time_most'].values.reshape(-1,1))

print("Train Category-Count Shape: ",Xtr_time_most.shape)
print("Test Category-Count Shape: ",Xte_time_most.shape)


# In[ ]:


vectorizer=StandardScaler()
vectorizer.fit(trainEventData['time_small'].values.reshape(-1,1))

Xtr_time_small = vectorizer.transform(trainEventData['time_small'].values.reshape(-1,1))
Xte_time_small = vectorizer.transform(testEventData['time_small'].values.reshape(-1,1))

print("Train Category-Count Shape: ",Xtr_time_small.shape)
print("Test Category-Count Shape: ",Xte_time_small.shape)


# In[ ]:


Xtr_catCntProp = ((trainEventData.catCnt)/uCats).values.reshape(-1,1)
Xte_catCntProp = ((testEventData.catCnt)/uCats).values.reshape(-1,1)

print("Train Category-Count Proportion Shape: ",Xtr_catCntProp.shape)
print("Test Category-Count Proportion Shape: ",Xte_catCntProp.shape)


# In[ ]:


Xtr_lCatEv, Xte_lCatEv = vectorize(trainEventData, testEventData, ["category"], "missing")
print(Xtr_lCatEv.shape)
print(Xte_lCatEv.shape)


# In[ ]:


trainEventData = trainEventData.drop(['category','catCnt'], axis=1)
testEventData = testEventData.drop(['category','catCnt'], axis=1)


# In[ ]:


print("--Handling APP IDs")
#---------------------------------------------------------------------------
labelap = LabelEncoder().fit(labelCat.app_id)
labelCat.app_id = labelap.transform(labelCat.app_id)
appCount = len(labelap.classes_)
print('Total unique apps: ', appCount)

appEventsData.app_id = labelap.transform(appEventsData.app_id)
#---------------------------------------------------------------------------
print("----APP-EVENTS")
appEventsData["appID"] = appEventsData.app_id.astype(str).apply(lambda x: "APPID:"+str(x))
appIDs = appEventsData.groupby("event_id")["appID"].apply(lambda x: " ".join(str(s) for s in x))

appEventsData = appEventsData.drop('appID', axis=1)
#---------------------------------------------------------------------------
print("----EVENTS")
eventsData["appID"] = eventsData["event_id"].map(appIDs)
appIDs = eventsData.groupby("device_id")["appID"].apply(lambda x: " ".join(str(s) for s in x))

eventsData = eventsData.drop('appID', axis=1)
#---------------------------------------------------------------------------
print("----TRAIN-TEST Merge")
#ageGenderTrain["appID"] = ageGenderTrain["device_id"].map(appIDs)
#ageGenderTest["appID"] = ageGenderTest["device_id"].map(appIDs)
trainEventData["appID"] = trainEventData["device_id"].map(appIDs)
testEventData["appID"] = testEventData["device_id"].map(appIDs)

#---------------------------------------------------------------------------
del appIDs
#---------------------------------------------------------------------------
trainEventData.head()


# In[ ]:


trainEventData['appIDCnt'] = trainEventData.appID.str.replace('APPID:','')
trainEventData.appIDCnt = trainEventData.appIDCnt.str.replace(' ',', ')
testEventData['appIDCnt'] = testEventData.appID.str.replace('APPID:','')
testEventData.appIDCnt = testEventData.appIDCnt.str.replace(' ',', ')
trainEventData.head()


# In[ ]:


testEventData.head()


# In[ ]:


trainEventData.appIDCnt = trainEventData.appIDCnt.apply(lambda x: list(set(str(x).split(', '))))
#trainEventData.appID = trainEventData.appIDCnt.astype(str)
trainEventData.appIDCnt = trainEventData.appIDCnt.str.len()

testEventData.appIDCnt = testEventData.appIDCnt.apply(lambda x: list(set(str(x).split(', '))))
#testEventData.appID = testEventData.appIDCnt.astype(str)
testEventData.appIDCnt = testEventData.appIDCnt.str.len()

trainEventData.head()


# In[ ]:


Xtr_appIDEv, Xte_appIDEv = vectorize(trainEventData, testEventData, ["appID"], "missing")
print(Xtr_appIDEv.shape)
print(Xte_appIDEv.shape)


# In[ ]:


vectorizer=StandardScaler()
vectorizer.fit(trainEventData['appIDCnt'].values.reshape(-1,1))

Xtr_appIDCnt = vectorizer.transform(trainEventData['appIDCnt'].values.reshape(-1,1))
Xte_appIDCnt = vectorizer.transform(testEventData['appIDCnt'].values.reshape(-1,1))

print("Train APPID-Count Shape: ",Xtr_appIDCnt.shape)
print("Test APPID-Count Shape: ",Xte_appIDCnt.shape)


# In[ ]:


Xtr_appIDCntProp = ((trainEventData.appIDCnt)/uCats).values.reshape(-1,1)
Xte_appIDCntProp = ((testEventData.appIDCnt)/uCats).values.reshape(-1,1)
print("Train APP ID Proportion Shape: ",Xtr_appIDCntProp.shape)
print("Test APP ID Proportion Shape: ",Xte_appIDCntProp.shape)


# In[ ]:


from scipy.stats import entropy


# In[ ]:


# REF - https://www.kaggle.com/c/talkingdata-mobile-user-demographics/discussion/23424
trainEventData.appID = trainEventData.appID.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))
testEventData.appID = testEventData.appID.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))

print(trainEventData.shape)
print(testEventData.shape)
trainEventData.head()


# In[ ]:


print("--Handling IS_ACTIVE")
#---------------------------------------------------------------------------
print("----APP-EVENTS")
appEventsData["activeApp"] = appEventsData.is_active.astype(str).apply(lambda x: " ".join(str(s) for s in x))
activeApps = appEventsData.groupby("event_id")["is_active"].apply(lambda x: " ".join(str(s) for s in x))

appEventsData = appEventsData.drop('activeApp', axis=1)
#---------------------------------------------------------------------------
print("----EVENTS")
eventsData["activeApp"] = eventsData["event_id"].map(activeApps)
activeApps = eventsData.groupby("device_id")["activeApp"].apply(lambda x: " ".join(str(s) for s in x))

eventsData = eventsData.drop('activeApp', axis=1)
#---------------------------------------------------------------------------
print("----TRAIN-TEST Merge")
#ageGenderTrain["activeApp"] = ageGenderTrain["device_id"].map(activeApps)
#ageGenderTest["activeApp"] = ageGenderTest["device_id"].map(activeApps)

trainEventData["activeApp"] = trainEventData["device_id"].map(activeApps)
testEventData["activeApp"] = testEventData["device_id"].map(activeApps)

del activeApps
#---------------------------------------------------------------------------
trainEventData.head()


# In[ ]:


Xtr_activeAppEv, Xte_activeAppEv = vectorize(trainEventData, testEventData, ["activeApp"], "missing")
print(Xtr_activeAppEv.shape)
print(Xte_activeAppEv.shape)


# In[ ]:


trainEventData['actvAppCnt'] = trainEventData.activeApp.str.count('1')
testEventData['actvAppCnt'] = testEventData.activeApp.str.count('1')

vectorizer=StandardScaler()
vectorizer.fit(trainEventData['actvAppCnt'].values.reshape(-1,1))

Xtr_actvAppCnt = vectorizer.transform(trainEventData['actvAppCnt'].values.reshape(-1,1))
Xte_actvAppCnt = vectorizer.transform(testEventData['actvAppCnt'].values.reshape(-1,1))

print("Train Active APP Count Shape: ",Xtr_actvAppCnt.shape)
print("Test Active APP Count Shape: ",Xte_actvAppCnt.shape)


# In[ ]:


trainEventData['avg_actvAppCnt'] = trainEventData['actvAppCnt']/7
testEventData['avg_actvAppCnt'] = testEventData['actvAppCnt']/7
vectorizer=StandardScaler()
vectorizer.fit(trainEventData['avg_actvAppCnt'].values.reshape(-1,1))

Xtr_avg_actvAppCnt = vectorizer.transform(trainEventData['avg_actvAppCnt'].values.reshape(-1,1))
Xte_avg_actvAppCnt = vectorizer.transform(testEventData['avg_actvAppCnt'].values.reshape(-1,1))


# In[ ]:


trainEventData.activeApp = trainEventData.activeApp.str.replace(' ',', ')
testEventData.activeApp = testEventData.activeApp.str.replace(' ',', ')

# REF - https://www.kaggle.com/c/talkingdata-mobile-user-demographics/discussion/23424
trainEventData.activeApp = trainEventData.activeApp.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))
testEventData.activeApp = testEventData.activeApp.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))

print(trainEventData.shape)
print(testEventData.shape)
trainEventData.head()


# In[ ]:


Xtr_activeAppEntropy = trainEventData['activeApp'].values.reshape(-1,1)
Xte_activeAppEntropy = testEventData['activeApp'].values.reshape(-1,1)

print("Train Active APP Entropy Shape: ",Xtr_activeAppEntropy.shape)
print("Test Active APP Entropy Shape: ",Xte_activeAppEntropy.shape)


# In[ ]:


trainEventData = trainEventData.drop(['activeApp', 'actvAppCnt','avg_actvAppCnt'], axis=1)
testEventData = testEventData.drop(['activeApp', 'actvAppCnt','avg_actvAppCnt'], axis=1)


# In[ ]:


print('Handling Phone-Brand and Device-Model')
phoneBrand = phoneBrand.drop_duplicates('device_id', keep='first')
phoneBrand.device_model = phoneBrand.phone_brand.str.cat(" "+phoneBrand.device_model)
phoneBrand.phone_brand = phoneBrand.phone_brand.map(str.strip).map(str.lower)
phoneBrand.device_model = phoneBrand.device_model.map(str.strip).map(str.lower)
uModels = phoneBrand.device_model.nunique()

ageGenderTrain = ageGenderTrain.merge(phoneBrand, on='device_id', how='left')
ageGenderTest = ageGenderTest.merge(phoneBrand, on='device_id', how='left')
#---------------------------------------------
print("Train:", ageGenderTrain.shape)
print("Test:", ageGenderTest.shape)
ageGenderTrain.head()


# In[ ]:


#notrainEventData = ageGenderTrain.loc[~ageGenderTrain.device_id.isin(eventsData.device_id)]
#notestEventData = ageGenderTest.loc[~ageGenderTest.device_id.isin(eventsData.device_id)]
notrainEventData = ageGenderTrain
notestEventData = ageGenderTest
trainEventData = ageGenderTrain.loc[ageGenderTrain.device_id.isin(eventsData.device_id)]
testEventData = ageGenderTest.loc[ageGenderTest.device_id.isin(eventsData.device_id)]


# In[ ]:


print(notestEventData)


# In[ ]:


phbrData = pd.concat([ageGenderTrain, ageGenderTest], axis=0, ignore_index=True)
print("TfidfVectorizer for Phone Brand")
vectorizer = TfidfVectorizer(min_df=1).fit(phbrData.phone_brand)
Xtr_phbrev = vectorizer.transform(trainEventData.phone_brand)
Xte_phbrev = vectorizer.transform(testEventData.phone_brand)
print("=====================================")
print("After TfidfVectorizer for PHONE BRAND")
print(Xtr_phbrev.shape)
print(Xte_phbrev.shape)
print("=====================================")

Xtr_phbrnoev = vectorizer.transform(notrainEventData.phone_brand)
Xte_phbrnoev = vectorizer.transform(notestEventData.phone_brand)

print("=====================================")
print("After TfidfVectorizer for PHONE BRAND")
print(Xtr_phbrnoev.shape)
print(Xte_phbrnoev.shape)
print("=====================================")


# In[ ]:


demoData = pd.concat([ageGenderTrain, ageGenderTest], axis=0, ignore_index=True)
print("TfidfVectorizer for Device Model")
vectorizer = TfidfVectorizer(min_df=1).fit(demoData.device_model)
Xtr_demoev = vectorizer.transform(trainEventData.device_model)
Xte_demoev = vectorizer.transform(testEventData.device_model)

print("=====================================")
print("After TfidfVectorizer for DEVICE MODEL")
print(Xtr_demoev.shape)
print(Xte_demoev.shape)
print("=====================================")

Xtr_demonoev = vectorizer.transform(notrainEventData.device_model)
Xte_demonoev = vectorizer.transform(notestEventData.device_model)

print("=====================================")
print("After TfidfVectorizer for DEVICE MODEL")
print(Xtr_demonoev.shape)
print(Xte_demonoev.shape)
print("=====================================")


# In[ ]:


ageGenderTrain = ageGenderTrain.drop(['phone_brand','device_model'], axis=1)
ageGenderTest = ageGenderTest.drop(['phone_brand','device_model'], axis=1)

trainEventData = trainEventData.drop(['phone_brand','device_model'], axis=1)
testEventData = testEventData.drop(['phone_brand','device_model'], axis=1)

notrainEventData = notrainEventData.drop(['phone_brand','device_model'], axis=1)
notestEventData = notestEventData.drop(['phone_brand','device_model'], axis=1)

print(ageGenderTrain.shape)
print(ageGenderTest.shape)

ageGenderTrain.head()


# In[ ]:


ageGenderTrain['trainrow'] = np.arange(ageGenderTrain.shape[0])
ageGenderTest['testrow'] = np.arange(ageGenderTest.shape[0])
#---------------------------------------------
print(ageGenderTrain.shape)
print(ageGenderTest.shape)
ageGenderTrain.head()


# In[ ]:


#---------------------------------------------------------------------------
trEventData = ageGenderTrain.loc[ageGenderTrain.device_id.isin(eventsData.device_id)]
teEventData = ageGenderTest.loc[ageGenderTest.device_id.isin(eventsData.device_id)]

evtrainrec = trEventData.shape[0]
evtestrec = teEventData.shape[0]
trEventData['trainrow'] = np.arange(trEventData.shape[0])
teEventData['testrow'] = np.arange(teEventData.shape[0])


# In[ ]:


def findDayPart(x):
    if (x>21 and x <=23) or (x>=0 and x<=6):
        return 0 #NIGHT
    if x>6 and x<9:
        return 1 #MORNING
    if x>=9 and x<=18:
        return 2 #PEAKHOURS
    if x>18 and x<22:
        return 3 #EVENING
#---------------------------------------------------------------------------
eventsData['dayOfWeek'] = eventsData.timestamp.dt.dayofweek
eventsData['activityhour'] = eventsData.timestamp.dt.hour
eventsData['dayPart'] = eventsData['activityhour'].apply(findDayPart)
eventsData = eventsData.drop(['timestamp'], axis=1)
print(eventsData.shape)
eventsData.head()


# In[ ]:


trEventData = trEventData.merge(eventsData[['device_id','dayOfWeek']], on='device_id', how='left')
teEventData = teEventData.merge(eventsData[['device_id','dayOfWeek']], on='device_id', how='left')
#---------------------------------------------------------------------------

Xtr_dayOfWeekEv = csr_matrix((np.ones(trEventData.shape[0]), (trEventData.trainrow, trEventData.dayOfWeek)), shape=(evtrainrec,7))
Xte_dayOfWeekEv = csr_matrix((np.ones(teEventData.shape[0]), (teEventData.testrow, teEventData.dayOfWeek)), shape=(evtestrec,7))
#---------------------------------------------------------------------------
print(Xtr_dayOfWeekEv.shape)
print(Xte_dayOfWeekEv.shape)


# In[ ]:


# REF - https://www.kaggle.com/c/talkingdata-mobile-user-demographics/discussion/23424
dowEntropy = eventsData[['device_id', 'dayOfWeek']].groupby('device_id')['dayOfWeek'].apply(lambda x: ", ".join(str(s) for s in x))

trEventData['dowEntropy'] = trEventData.device_id.map(dowEntropy)
trEventData.dowEntropy = trEventData.dowEntropy.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))
teEventData['dowEntropy'] = teEventData.device_id.map(dowEntropy)
teEventData.dowEntropy = teEventData.dowEntropy.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))

trEventData = trEventData.drop_duplicates('device_id')
teEventData = teEventData.drop_duplicates('device_id')

print(trEventData.shape)
print(teEventData.shape)
trEventData.head()


# In[ ]:


Xtr_dowEntropy = trEventData['dowEntropy'].values.reshape(-1,1)
Xte_dowEntropy = teEventData['dowEntropy'].values.reshape(-1,1)

print("Train EVENT-Count Shape: ",Xtr_dowEntropy.shape)
print("Test EVENT-Count Shape: ",Xte_dowEntropy.shape)

trEventData = trEventData.drop(['dowEntropy'], axis=1)
teEventData = teEventData.drop(['dowEntropy'], axis=1)


# In[ ]:


trEventData = trEventData.drop(['dayOfWeek'], axis=1)
teEventData = teEventData.drop(['dayOfWeek'], axis=1)

trEventData = trEventData.drop_duplicates('device_id')
teEventData = teEventData.drop_duplicates('device_id')

trEventData = trEventData.merge(eventsData[['device_id','activityhour']], on='device_id', how='left')
teEventData = teEventData.merge(eventsData[['device_id','activityhour']], on='device_id', how='left')

Xtr_activityhourEv = csr_matrix((np.ones(trEventData.shape[0]), (trEventData.trainrow, trEventData.activityhour)), shape=(evtrainrec,24))
Xte_activityhourEv = csr_matrix((np.ones(teEventData.shape[0]), (teEventData.testrow, teEventData.activityhour)), shape=(evtestrec,24))
#---------------------------------------------------------------------------
print(Xtr_activityhourEv.shape)
print(Xte_activityhourEv.shape)


# In[ ]:


hourEntropy = eventsData[['device_id', 'activityhour']].groupby('device_id')['activityhour'].apply(lambda x: ", ".join(str(s) for s in x))

trEventData['hourEntropy'] = trEventData.device_id.map(hourEntropy)
trEventData.hourEntropy = trEventData.hourEntropy.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))
teEventData['hourEntropy'] = teEventData.device_id.map(hourEntropy)
teEventData.hourEntropy = teEventData.hourEntropy.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))

trEventData = trEventData.drop_duplicates('device_id')
teEventData = teEventData.drop_duplicates('device_id')

print(trEventData.shape)
print(teEventData.shape)
trEventData.head()


# In[ ]:


Xtr_hourEntropy = trEventData['hourEntropy'].values.reshape(-1,1)
Xte_hourEntropy = teEventData['hourEntropy'].values.reshape(-1,1)

print("Train EVENT-Count Shape: ",Xtr_hourEntropy.shape)
print("Test EVENT-Count Shape: ",Xte_hourEntropy.shape)

trEventData = trEventData.drop(['hourEntropy'], axis=1)
teEventData = teEventData.drop(['hourEntropy'], axis=1)


# In[ ]:


trEventData = trEventData.drop(['activityhour'], axis=1)
teEventData = teEventData.drop(['activityhour'], axis=1)
trEventData = trEventData.drop_duplicates('device_id')
teEventData = teEventData.drop_duplicates('device_id')


trEventData = trEventData.merge(eventsData[['device_id','dayPart']], on='device_id', how='left')
teEventData = teEventData.merge(eventsData[['device_id','dayPart']], on='device_id', how='left')

Xtr_dayPartEv = csr_matrix((np.ones(trEventData.shape[0]), (trEventData.trainrow, trEventData.dayPart)), shape=(evtrainrec,4))
Xte_dayPartEv = csr_matrix((np.ones(teEventData.shape[0]), (teEventData.testrow, teEventData.dayPart)), shape=(evtestrec,4))
#---------------------------------------------------------------------------
print(Xtr_dayPartEv.shape)
print(Xte_dayPartEv.shape)


# In[ ]:


# REF - https://www.kaggle.com/c/talkingdata-mobile-user-demographics/discussion/23424
dayPartEntropy = eventsData[['device_id', 'dayPart']].groupby('device_id')['dayPart'].apply(lambda x: ", ".join(str(s) for s in x))

trEventData['dayPartEntropy'] = trEventData.device_id.map(dayPartEntropy)
trEventData.dayPartEntropy = trEventData.dayPartEntropy.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))
teEventData['dayPartEntropy'] = teEventData.device_id.map(dayPartEntropy)
teEventData.dayPartEntropy = teEventData.dayPartEntropy.apply(lambda x: entropy(list(Counter(str(x).split(', ')).values()), base=2))

trEventData = trEventData.drop_duplicates('device_id')
teEventData = teEventData.drop_duplicates('device_id')

print(trEventData.shape)
print(teEventData.shape)
trEventData.head()


# In[ ]:


Xtr_dayPartEntropy = trEventData['dayPartEntropy'].values.reshape(-1,1)
Xte_dayPartEntropy = teEventData['dayPartEntropy'].values.reshape(-1,1)

print("Train EVENT-Count Shape: ",Xtr_dayPartEntropy.shape)
print("Test EVENT-Count Shape: ",Xte_dayPartEntropy.shape)

trEventData = trEventData.drop(['dayPartEntropy'], axis=1)
teEventData = teEventData.drop(['dayPartEntropy'], axis=1)


# In[ ]:


trEventData = trEventData.drop(['dayPart'], axis=1)
teEventData = teEventData.drop(['dayPart'], axis=1)

trEventData = trEventData.drop_duplicates('device_id')
teEventData = teEventData.drop_duplicates('device_id')


# In[ ]:


# REF - https://www.kaggle.com/zfturbo/xgboost-simple-starter
eventsData['evCount'] = eventsData.groupby(['device_id'])['event_id'].transform('count')
deviceEvents = eventsData[['device_id', 'evCount']].drop_duplicates('device_id', keep='first')
eventsData = eventsData.drop(['evCount'], axis=1)

trEventData = trEventData.merge(deviceEvents, on='device_id', how='left')
trEventData.evCount = trEventData.evCount.fillna(0)
teEventData = teEventData.merge(deviceEvents, on='device_id', how='left')
teEventData.evCount = teEventData.evCount.fillna(0)

print(trEventData.shape)
print(teEventData.shape)
trEventData.head()


# In[ ]:


vectorizer=StandardScaler()
vectorizer.fit(trEventData['evCount'].values.reshape(-1,1))

Xtr_evCount = vectorizer.transform(trEventData['evCount'].values.reshape(-1,1))
Xte_evCount = vectorizer.transform(teEventData['evCount'].values.reshape(-1,1))

print("Train EVENT-Count Shape: ",Xtr_evCount.shape)
print("Test EVENT-Count Shape: ",Xte_evCount.shape)


# In[ ]:


y = ageGenderTrain['value']
#ohe = LabelEncoder().fit(y.astype(str))
#y = ohe.transform(y.astype(str))
print(y)


# In[ ]:


ynoev = notrainEventData['value']
#ynoev = ohe.transform(ynoev.astype(str))
print(ynoev)


# In[ ]:


yev = trainEventData['value']
#yev = ohe.transform(yev.astype(str))
#print(yev)


# In[ ]:


from scipy.sparse import hstack
Xnoev_tr = hstack((Xtr_phbrnoev, Xtr_demonoev)).tocsr()
Xnoev_te = hstack((Xte_phbrnoev, Xte_demonoev)).tocsr()

print("====================================")
print("After Merging all the Sparse Matrices")
print(Xnoev_tr.shape)
print(Xnoev_te.shape)
print("====================================")


# In[ ]:


from scipy.sparse import hstack
Xev_tr = hstack((Xtr_time_large,Xtr_time_most,Xtr_time_most,Xtr_lCatEv, Xtr_lCatCnt, Xtr_catCntProp, Xtr_appIDEv, Xtr_appIDCnt, Xtr_appIDCntProp, Xtr_appIDEntropy, Xtr_activeAppEv, Xtr_actvAppCnt, Xtr_activeAppEntropy, Xtr_phbrev, Xtr_demoev, Xtr_dayOfWeekEv, Xtr_dowEntropy, Xtr_activityhourEv, Xtr_hourEntropy, Xtr_dayPartEv, Xtr_dayPartEntropy, Xtr_evCount)).tocsr()
Xev_te = hstack((Xte_ltime_large,Xte_time_most,Xte_time_most,Xte_lCatEv, Xte_lCatCnt, Xte_catCntProp, Xte_appIDEv, Xte_appIDCnt, Xte_appIDCntProp, Xte_appIDEntropy, Xte_activeAppEv, Xte_actvAppCnt, Xte_activeAppEntropy, Xte_phbrev, Xte_demoev, Xte_dayOfWeekEv, Xte_dowEntropy, Xte_activityhourEv, Xte_hourEntropy, Xte_dayPartEv, Xte_dayPartEntropy, Xte_evCount)).tocsr()

print("====================================")
print("After Merging all the Sparse Matrices")
print(Xev_tr.shape)
print(Xev_te.shape)
print("====================================")


# In[ ]:


print(Xtr_lCatEv) #0.017581295408285763


# In[ ]:


def save_sparse_matrix(filename, xmtr):
    np.savez(filename,data = xmtr.data ,indices= xmtr.indices,
             indptr =xmtr.indptr, shape=xmtr.shape )
    
#Loads a sparse matrix
def load_sparse_matrix(filename):
    tmp = np.load(filename)
    return csr_matrix((tmp['data'], tmp['indices'], tmp['indptr']), shape= tmp['shape'])


# In[ ]:


save_sparse_matrix('sparse/Xev_tr.npz',Xev_tr.tocsr())
save_sparse_matrix('sparse/Xev_te.npz',Xev_te.tocsr())

