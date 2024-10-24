#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#1. 图像分类任务的Baseline概述 
#PyTorch是一个灵活且易用的深度学习框架，即使在CPU上也能实现简单的图像分类任务。下面我们会使用经典的MNIST数据集来进行基线模型的搭建，MNIST是一个包含手写数字（0-9）的小型图像数据集，非常适合用于快速训练和调试。

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
# 定义数据转换和加载
transform = transforms.Compose([
    transforms.ToTensor(),  # 转换为Tensor
    transforms.Normalize((0.5,), (0.5,))  # 标准化
])

# 加载训练集和测试集
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=64, shuffle=False)
#4. 构建简单的卷积神经网络模型
#我们将使用一个小型的卷积神经网络（CNN）作为Baseline模型。这个网络结构包括两个卷积层和两个全连接层，适合在CPU上训练。
# 定义卷积神经网络
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1)  # 第一层卷积
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)  # 第二层卷积
        self.fc1 = nn.Linear(32 * 7 * 7, 128)  # 全连接层1
        self.fc2 = nn.Linear(128, 10)  # 全连接层2，输出10类

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2)  # 池化层1
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)  # 池化层2
        x = x.view(-1, 32 * 7 * 7)  # 展平特征图
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 初始化模型
model = SimpleCNN()
# 损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)  # 学习率可以根据需要进行调整
# 训练模型
num_epochs = 5

for epoch in range(num_epochs):
    model.train()  # 设置模型为训练模式
    running_loss = 0.0
    for images, labels in train_loader:
        # 前向传播
        outputs = model(images)
        loss = criterion(outputs, labels)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')
# 在测试集上评估模型
model.eval()  # 设置模型为评估模式
correct = 0
total = 0

with torch.no_grad():  # 在评估时不需要计算梯度
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f'Test Accuracy: {accuracy:.2f}%')
# 保存模型
torch.save(model.state_dict(), 'simple_cnn_model.pth')

# 载入模型（如需再使用）
model = SimpleCNN()
model.load_state_dict(torch.load('simple_cnn_model.pth'))

# 假设有新的数据需要预测
new_images, _ = next(iter(test_loader))
model.eval()
predictions = model(new_images)
_, predicted_labels = torch.max(predictions, 1)

# 打印部分预测结果
print("Predicted labels:", predicted_labels[:10].numpy())
#1. 基于卷积神经网络（CNN）的图像分类Baseline
#卷积神经网络（CNN）是一种非常经典的用于图像分类的深度学习模型。以下是一个使用CIFAR-10数据集的CNN Baseline代码。
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 定义数据预处理和加载
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 加载CIFAR-10数据集
train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=64, shuffle=False)

# 定义卷积神经网络模型
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, 1, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1, 1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 10)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 初始化模型、损失函数和优化器
model = SimpleCNN()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练模型
num_epochs = 5
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')

# 评估模型性能
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f'Test Accuracy: {accuracy:.2f}%')


# In[ ]:


# 使用PyTorch进行猫狗分类的Baseline代码，附带参数说明
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

# 定义超参数
batch_size = 32  # 每个批次的样本数
learning_rate = 0.001  # 学习率
num_epochs = 10  # 训练的轮数

# 定义数据转换（包括数据预处理）
transform = transforms.Compose([
    transforms.Resize((64, 64)),  # 调整图像大小到64x64
    transforms.ToTensor(),  # 转换为张量
    transforms.Normalize((0.5,), (0.5,))  # 归一化，使图像像素值在[-1, 1]之间
])

# 加载猫狗数据集（假设使用的是本地文件夹）
dataset = datasets.ImageFolder(root='path/to/cat_dog_data', transform=transform)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

# 创建数据加载器
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 定义简单的卷积神经网络模型
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)  # 第一个卷积层，输入通道3，输出通道16，卷积核大小3x3
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)  # 第二个卷积层
        self.fc1 = nn.Linear(32 * 16 * 16, 128)  # 全连接层，输入大小32*16*16，输出大小128
        self.fc2 = nn.Linear(128, 2)  # 最后一层，输出大小为2（猫和狗）

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2, 2)  # 最大池化层
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2, 2)
        x = x.view(-1, 32 * 16 * 16)  # 展平
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 初始化模型、损失函数和优化器
model = SimpleCNN()
criterion = nn.CrossEntropyLoss()  # 交叉熵损失函数
optimizer = optim.Adam(model.parameters(), lr=learning_rate)  # Adam优化器

# 训练模型
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        # 前向传播
        outputs = model(images)
        loss = criterion(outputs, labels)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}")

# 评估模型性能
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"Test Accuracy: {accuracy:.2f}%")


# In[ ]:


# 使用PyTorch进行基本图像多分类的Baseline代码，附带参数说明
# 加载CIFAR-10数据集
cifar_transform = transforms.Compose([
    transforms.Resize((32, 32)),  # 调整图像大小到32x32
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # 归一化
])

train_dataset_cifar = datasets.CIFAR10(root='./data', train=True, download=True, transform=cifar_transform)
test_dataset_cifar = datasets.CIFAR10(root='./data', train=False, download=True, transform=cifar_transform)

train_loader_cifar = DataLoader(train_dataset_cifar, batch_size=batch_size, shuffle=True)
test_loader_cifar = DataLoader(test_dataset_cifar, batch_size=batch_size, shuffle=False)

# 定义卷积神经网络用于多分类任务（CIFAR-10）
class CIFARCNN(nn.Module):
    def __init__(self):
        super(CIFARCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.fc1 = nn.Linear(64 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 10)  # CIFAR-10有10个分类

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2, 2)
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2, 2)
        x = x.view(-1, 64 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 初始化模型、损失函数和优化器
model_cifar = CIFARCNN()
criterion_cifar = nn.CrossEntropyLoss()
optimizer_cifar = optim.Adam(model_cifar.parameters(), lr=learning_rate)

# 训练CIFAR-10模型
for epoch in range(num_epochs):
    model_cifar.train()
    running_loss = 0.0
    for images, labels in train_loader_cifar:
        # 前向传播
        outputs = model_cifar(images)
        loss = criterion_cifar(outputs, labels)

        # 反向传播和优化
        optimizer_cifar.zero_grad()
        loss.backward()
        optimizer_cifar.step()

        running_loss += loss.item()
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader_cifar):.4f}")

# 评估CIFAR-10模型性能
model_cifar.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader_cifar:
        outputs = model_cifar(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy_cifar = 100 * correct / total
print(f"CIFAR-10 Test Accuracy: {accuracy_cifar:.2f}%")

# 使用PyTorch进行手写数字识别（MNIST）的Baseline代码，附带参数说明
# 加载MNIST数据集
mnist_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_dataset_mnist = datasets.MNIST(root='./data', train=True, download=True, transform=mnist_transform)
test_dataset_mnist = datasets.MNIST(root='./data', train=False, download=True, transform=mnist_transform)

train_loader_mnist = DataLoader(train_dataset_mnist, batch_size=batch_size, shuffle=True)
test_loader_mnist = DataLoader(test_dataset_mnist, batch_size=batch_size, shuffle=False)

# 定义简单的全连接神经网络用于MNIST分类
class MNISTNN(nn.Module):
    def __init__(self):
        super(MNISTNN, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28 * 28)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 初始化模型、损失函数和优化器
model_mnist = MNISTNN()
criterion_mnist = nn.CrossEntropyLoss()
optimizer_mnist = optim.Adam(model_mnist.parameters(), lr=learning_rate)

# 训练MNIST模型
for epoch in range(num_epochs):
    model_mnist.train()
    running_loss = 0.0
    for images, labels in train_loader_mnist:

