import numpy as np
import pandas as pd
import seaborn as sns
import torch
import torch.nn as nn
import torch.nn.functional as F
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from torch import optim
from torch.utils.data import TensorDataset, DataLoader, random_split
from tqdm import tqdm

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题


class NormalModel(nn.Module):
    def __init__(self, X: pd.DataFrame, Y: pd.DataFrame, visualization=True, step=0, mission='分类', class_names=None):
        super(NormalModel, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.X = torch.tensor(X.values, dtype=torch.float32).to(self.device)
        if mission == '分类':
            self.Y = torch.tensor(Y.values, dtype=torch.long).to(self.device)
        else:
            self.Y = torch.tensor(Y.values, dtype=torch.float32).to(self.device)

        self.Y_unique = int(Y.nunique())
        if class_names is None:
            self.class_names = self.Y.unique().tolist()
        else:
            self.class_names = class_names

        self.step = step
        self.visualization = visualization
        self.mission = mission

        self.hidden_size = 64
        self.mean = torch.mean(self.X, dim=0).to(self.device)
        self.std = torch.std(self.X, dim=0).to(self.device)

        self.fc1 = nn.Linear(self.X.shape[1], self.hidden_size)
        self.fc2 = nn.Linear(self.hidden_size, self.hidden_size)
        if self.mission == '分类':
            self.fc3 = nn.Linear(self.hidden_size, self.Y_unique)
        else:
            self.fc3 = nn.Linear(self.hidden_size, 1)

        self.num_epochs = 10
        self.batch_size = 16
        self.learning_rate = 0.001
        self.frequency = self.num_epochs // 10 if self.num_epochs // 10 != 0 else 1

        self.optimizer = optim.AdamW(self.parameters(), lr=self.learning_rate, weight_decay=1e-4)
        if self.mission == '分类':
            self.criterion = nn.CrossEntropyLoss().to(self.device)
        else:
            self.criterion = nn.MSELoss().to(self.device)

        self.loss = []
        self.val_loss = []
        self.test_loss = []
        self.predictions = []

        print("显示信息: ", self.visualization)
        print("num_epochs: ", self.num_epochs)
        print("batch_size: ", self.batch_size)
        print("learning_rate: ", self.learning_rate)
        print("frequency: ", self.frequency)
        print("optimizer: ", self.optimizer)
        print("loss function: ", self.criterion)
        print("device: ", self.device)
        print("初始化模型成功")
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        self.to(self.device)

        self.train_loader, self.val_loader, self.test_loader = self.__data_split()

        print("开始训练模型:")
        self.__train_model()
        self.__plot_loss()

        print("开始评估模型:")
        self.__val_model()

    def __normalize_tensor(self):
        return (self.X - self.mean) / self.std

    def __set_dataset(self):
        return TensorDataset(self.X, self.Y)

    def __data_split(self):
        # 计算数据集的大小
        dataset_size = len(self.__set_dataset())
        train_size = int(0.90 * dataset_size)
        val_size = int(0.05 * dataset_size)
        test_size = dataset_size - train_size - val_size

        # 划分数据集
        train_dataset, val_dataset, test_dataset = random_split(self.__set_dataset(), [train_size, val_size, test_size])

        # 创建DataLoader
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)

        return train_loader, val_loader, test_loader

    def forward(self, x):
        x = (x - self.mean) / self.std
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def __train_model(self):

        for epoch in tqdm(range(self.num_epochs), desc="训练中", total=self.num_epochs, unit_scale=True, smoothing=1,
                          ncols=100):
            self.train()
            for i, (inputs, targets) in enumerate(self.train_loader):
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                # 前向传播
                outputs = self.forward(inputs).squeeze(1).to(self.device)
                loss = self.criterion(outputs, targets)
                # 反向传播和优化
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            self.loss.append(loss.item())
            # 验证模型
            self.eval()  # 设置模型为评估模式
            val_loss = 0
            with torch.no_grad():
                for inputs, targets in self.val_loader:
                    outputs = self.forward(inputs).squeeze(1)
                    val_loss += self.criterion(outputs, targets).item()
            val_loss /= len(self.val_loader)
            self.val_loss.append(val_loss)

            if (epoch + 1) % self.frequency == 0:
                print(f'Epoch [{epoch + 1}/{self.num_epochs}], Loss: {loss.item():.4f}, '
                      f'Val Loss: {val_loss:.4f}')

        print("训练完成")
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")
        print(f"数据训练{self.num_epochs}步完成")
        print(f'Train Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}')
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

    def __val_model(self):
        if self.mission == '分类':
            # 初始化准确率
            correct = 0
            total = 0
            self.eval()
            # 不计算梯度
            with torch.no_grad():
                for (inputs, targets) in self.test_loader:
                    outputs = self.forward(inputs)
                    _, predicted = torch.max(outputs.data, 1)
                    total += targets.size(0)
                    correct += (predicted == targets).sum().item()

            accuracy = correct / total

            print(f"测试集准确率: {accuracy * 100:.2f}%")
            self.__plot_confusion_matrix()
        else:
            # 预测
            self.eval()
            with torch.no_grad():
                total_loss = 0
                for inputs, labels in self.test_loader:
                    # 如果有使用 GPU
                    inputs, labels = inputs.to(self.device), labels.to(self.device)

                    # 获取模型预测
                    outputs = self.forward(inputs)

                    # 计算损失（根据回归任务或分类任务选择合适的损失函数）
                    loss = self.criterion(outputs, labels)
                    total_loss += loss.item()

                    self.test_loss.append(loss.item())

                # 打印平均损失
                print(f'Average Test Loss: {total_loss / len(self.test_loss)}')
                self.__plot_accuracy()

        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

    def __plot_loss(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.loss, marker='o', linestyle='-', color='b', label='训练损失')
        plt.plot(self.val_loss, marker='o', linestyle='-', color='r', label='验证损失')
        plt.title('损失值随迭代次数变化图')
        plt.xlabel('索引')
        plt.ylabel('值')
        plt.legend()  # 显示标签
        plt.grid(True)
        plt.show()

    def __plot_accuracy(self):
        # 假设 test_loader 已经定义好，并且模型也已经训练完成
        self.eval()  # 设置模型为评估模式

        all_preds = []
        all_labels = []

        # 禁用梯度计算，只进行前向传播
        with torch.no_grad():
            for inputs, labels in self.test_loader:
                # 如果使用GPU，需要将数据移到GPU上
                inputs = inputs.to(self.device)

                # 获取预测值
                outputs = self.forward(inputs)

                # 将预测值和真实值从GPU移动到CPU，并转换为NumPy数组
                all_preds.append(outputs.cpu().numpy())
                all_labels.append(labels.cpu().numpy())

        # 将预测值和真实值拼接为一维数组
        predictions = np.concatenate(all_preds, axis=0)
        true_values = np.concatenate(all_labels, axis=0)

        # 绘制真实值和预测值的折线图
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(true_values)), true_values, label='真实值', color='blue', linestyle='-', linewidth=2)
        plt.plot(range(len(predictions)), predictions, label='预测值', color='red', linestyle='--',
                 linewidth=2)

        # 添加图例和标题
        plt.legend()
        plt.title('真实值 vs 预测值')
        plt.xlabel('样本索引')
        plt.ylabel('值')

        # 展示图表
        plt.show()

    def __plot_confusion_matrix(self):
        # 设置模型为评估模式
        self.eval()

        # 存储所有预测值和真实标签
        all_preds = []
        all_labels = []

        # 禁用梯度计算
        with torch.no_grad():
            for inputs, labels in self.test_loader:
                # 如果使用GPU，将数据放到GPU上
                inputs = inputs.to(self.device)

                # 模型预测
                outputs = self.forward(inputs)

                # 获取预测的类别（对于多分类，通常使用 torch.max）
                _, preds = torch.max(outputs, 1)

                # 将预测结果和真实标签存储到 CPU 并转换为 NumPy 数组
                all_preds.append(preds.cpu().numpy())
                all_labels.append(labels.cpu().numpy())

        # 将所有批次的预测和真实标签拼接为一维数组
        all_preds = np.concatenate(all_preds)
        all_labels = np.concatenate(all_labels)

        # 计算混淆矩阵
        cm = confusion_matrix(all_labels, all_preds)

        # 使用 seaborn 绘制带颜色编码的混淆矩阵
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=self.class_names, yticklabels=self.class_names)

        # 添加标题和标签
        plt.title('预测x真实')
        plt.xlabel('预测值')
        plt.ylabel('真实值')

        # 展示图表
        plt.show()