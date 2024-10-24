#1. ARIMA 模型的时间序列预测 Baseline
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# 加载时间序列数据集（假设数据是月份和销售额的时间序列）
data = pd.read_csv('time_series_data.csv', index_col='Month', parse_dates=True)
time_series = data['Sales']

# 拆分训练和测试数据
train_data = time_series[:'2020-12']
test_data = time_series['2021-01':]

# 建立并拟合ARIMA模型
model = ARIMA(train_data, order=(5, 1, 0))  # (p, d, q) 参数：5阶自回归，1阶差分，0阶移动平均
model_fit = model.fit()

# 进行预测
forecast = model_fit.forecast(steps=len(test_data))

# 绘图
plt.figure(figsize=(10, 5))
plt.plot(train_data, label='Train')
plt.plot(test_data, label='Test')
plt.plot(test_data.index, forecast, label='Forecast', linestyle='--')
plt.legend()
plt.show()
'''
参数说明：
order (p, d, q)：ARIMA的三个参数，分别表示自回归阶数、差分次数、移动平均阶数。
model.fit()：拟合模型。
model.forecast()：对未来进行预测。
'''
#2. Prophet 模型的时间序列预测 Baseline
from fbprophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

# 加载时间序列数据集
data = pd.read_csv('time_series_data.csv')
data.columns = ['ds', 'y']  # Prophet需要特定格式，时间列必须为 'ds'，目标列必须为 'y'

# 初始化并拟合模型
model = Prophet()
model.fit(data)

# 创建未来日期的DataFrame，进行预测
future = model.make_future_dataframe(periods=12, freq='M')  # 预测未来12个月
forecast = model.predict(future)

# 绘制预测结果
model.plot(forecast)
plt.show()
'''
参数说明：
ds：时间列，必须是日期时间格式。
y：预测的目标变量。
periods：预测的时间长度。
freq：时间间隔，这里设为'M'表示按月进行预测。
'''
#3. 基于LSTM的时间序列预测 Baseline
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

# 加载时间序列数据集
data = pd.read_csv('time_series_data.csv', index_col='Month', parse_dates=True)
time_series = data['Sales']

# 数据标准化
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(time_series.values.reshape(-1, 1))

# 准备训练集和测试集
train_size = int(len(scaled_data) * 0.8)
train_data, test_data = scaled_data[:train_size], scaled_data[train_size:]

# 创建输入序列和输出序列
def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

time_step = 10  # 设置时间步长
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

# 调整输入数据的形状为LSTM所需的格式：[样本数, 时间步长, 特征数]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# 构建LSTM模型
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))  # 第一层LSTM
model.add(LSTM(50, return_sequences=False))  # 第二层LSTM
model.add(Dense(1))  # 输出层

# 编译模型
model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# 进行预测
predicted = model.predict(X_test)
predicted = scaler.inverse_transform(predicted)

# 可视化预测结果
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.plot(time_series.index[-len(y_test):], scaler.inverse_transform(y_test.reshape(-1, 1)), label='True Data')
plt.plot(time_series.index[-len(y_test):], predicted, label='Predicted Data', linestyle='--')
plt.legend()
plt.show()
'''
参数说明：
time_step：LSTM的时间步长，用于决定LSTM记忆多少历史信息。
LSTM层：50个神经元的两层LSTM，用于捕获时间序列中的长期依赖关系。
epochs：训练的轮数，决定模型训练的次数。

'''
