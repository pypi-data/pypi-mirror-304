#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from autogluon.tabular import TabularDataset,TabularPredictor
import os
import pandas as pd
import numpy as np
#os.environ["NUMEXPR_MAX_THREADS"] = '20'
from imblearn.over_sampling import SMOTE
from keras import backend as K


# In[ ]:


from autogluon.tabular.configs.hyperparameter_configs import get_hyperparameter_config
hyperparameters = get_hyperparameter_config('multimodal')
hyperparameters


# In[ ]:


'''
margin = 0.8
theta = lambda t: (K.sign(t)+1.)/2.
def bin_loss(y_true, y_pred):
    return - (1 - theta(y_true - margin) * theta(y_pred - margin)
                - theta(1 - margin - y_true) * theta(1 - margin - y_pred)
             ) * (y_true * K.log(y_pred + 1e-8) + (1 - y_true) * K.log(1 - y_pred + 1e-8))
'''


# In[ ]:


'''
hyperparameters = {
    'GBM': [
        {'ag_args_fit': {'num_cpus': 20,'learning_rate': 0.01,}},  # Train with CPU #'num_cpus': 20,
         # Train with GPU
    ],
    'CAT': [
        {'ag_args_fit': {'num_cpus': 20,'learning_rate': 0.01}},  # Train with CPU#'num_cpus': 20},
         # Train with GPU
    ],
   
   'XGB': [
        {'ag_args_fit': {'num_cpus': 20,'learning_rate': 0.01}},  # Train with CPU #'num_cpus': 20,
         # Train with GPU
    ]
}
'''


# In[ ]:


'''
import torch
import numpy as np
def multilabel_categorical_crossentropy(y_true, y_pred):
    """多标签分类的交叉熵
    说明：y_true和y_pred的shape一致，y_true的元素非0即1，
         1表示对应的类为目标类，0表示对应的类为非目标类。
    警告：请保证y_pred的值域是全体实数，换言之一般情况下y_pred
         不用加激活函数，尤其是不能加sigmoid或者softmax！预测
         阶段则输出y_pred大于0的类。如有疑问，请仔细阅读并理解
         本文。
    假如类别总数为10
    label ：[0,1,0,0,0,0,0,0,0,1]  代表条数据被标注为 2,10 属于 2类也属于10类
    输出也为10类别 输出维度也为10。
    类别从1位置开始0位置代表阈值s就是输出的维度第一个位置是阈值预测
    目标类的分数都大于s，非目标类的分数都小于s
    这里阈值s默认为0故而可忽略只要类从1开始就可
    """
    y_true=torch.Tensor(np.array(y_true))
    y_pred=torch.Tensor(np.array(y_pred))
    y_pred = (1 - 2 * y_true) * y_pred
    y_pred_neg = y_pred - y_true * 1e12
    y_pred_pos = y_pred - (1 - y_true) * 1e12


    zeros = torch.zeros_like(y_pred[..., :1])

    y_pred_neg = torch.cat((y_pred_neg, zeros), dim=-1)
    y_pred_pos = torch.cat((y_pred_pos, zeros), dim=-1)


    neg_loss = torch.logsumexp(y_pred_neg, dim=-1)
    pos_loss = torch.logsumexp(y_pred_pos, dim=-1)
    new_loss = (neg_loss + pos_loss).numpy()
    return new_loss


'''


# In[ ]:





# In[ ]:


'''
if __name__ == '__main__':
    a=torch.Tensor(np.array([1,0,0,0,0,0,1]))
    b=torch.Tensor(np.array([1,2,3,4,5,6,5]))
    print(multilabel_categorical_crossentropy(a,b))
'''


# In[ ]:


'''
a=[0,0]
b=[0,0]
'''


# In[ ]:


'''
from autogluon.core.metrics import make_scorer
multilabel_categorical_crossentropy_scorer = make_scorer(name='bin_categorical_crossentropy',
                                                  score_func=bin_loss,
                                                  optimum=0,
                                                  greater_is_better=False)
'''


# In[ ]:


multilabel_categorical_crossentropy_scorer(a,b)


# In[ ]:





# In[ ]:





