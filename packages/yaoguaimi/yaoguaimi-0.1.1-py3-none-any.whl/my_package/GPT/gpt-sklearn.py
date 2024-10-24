#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 使用逻辑回归进行分类的Baseline代码，附带参数说明
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 加载数据集（以鸢尾花数据集为例）
data = load_iris()
X, y = data.data, data.target

# 将数据集拆分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化逻辑回归模型，并设置常用参数
model = LogisticRegression(
    max_iter=200,  # 最大迭代次数，控制优化器的收敛（常见设置在 100-500 之间）
    solver='lbfgs',  # 优化算法，适用于中小型数据集，其他可选项有：'liblinear', 'saga'
    C=1.0,  # 正则化强度的倒数；较小的值表示较强的正则化（常见设置范围为 0.01-10）
    penalty='l2'  # 正则化类型：'l2' 是默认值，适用于大多数情况
)

# 使用训练数据拟合模型
model.fit(X_train, y_train)

# 使用测试数据进行预测
y_pred = model.predict(X_test)

# 评估模型性能
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# 使用随机森林分类器进行分类的Baseline代码，附带参数说明
from sklearn.ensemble import RandomForestClassifier

# 初始化随机森林分类器，并设置常用参数
model_rf = RandomForestClassifier(
    n_estimators=100,  # 森林中树的数量（常见设置在 100-500 之间）
    max_depth=None,  # 每棵树的最大深度，'None' 表示直到所有叶子节点纯净或包含的样本少于 min_samples_split
    min_samples_split=2,  # 内部节点再分裂所需的最小样本数（常见设置在 2-10 之间）
    random_state=42  # 随机种子，用于保证结果的可复现性
)

# 使用训练数据拟合随机森林模型
model_rf.fit(X_train, y_train)

# 使用测试数据进行预测
y_pred_rf = model_rf.predict(X_test)

# 评估随机森林模型性能
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"RandomForest Accuracy: {accuracy_rf:.2f}")
print("RandomForest Classification Report:")
print(classification_report(y_test, y_pred_rf))

# 使用线性回归进行回归的Baseline代码，附带参数说明
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 加载数据集（以波士顿房价数据集为例）
data = load_boston()
X, y = data.data, data.target

# 将数据集拆分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化线性回归模型，并设置常用参数
model_lr = LinearRegression(
    fit_intercept=True,  # 是否计算截距。如果为 False，则不使用截距。
    normalize=False  # 是否在拟合前标准化回归变量。此参数已废弃，默认值为 False。
)

# 使用训练数据拟合线性回归模型
model_lr.fit(X_train, y_train)

# 使用测试数据进行预测
y_pred_lr = model_lr.predict(X_test)

# 评估线性回归模型性能
mse = mean_squared_error(y_test, y_pred_lr)
r2 = r2_score(y_test, y_pred_lr)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R2 Score: {r2:.2f}")

# 使用随机森林回归器进行回归的Baseline代码，附带参数说明
from sklearn.ensemble import RandomForestRegressor

# 初始化随机森林回归器，并设置常用参数
model_rfr = RandomForestRegressor(
    n_estimators=100,  # 森林中树的数量
    max_depth=None,  # 每棵树的最大深度
    min_samples_split=2,  # 内部节点再分裂所需的最小样本数
    random_state=42  # 随机种子，用于保证结果的可复现性
)

# 使用训练数据拟合随机森林回归器模型
model_rfr.fit(X_train, y_train)

# 使用测试数据进行预测
y_pred_rfr = model_rfr.predict(X_test)

# 评估随机森林回归器模型性能
mse_rf = mean_squared_error(y_test, y_pred_rfr)
r2_rf = r2_score(y_test, y_pred_rfr)
print(f"RandomForestRegressor Mean Squared Error: {mse_rf:.2f}")
print(f"RandomForestRegressor R2 Score: {r2_rf:.2f}")

# 使用KMeans聚类的Baseline代码，附带参数说明
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# 生成用于聚类的数据集（以make_blobs为例）
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=42)

# 初始化KMeans模型，并设置常用参数
model_kmeans = KMeans(
    n_clusters=4,  # 聚类的簇数，代表最终要分成的类的数量
    init='k-means++',  # 初始化簇中心的方法，'k-means++' 是一种加速收敛的初始化方法
    max_iter=300,  # 最大迭代次数（常见设置为 300-500）
    n_init=10,  # KMeans算法运行的次数，每次以不同的初始簇心运行，最终选择最优结果
    random_state=42  # 随机种子，用于保证结果的可复现性
)

# 使用聚类数据拟合KMeans模型
model_kmeans.fit(X)

# 获取聚类结果
labels = model_kmeans.labels_

# 打印每个样本的聚类标签
print("Cluster labels for each point:")
print(labels)

