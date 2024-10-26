'''
1. setup 函数中的常用参数
setup 是 PyCaret 中的核心函数，用于初始化机器学习环境。

data: 传入的数据集（DataFrame）。
target: 目标列名（标签）。
train_size: 指定训练集的比例，默认为 0.7。
normalize: 是否归一化数据，布尔类型，默认为 False。
normalize_method: 归一化方法，如 'zscore', 'minmax', 'maxabs', 'robust'。
imputation_type: 缺失值填充方式，simple 或 iterative。
numeric_features: 需要强制指定为数值特征的列。
categorical_features: 需要强制指定为分类特征的列。
ignore_features: 忽略的列名。
remove_multicollinearity: 是否移除多重共线性特征，默认为 False。
polynomial_features: 是否生成多项式特征，默认为 False。
feature_interaction: 是否进行特征交互，默认为 False。
silent: 是否静默运行，跳过所有确认提示，默认为 False。
session_id: 设置随机种子以保持可重复性。

2. compare_models 函数中的常用参数
compare_models 函数用于比较所有可用的机器学习模型，并根据选择的评估指标进行排序。

fold: 交叉验证的折数，默认值为 10。
sort: 用于排序的评估指标，如 'Accuracy', 'AUC', 'Recall', 'RMSE' 等。
n_select: 选择的模型数量，默认为 1。
include: 要包含在比较中的模型列表，例如 ['rf', 'xgboost']。
3. create_model 函数中的常用参数
create_model 用于创建和训练指定的模型。

estimator: 模型的缩写名称或自定义模型对象，例如 'lr'（线性回归），'rf'（随机森林）。
fold: 用于交叉验证的折数，默认值为 10。
round: 评估结果的小数位数，默认值为 4。
cross_validation: 是否进行交叉验证，默认为 True。
verbose: 是否打印训练输出，默认值为 True。
4. tune_model 函数中的常用参数
tune_model 用于调优模型的超参数。

estimator: 需要调优的模型对象。
fold: 交叉验证的折数，默认值为 10。
n_iter: 随机搜索的迭代次数，默认值为 10。
optimize: 优化的指标，例如 'Accuracy', 'AUC', 'Recall', 'RMSE' 等。
custom_grid: 自定义的超参数网格，默认为 None。
5. plot_model 函数中的常用参数
plot_model 用于对模型进行可视化分析。

estimator: 训练后的模型对象。
plot: 可视化类型，如 'auc', 'confusion_matrix', 'feature'（特征重要性），'learning'（学习曲线）等。
save: 是否保存图表到本地文件，默认为 False。
6. evaluate_model 函数
evaluate_model 提供一个交互式界面，用于可视化模型的各种评估指标。

estimator: 训练后的模型对象，无其他参数。
7. predict_model 函数中的常用参数
predict_model 用于评估模型对新数据的预测效果。

estimator: 需要进行预测的模型对象。
data: 用于预测的数据集。
probability_threshold: 用于二分类问题的概率阈值（只在部分分类模型中使用）。

8. finalize_model 函数
finalize_model 用于将模型进行最终拟合，通常用于生产环境部署前的最终训练。

estimator: 需要最终训练的模型对象，无其他参数。

9. save_model 和 load_model 函数
save_model: 保存训练好的模型。
model: 需要保存的模型对象。
model_name: 保存的模型名称。
load_model: 加载已保存的模型。
model_name: 已保存的模型名称。
'''