# ### 1、导入数据

# In[ ]:


# 导入数据  
print("Loading Data ... ")  
df = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')#在特征工程代码中生成的中间文件
best_sub = pd.read_csv('result_711_boost_99985.csv')#注:best_sub_9704.csv为上一次最好提交结果，该CSV也为此模型在原始训练文件中跑出，但模型参数可能略有不同，分数0.9704（7月4日），在这个CSV基础上提取训练样本加入原训练集中，让模型学习更多的隐藏因子。


# ### 2、数据预处理

# In[ ]:


test_data3 = test_data.copy()
test_data2 = test_data.copy()
#test_data2 = df.copy()
test_data2['label'] = best_sub['label']


# In[ ]:


y2=df['label']


# In[ ]:


df2= df.drop('label', axis=1)


# In[ ]:


'''
#欠采样
from imblearn.under_sampling import ClusterCentroids
cc = ClusterCentroids(random_state=0)
X_resampled, y_resampled = cc.fit_resample(df,y2)
'''


# In[ ]:


#X_resampled['label'] = y_resampled


# In[ ]:


#X_resampled.to_csv('X_resampled.csv',index=False)


# In[ ]:


'''
# 使用 SMOTE 对数据进行上采样以解决类别不平衡问题
smote = SMOTE(random_state=2021, n_jobs=-1)
k_x_train, k_y_train = smote.fit_resample(x_train, y_train)  
print(f"after smote, k_x_train.shape: {k_x_train.shape}, k_y_train.shape: {k_y_train.shape}")

# 将训练集转换为适应 CNN 输入的 shape
#k_x_train = np.array(k_x_train).reshape(k_x_train.shape[0], k_x_train.shape[1], 1)


k_x_train = k_x_train

k_y_train = k_y_train
'''


# In[ ]:





# In[ ]:


#newdf = x_train.copy()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#best_sub[best_sub['label']>0.51].count()  #注"0.992"该数值由于上一次迭代的时候没做记录，但误差应该在0.0001-0.001之间


# In[ ]:


#newdf=np.concatenate((df,test_data2),axis=0)


# In[ ]:


newdf = df.copy()


# In[ ]:


#new_test2 = test_data2[test_data2['label'] > 0.51] #具体数值由于上一次迭代的时候没做记录了，但误差应该在0.0001-0.003之间


# In[ ]:


#new_test2['label'][new_test2['label'] > 0.51] =1


# In[ ]:


#newdf = pd.concat([df.assign(is_train = 1),new_test2.assign(is_train = 0)],ignore_index=True) #合并train和test，并且用is_train进行标记


# In[ ]:


newdf.head


# In[ ]:


#test_data2['是否流失'] = best_sub['是否流失']


# In[ ]:


newdf = newdf.drop(['uid','col_1','col_3'], axis=1)


# In[ ]:


#newdf = newdf.drop(['uid'], axis=1)


# ### 3、训练数据准备

# In[ ]:


newdf.info(verbose=True, null_counts=True)
from sklearn.model_selection import train_test_split
X=newdf
y=newdf['label']
train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.0001,random_state=2022)
print(test_x.shape)
print(train_x.shape)
print(test_y.shape)


# In[ ]:





# In[ ]:





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

#num_bag_folds, num_stack_levels, num_bag_sets, hyperparameter_tune_kwargs, hyperparameters, refit_full.


# In[ ]:





# ### 4、训练数据

# In[ ]:


#注：训练时间较长，约为11个小时，将生成约31.5GB大小的模型文件夹
predictor = TabularPredictor(label='label', eval_metric=multilabel_categorical_crossentropy_scorer).fit(train_data=X,presets='best_quality',verbosity = 3,auto_stack=True,  num_bag_folds=8, num_bag_sets=4, num_stack_levels=3, )#'NN_TORCH':[{'ag_args_fit':{'num_gpus':1}}] ,#NeuralNetFastAI #ag_args_fit={'num_cpus': 20},hyperparameters = {'NN_TORCH': {'num_epochs': 500}, },#auto_stack=True,  num_bag_folds=5, num_bag_sets=3, num_stack_levels=3 
#predictor = TabularPredictor(label='label', eval_metric='f1').fit(train_data=X,presets='best_quality',verbosity = 3 )#'NN_TORCH':[{'ag_args_fit':{'num_gpus':1}}] ,#NeuralNetFastAI #ag_args_fit={'num_cpus': 20},hyperparameters = {'NN_TORCH': {'num_epochs': 500}, },#auto_stack=True,  num_bag_folds=5, num_bag_sets=3, num_stack_levels=3 


# In[ ]:


results = predictor.fit_summary()   #8034#"AutogluonModels/ag-20220704_164359/"


# In[ ]:


#predictor.leaderboard(train_x, silent=True)


# ### 5、预测数据

# In[ ]:


#读取生成的模型，该模型文件夹名为每次训练模型后自动生成，需自已替换，这里预置的模型即为本次比赛本队获得0.97079分数的模型，大小共31.5G，
predictor=TabularPredictor.load("AutogluonModels/ag-20220711_161627") 
#results_importance = predictor.feature_importance(X)


# In[ ]:


'''
from sklearn.metrics import confusion_matrix,accuracy_score,recall_score,f1_score,classification_report

test_data_t=test_x.drop(labels=['是否流失'],axis=1)
#模型预测
predictor=TabularPredictor.load("AutogluonModels/ag-20220619_132656/")
#可以设置不同的模型，也可以不写model，默认是最优的模型
pred=predictor.predict(test_data_t)#,model='LightGBM'
#获取准确率、召回率、F1值
cy=confusion_matrix(pred, test_y)
print("confusion_matrix:",cy)
dc=accuracy_score(pred, test_y)
print("accuracy_score",dc)
recall=recall_score(pred, test_y)
print("recall_score",recall)
f1=f1_score(pred, test_y)
print("f1_score",f1)
'''


# In[ ]:


#test_data = test_data.drop(['客户ID'], axis=1)


# In[ ]:


'''
test_data['地理区域'] = test_data['地理区域'].astype('category')
test_data['是否双频'] = test_data['是否双频'].astype('category')
test_data['是否翻新机'] = test_data['是否翻新机'].astype('category')
test_data['手机网络功能'] = test_data['手机网络功能'].astype('category')
test_data['婚姻状况'] = test_data['婚姻状况'].astype('category')
test_data['信息库匹配'] = test_data['信息库匹配'].astype('category')
test_data['新手机用户'] = test_data['新手机用户'].astype('category')
test_data['账户消费限额'] = test_data['账户消费限额'].astype('category')
test_data['信用卡指示器'] = test_data['信用卡指示器'].astype('category')
test_data['是否双频'] = test_data['是否双频'].astype('category')
'''


# In[ ]:


#df3=df.copy()


# In[ ]:


#df3 = df3.drop(['客户ID','是否流失'], axis=1)


# In[ ]:


#pd.set_option('display.max_rows',None) 


# In[ ]:


#pd.set_option('max_row',300)
#pd.set_option('display.float_format',lambda x:' %.5f' % x)


# In[ ]:


#pd.options.display.max_rows = None


# In[ ]:


#predictor.feature_importance(X)
#results_importance2.to_csv('results_importance2.csv',index=False)


# In[ ]:


test_data = test_data.drop(['uid','col_1','col_3'], axis=1)


# In[ ]:


#test_data = test_data.drop(['uid'], axis=1)


# In[ ]:


#预测数据
pred_test=predictor.predict_proba(test_data)#,model='LightGBM'


# In[ ]:


pred_test.head


# ### 7、结果输出

# In[ ]:


test_data2 = pd.read_csv('test.csv')#在特征工程代码中生成的中间文件


test_data2['label'] = pred_test[1]

test_data2[['uid','label']].to_csv('result_n_1.csv', index=False)


# In[ ]:


test_data3 = pd.read_csv('result_710_M3_9977.csv')


# In[ ]:


test_data3.loc[test_data3['label'] < 0.0001, 'label'] = 0


# In[ ]:


test_data3[['uid','label']].to_csv('result_710_M3_9997_round.csv', index=False)


# In[ ]:


test_data3.head


# In[ ]:




