#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
使用附加信息预测时间序列
在实际的预测问题中，我们经常可以获得除原始时间序列值之外的其他信息。AutoGluon 支持两种类型的此类附加信息：静态特征和随时间变化的协变量。

静态特征
静态特征是时间序列中与时间无关的属性（元数据）。这些可能包括以下信息：

记录时间序列的位置（国家、州、城市）

产品的固定属性（品牌名称、颜色、尺寸、重量）

商店 ID 或产品 ID

例如，提供这些信息可能有助于预测模型为位于同一城市的商店生成类似的需求预测。

在 AutoGluon 中，静态特征存储为TimeSeriesDataFrame对象的属性。作为示例，我们来看看 M4 Daily 数据集。
'''


# In[ ]:


import pandas as pd
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor


# In[ ]:


df = pd.read_csv("https://autogluon.s3.amazonaws.com/datasets/timeseries/m4_daily_subset/train.csv")
df.head()


# In[ ]:


static_features_df = pd.read_csv("https://autogluon.s3.amazonaws.com/datasets/timeseries/m4_daily_subset/metadata.csv")
static_features_df.head()


# In[ ]:


train_data = TimeSeriesDataFrame.from_data_frame(
    df,
    id_column="item_id",
    timestamp_column="timestamp",
    static_features_df=static_features_df,
)
train_data.head()


# In[ ]:


train_data.static_features.head()


# In[ ]:


predictor = TimeSeriesPredictor(prediction_length=14).fit(train_data)


# In[ ]:


#默认情况下，此列将被解释为连续数字。我们可以通过将 dtype 更改为 来强制 AutoGluon 将其解释为分类特征category。
train_data.static_features["store_id"] = list(range(len(train_data.item_ids)))
train_data.static_features["store_id"] = train_data.static_features["store_id"].astype("category")


# In[ ]:


df_irregular = TimeSeriesDataFrame(
    pd.DataFrame(
        {
            "item_id": [0, 0, 0, 1, 1],
            "timestamp": ["2022-01-01", "2022-01-02", "2022-01-04", "2022-01-01", "2022-01-04"],
            "target": [1, 2, 3, 4, 5],
        }
    )
)
df_irregular


# In[ ]:


#处理不规则数据和缺失值
#在这种情况下，您可以在使用参数创建预测器时指定所需的频率freq。
predictor = TimeSeriesPredictor(..., freq="D").fit(df_irregular)
#AutoGluon 会自动将不规则数据转换为每日频率并处理缺失值。
df_regular = df_irregular.convert_frequency(freq="D")
df_regular
#或者，我们可以使用TimeSeriesDataFrame.fill_missing_values()以适当的策略手动填充 NaN 。默认情况下，缺失值使用前向 + 后向填充的组合进行填充。
df_filled = df_regular.fill_missing_values()
df_filled
#在某些应用（例如需求预测）中，缺失值可能对应于零需求。在这种情况下，常量填充更为合适。
df_filled = df_regular.fill_missing_values(method="constant", value=0.0)
df_filled


# In[ ]:


#如何评估预测准确率？
prediction_length = 48
data = TimeSeriesDataFrame.from_path("https://autogluon.s3.amazonaws.com/datasets/timeseries/m4_hourly_subset/train.csv")
train_data, test_data = data.train_test_split(prediction_length)


# In[ ]:


import matplotlib.pyplot as plt
import numpy as np

item_id = "H1"
fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=[10, 4], sharex=True)
train_ts = train_data.loc[item_id]
test_ts = test_data.loc[item_id]
ax1.set_title("Train data (past time series values)")
ax1.plot(train_ts)
ax2.set_title("Test data (past + future time series values)")
ax2.plot(test_ts)
for ax in (ax1, ax2):
    ax.fill_between(np.array([train_ts.index[-1], test_ts.index[-1]]), test_ts.min(), test_ts.max(), color="C1", alpha=0.3, label="Forecast horizon")
plt.legend()
plt.show()


# In[ ]:


predictor = TimeSeriesPredictor(...)
predictor.fit(train_data, presets="medium_quality")

'''
fast_training
medium_quality
high_quality
best_quality
'''
'''
ETS
AutoARIMA
Theta
SeasonalNaive
'''

'''
DeepAR

PatchTST

DLinear

TemporalFusionTransformer
'''

