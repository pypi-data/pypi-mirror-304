#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#2.1 列表（List）
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")  # 添加元素
fruits.remove("banana")  # 移除元素
print(fruits[1])         # 访问第二个元素，输出：cherry
#2.2 字典（Dictionary）
person = {"name": "John", "age": 25, "city": "New York"}
print(person["name"])    # 输出：John
person["age"] = 30       # 修改值
person["job"] = "Engineer"  # 添加键值对
#2.4 元组（Tuple）
numbers = (1, 2, 3, 4)
print(numbers[1])  # 访问第二个元素
#3.1 条件语句（if-else）
x = 10
if x > 5:
    print("x is greater than 5")
elif x == 5:
    print("x is equal to 5")
else:
    print("x is less than 5")
3.2 循环（for 和 while）
# for循环
for i in range(5):
    print(i)  # 输出 0, 1, 2, 3, 4

# while循环
n = 5
while n > 0:
    print(n)
    n -= 1  # 递减
4. 函数定义
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # 调用函数，输出：Hello, Alice!
#5.1 读取文件
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
#5.2 写入文件
with open('example.txt', 'w') as file:
    file.write("This is a new line of text.")
#11. 时间和日期操作
from datetime import datetime

now = datetime.now()
print("Current Date and Time:", now)
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted Time:", formatted_time)
#12. 随机数生成
import random

print(random.randint(1, 100))  # 生成1到100之间的随机整数
print(random.choice(['apple', 'banana', 'cherry']))  # 从列表中随机选择一个
#13. 使用正则表达式
import re

text = "My phone number is 123-456-7890"
pattern = r"\d{3}-\d{3}-\d{4}"
match = re.search(pattern, text)

if match:
    print("Phone number found:", match.group())
#1.1 安装代码补全与代码提示扩展
jupyterlab-lsp 是一个非常流行的扩展，用于在 JupyterLab 中实现类似于 IDE 的代码补全和提示功能。
#!pip install jupyterlab-lsp python-lsp-server
#使用 drop() 方法删除指定的列。

# 假设有一个 DataFrame df
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
})

# 删除列 'Age'
df = df.drop(columns=['Age'])
print(df)
#使用 drop() 方法删除指定的行。

# 假设我们想删除第一行
df = df.drop(index=0)
print(df)
#删除符合特定条件的行。

# 删除 Age 大于 30 的行
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
})

df = df[df['Age'] <= 30]
print(df)
#使用 dropna() 方法删除含有缺失值的行或列。

# 删除含有缺失值的行
df = df.dropna()

# 删除含有缺失值的列
df = df.dropna(axis=1)
#使用 fillna() 方法填充缺失值。

# 填充缺失值为 0
df = df.fillna(0)

# 用列的中位数填充缺失值
df['Age'] = df['Age'].fillna(df['Age'].median())
#使用 rename() 方法对列进行重命名。

# 重命名列 'Name' 为 'Full Name'
df = df.rename(columns={'Name': 'Full Name'})
print(df)
#可以使用 .loc[] 和 .iloc[] 方法对数据进行选择，或者直接通过列名称进行选择。

# 选择 'Name' 列
name_column = df['Full Name']
print(name_column)
#5.2 选择多列
# 选择 'Full Name' 和 'City' 列
df_subset = df[['Full Name', 'City']]
print(df_subset)
#5.3 使用条件选择数据
# 选择 Age 大于等于 30 的行
df_filtered = df[df['Age'] >= 30]
print(df_filtered)
#可以使用现有列的数据来创建一个新的特征列。例如，在原有的基础上计算新特征。

# 增加一个新列 'Age_in_5_years'，表示 5 年后的年龄
df['Age_in_5_years'] = df['Age'] + 5
print(df)
#使用 reset_index() 方法重设 DataFrame 的索引，尤其是在删除行之后常用。

# 重设索引并删除旧索引列
df = df.reset_index(drop=True)
print(df)
#8.1 按列拼接（concat）
data1 = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30]
})

data2 = pd.DataFrame({
    'City': ['New York', 'Los Angeles']
})

# 按列拼接
df_combined = pd.concat([data1, data2], axis=1)
print(df_combined)
#将两个数据表按行拼接起来。

# 假设我们有两个结构相同的数据表
data3 = pd.DataFrame({
    'Name': ['Charlie'],
    'Age': [35],
    'City': ['Chicago']
})

# 按行拼接
df_combined = pd.concat([df_combined, data3], axis=0)
print(df_combined)
#可以使用 groupby() 进行分组聚合操作，方便数据汇总和统计。

# 按 'City' 进行分组，并计算每个城市的平均年龄
grouped = df.groupby('City')['Age'].mean().reset_index()
print(grouped)


# In[ ]:


#1.1 导入 pandas 并转换为日期格式
import pandas as pd

# 创建一个包含日期的 DataFrame
data = {
    'date': ['2021-01-01', '2021-02-15', '2021-03-10', '2021-04-25']
}
df = pd.DataFrame(data)

# 将日期列转换为 datetime 格式
df['date'] = pd.to_datetime(df['date'])
print(df)

#2.1 提取年、月、日
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

print(df)

#提取星期几和季度信息有助于分析季节性趋势或周末效应。提取星期几 (0-6, 0 表示周一)
df['day_of_week'] = df['date'].dt.dayofweek

# 提取季度信息 (1-4)
df['quarter'] = df['date'].dt.quarter

print(df)

#有时候需要知道某个日期是一年中的第几天，可以使用 .dayofyear 属性。 提取一年中的第几天
df['day_of_year'] = df['date'].dt.dayofyear
print(df)

#3.1 提取小时、分钟、秒在某些数据集中可能包含时间信息（例如交易时间、心跳监测时间等），可以提取小时、分钟、秒等特征。

# 创建一个包含时间信息的 DataFrame
data = {
    'datetime': ['2021-01-01 10:15:30', '2021-02-15 23:45:10', '2021-03-10 12:00:00', '2021-04-25 08:30:45']
}
df = pd.DataFrame(data)

# 将 datetime 列转换为 datetime 格式
df['datetime'] = pd.to_datetime(df['datetime'])

# 提取小时、分钟、秒
df['hour'] = df['datetime'].dt.hour
df['minute'] = df['datetime'].dt.minute
df['second'] = df['datetime'].dt.second

print(df)

#4.1 计算两个日期之间的差值时间差是非常重要的特征。例如，计算两个日期之间的天数或小时数，用于分析任务完成时间、事件间隔等。
# 假设我们有一个订单提交和交付日期
df = pd.DataFrame({
    'order_date': ['2021-01-01', '2021-01-10', '2021-02-01'],
    'delivery_date': ['2021-01-05', '2021-01-15', '2021-02-05']
})

# 转换为 datetime 格式
df['order_date'] = pd.to_datetime(df['order_date'])
df['delivery_date'] = pd.to_datetime(df['delivery_date'])

# 计算交付时间差（天数）
df['delivery_time_days'] = (df['delivery_date'] - df['order_date']).dt.days

print(df)

#我们还可以计算每个时间点相对于某一基准日期的时间差，通常用于时间序列建模。

# 基准日期
base_date = pd.to_datetime('2021-01-01')

# 计算每个日期与基准日期之间的差（以天为单位）
df['days_since_base'] = (df['order_date'] - base_date).dt.days

print(df)


#有时在特征工程中，我们需要知道某一天是否为周末或某一节假日。
# 判断是否是周末
df['is_weekend'] = df['order_date'].dt.dayofweek >= 5  # 5 表示周六，6 表示周日
print(df)


#如果你有节假日列表，可以使用该列表来判断某个日期是否为节假日。
# 假设有一个节假日列表
holidays = pd.to_datetime(['2021-01-01', '2021-02-01'])

# 判断是否是节假日
df['is_holiday'] = df['order_date'].isin(holidays)
print(df)









