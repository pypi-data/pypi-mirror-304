#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#2.1 缺失值处理
# load dataset
from pycaret.datasets import get_data
# 从本地加载数据，注意dataset是数据的文件名
data = get_data(dataset='./datasets/hepatitis', verbose=False)
# data = get_data('hepatitis',verbose=False)
# 可以看到第三行STEROID列出现NaN值
data.head()
'''
imputation_type：取值可以是 'simple' 或 'iterative'或 None。当imputation_type设置为 'simple' 时，PyCaret 将使用简单的方式（numeric_imputation和categorical_imputation）对缺失值进行填充。而当设置为 'iterative' 时，则会使用模型估计的方式（numeric_iterative_imputer，categorical_iterative_imputer）进行填充处理。如果设置为 None，则不会执行任何缺失值填充操作
numeric_imputation: 设置数值类型的缺失值，方式如下：
mean: 用列的平均值填充，默认
drop: 删除包含缺失值的行
median: 用列的中值填充
mode: 用列最常见值填充
knn: 使用K-最近邻方法拟合
int or float: 用指定值替代
categorical_imputation:
mode: 用列最常见值填充，默认
drop: 删除包含缺失值的行
str: 用指定字符替代
numeric_iterative_imputer: 使用估计模型拟合值，可输入str或sklearn模型, 默认使用lightgbm
categorical_iterative_imputer: 使用估计模型差值，可输入str或sklearn模型, 默认使用lightgbm
'''


# In[ ]:


# 使用均值填充数据
from pycaret.classification import ClassificationExperiment
s = ClassificationExperiment()
# 均值
# s.data['STEROID'].mean()
s.setup(data = data, session_id=0, target = 'Class',verbose=False, 
        # 设置data_split_shuffle和data_split_stratify为False不打乱数据
        data_split_shuffle = False, data_split_stratify = False,
        imputation_type='simple', numeric_iterative_imputer='drop')
# 查看转换后的数据
s.get_config('dataset_transformed').head()


# In[ ]:


# 使用knn拟合数据
from pycaret.classification import ClassificationExperiment
s = ClassificationExperiment()
s.setup(data = data, session_id=0, target = 'Class',verbose=False, 
        # 设置data_split_shuffle和data_split_stratify为False不打乱数据
        data_split_shuffle = False, data_split_stratify = False,
        imputation_type='simple', numeric_imputation = 'knn')
# 查看转换后的数据
s.get_config('dataset_transformed').head()


# In[ ]:


# 使用lightgbmn拟合数据
# from pycaret.classification import ClassificationExperiment
# s = ClassificationExperiment()
# s.setup(data = data, session_id=0, target = 'Class',verbose=False, 
#         # 设置data_split_shuffle和data_split_stratify为False不打乱数据
#         data_split_shuffle = False, data_split_stratify = False,
#         imputation_type='iterative', numeric_iterative_imputer = 'lightgbm')
# 查看转换后的数据
# s.get_config('dataset_transformed').head()


# In[ ]:


'''
2.2 类型转换
虽然 PyCaret具有自动识别特征类型的功能，但PyCaret提供了数据类型自定义参数，用户可以对数据集进行更精细的控制和指导，以确保模型训练和特征工程的效果更加符合用户的预期和需求。这些自定义参数如下：

numeric_features：用于指定数据集中的数值特征列的参数。这些特征将被视为连续型变量进行处理
categorical_features：用于指定数据集中的分类特征列的参数。这些特征将被视为离散型变量进行处理
date_features：用于指定数据集中的日期特征列的参数。这些特征将被视为日期型变量进行处理
create_date_columns：用于指定是否从日期特征中创建新的日期相关列的参数
text_features：用于指定数据集中的文本特征列的参数。这些特征将被视为文本型变量进行处理
text_features_method：用于指定对文本特征进行处理的方法的参数
ignore_features：用于指定在建模过程中需要忽略的特征列的参数
keep_features：用于指定在建模过程中需要保留的特征列的参数
'''


