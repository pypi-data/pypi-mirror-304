#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from autogluon.tabular import TabularDataset, TabularPredictor


# In[ ]:


train_data = TabularDataset('https://autogluon.s3.amazonaws.com/datasets/Inc/train.csv')
subsample_size = 500  # subsample subset of data for faster demo, try setting this to much larger values
train_data = train_data.sample(n=subsample_size, random_state=0)
train_data.head()


# In[ ]:


label = 'class'
print(f"Unique classes: {list(train_data[label].unique())}")


# In[ ]:


predictor = TabularPredictor(label=label).fit(train_data)


# In[ ]:


test_data = TabularDataset('https://autogluon.s3.amazonaws.com/datasets/Inc/test.csv')
test_data.head()


# In[ ]:


y_pred = predictor.predict(test_data)
y_pred.head()  # Predictions


# In[ ]:


y_pred_proba = predictor.predict_proba(test_data)
y_pred_proba.head()  # Prediction Probabilities


# In[ ]:


predictor.evaluate(test_data)


# In[ ]:


predictor.predict(test_data, model='LightGBM')


# In[ ]:


predictor.model_names()


# In[ ]:


'''
"multiclass": [
    "accuracy",
    "acc",
    "balanced_accuracy",
    "mcc",
    "roc_auc_ovo_macro",
    "log_loss",
    "nll",
    "pac_score",
    "quadratic_kappa",
    "precision_macro",
    "precision_micro",
    "precision_weighted",
    "recall_macro",
    "recall_micro",
    "recall_weighted",
    "f1_macro",
    "f1_micro",
    "f1_weighted"
  ],
'''
'''
"binary": [
    "accuracy",
    "acc",
    "balanced_accuracy",
    "mcc",
    "roc_auc_ovo_macro",
    "log_loss",
    "nll",
    "pac_score",
    "quadratic_kappa",
    "roc_auc",
    "average_precision",
    "precision",
    "precision_macro",
    "precision_micro",
    "precision_weighted",
    "recall",
    "recall_macro",
    "recall_micro",
    "recall_weighted",
    "f1",
    "f1_macro",
    "f1_micro",
    "f1_weighted"
  ],
  '''


'''
best_quality
high_quality
good_quality
medium_quality
'''


# In[ ]:


time_limit = 60  # for quick demonstration only, you should set this to longest time you are willing to wait (in seconds)
metric = 'roc_auc'  # specify your evaluation metric here
predictor = TabularPredictor(label, eval_metric=metric).fit(train_data, time_limit=time_limit, presets='best_quality')


# In[ ]:


age_column = 'age'
train_data[age_column].head()


# In[ ]:


predictor_age = TabularPredictor(label=age_column, path="agModels-predictAge").fit(train_data, time_limit=60)


# In[ ]:


predictor_age.evaluate(test_data)