# In[ ]:


# 转换变量类型
from pycaret.datasets import get_data
data = get_data(dataset='./datasets/hepatitis', verbose=False)
 
from pycaret.classification import *
s = setup(data = data, target = 'Class', ignore_features  = ['SEX','AGE'], categorical_features=['STEROID'],verbose = False,
         data_split_shuffle = False, data_split_stratify = False)


# In[ ]:


# 查看转换后的数据，前两列消失，STEROID变为分类变量
s.get_config('dataset_transformed').head()


# In[ ]:


'''
2.3 独热编码
当数据集中包含分类变量时，这些变量通常需要转换为模型可以理解的数值形式。独热编码是一种常用的方法，它将每个分类变量转换为一组二进制变量，其中每个变量对应一个可能的分类值，并且只有一个变量在任何给定时间点上取值为 1，其余变量均为 0。可以通过传递参数categorical_features来指定要进行独热编码的列。例如：
'''


# In[ ]:


# load dataset
from pycaret.datasets import get_data
data = get_data(dataset='./datasets/pokemon', verbose=False)
# data = get_data('pokemon')
data.head()


# In[ ]:


# 对Type 1实现独热编码
len(set(data['Type 1']))


# In[ ]:


from pycaret.classification import *
s = setup(data = data, categorical_features =["Type 1"],target = 'Legendary', verbose=False)
# 查看转换后的数据Type 1变为独热编码
s.get_config('dataset_transformed').head()


# In[ ]:


'''
2.4 数据平衡
在 PyCaret 中，fix_imbalance 和 fix_imbalance_method 是用于处理不平衡数据集的两个参数。这些参数通常用于在训练模型之前对数据集进行预处理，以解决类别不平衡问题。

fix_imbalance 参数：这是一个布尔值参数，用于指示是否对不平衡数据集进行处理。当设置为 True 时，PyCaret 将自动检测数据集中的类别不平衡问题，并尝试通过采样方法来解决。当设置为 False 时，PyCaret 将使用原始的不平衡数据集进行模型训练
fix_imbalance_method 参数：这是一个字符串参数，用于指定处理不平衡数据集的方法。可选的值包括：
使用 SMOTE（Synthetic Minority Over-sampling Technique）来生成人工合成样本，从而平衡类别（默认参数smote）
使用imbalanced-learn提供的估算模型
'''


# In[ ]:


# 加载数据
from pycaret.datasets import get_data
data = get_data(dataset='./datasets/credit', verbose=False)
# data = get_data('credit')
data.head()


# In[ ]:


# 查看数据各类别数
category_counts = data['default'].value_counts()
category_counts
from pycaret.classification import *
s = setup(data = data, target = 'default', fix_imbalance = True, verbose = False)
# 可以看到类1数据量变多了
s.get_config('dataset_transformed')['default'].value_counts()


# In[ ]:


'''
2.5 异常值处理
PyCaret的remove_outliers函数可以在训练模型之前识别和删除数据集中的异常值。它使用奇异值分解技术进行PCA线性降维来识别异常值，并可以通过setup中的outliers_threshold参数控制异常值的比例（默认0.05）。
'''


# In[ ]:


from pycaret.datasets import get_data
 
data = get_data(dataset='./datasets/insurance', verbose=False)
# insurance = get_data('insurance')
# 数据维度
data.shape


# In[ ]:


from pycaret.regression import *
s = setup(data = data, target = 'charges', remove_outliers = True ,verbose = False, outliers_threshold = 0.02)
# 移除异常数据后，数据量变少
s.get_config('dataset_transformed').shape


# In[ ]:


'''
2.6 特征重要性
特征重要性是一种用于选择数据集中对预测目标变量最有贡献的特征的过程。与使用所有特征相比，仅使用选定的特征可以减少过拟合的风险，提高准确性，并缩短训练时间。在PyCaret中，可以通过使用feature_selection参数来实现这一目的。对于PyCaret中几个与特征选择相关参数的解释如下：

feature_selection：用于指定是否在模型训练过程中进行特征选择。可以设置为 True 或 False。
feature_selection_method：特征选择方法：
'univariate': 使用sklearn的SelectKBest，基于统计测试来选择与目标变量最相关的特征。
'classic（默认）': 使用sklearn的SelectFromModel，利用监督学习模型的特征重要性或系数来选择最重要的特征。
'sequential': 使用sklearn的SequentialFeatureSelector，该类根据指定的算法（如前向选择、后向选择等）以及性能指标（如交叉验证得分）逐步选择特征。
n_features_to_select：特征选择的最大特征数量或比例。如果<1，则为起始特征的比例。默认为0.2。该参数在计数时不考虑 ignore_features 和 keep_features 中的特征。
'''


# In[ ]:


from pycaret.datasets import get_data
data = get_data('./datasets/diabetes')
from pycaret.regression import *
# feature_selection选择特征, n_features_to_select选择特征比例
s = setup(data = data, target = 'Class variable', feature_selection = True, feature_selection_method = 'univariate',
          n_features_to_select = 0.3, verbose = False)
# 查看哪些特征保留下来
s.get_config('X_transformed').columns
s.get_config('X_transformed').head()


# In[ ]:


'''
2.7 归一化
数据归一化

在 PyCaret 中，normalize 和 normalize_method 参数用于数据预处理中的特征缩放操作。特征缩放是指将数据的特征值按比例缩放，使之落入一个小的特定范围，这样可以消除特征之间的量纲影响，使模型训练更加稳定和准确。下面是关于这两个参数的说明：

normalize: 这是一个布尔值参数，用于指定是否对特征进行缩放。默认情况下，它的取值为 False，表示不进行特征缩放。如果将其设置为 True，则会启用特征缩放功能。
normalize_method: 这是一个字符串参数，用于指定特征缩放的方法。可选的值有：
zscore（默认）: 使用 Z 分数标准化方法，也称为标准化或 Z 标准化。该方法将特征的值转换为其 Z 分数，即将特征值减去其均值，然后除以其标准差，从而使得特征的均值为 0，标准差为 1。
minmax: 使用 Min-Max 标准化方法，也称为归一化。该方法将特征的值线性转换到指定的最小值和最大值之间，默认情况下是 [0, 1] 范围。
maxabs: 使用 MaxAbs 标准化方法。该方法将特征的值除以特征的最大绝对值，将特征的值缩放到 [-1, 1] 范围内。
robust: 使用 RobustScaler 标准化方法。该方法对数据的每个特征进行中心化和缩放，使用特征的中位数和四分位数范围来缩放特征。
'''


# In[ ]:


from pycaret.datasets import get_data
data = get_data('./datasets/pokemon')
data.head()
# 归一化
from pycaret.classification import *
s = setup(data, target='Legendary', normalize=True, normalize_method='robust', verbose=False)


# In[ ]:


'''
特征变换

归一化会重新调整数据，使其在新的范围内，以减少方差中幅度的影响。特征变换是一种更彻底的技术。通过转换改变数据的分布形状，使得转换后的数据可以被表示为正态分布或近似正态分布。PyCaret中通过transformation参数开启特征转换，transformation_method设置转换方法：yeo-johnson（默认）和分位数。此外除了特征变换，还有目标变换。目标变换它将改变目标变量而不是特征的分布形状。此功能仅在pycarte.regression模块中可用。使用transform_target开启目标变换，transformation_method设置转换方法。
'''


# In[ ]:


from pycaret.classification import *
s = setup(data = data, target = 'Legendary', transformation = True, verbose = False)
# 特征变换结果
s.get_config('X_transformed').head()


# In[ ]:




