from models import *
import pandas as pd
from os.path import splitext
import torch


# 新的打印方法
def printf(string, visualization=True):
    if visualization:
        print(string)


# 一键三连，实例化模型，并进行数据预处理，ai模型选取并训练，模型评估报告
class One2Three:
    def __init__(self, df: pd.DataFrame = None, label: str = None, filepath: str = None):
        self.visualization = True
        self.class_names = None
        self.format_supported = ['csv', 'xlsx']
        self.label = label
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if df is None:
            if label is not None:
                self.label = label
                if filepath is None:
                    raise FileNotFoundError("缺少文件路径或文件路径错误")
                elif splitext(filepath)[1][1:] not in self.format_supported:
                    raise FileNotFoundError(f"暂不支持{splitext(filepath)[1][1:]}形式的文件格式")
                else:

                    column_to_move = label
                    if splitext(filepath)[1][1:] == self.format_supported[0]:
                        self.df = pd.read_csv(filepath)
                    elif splitext(filepath)[1][1:] == self.format_supported[1]:
                        self.df = pd.read_excel(filepath, sheet_name=0)
                    self.df = self.df[[col for col in self.df.columns if col != column_to_move] + [column_to_move]]
            else:
                if filepath is None:
                    raise FileNotFoundError("缺少文件路径或文件路径错误")
                elif splitext(filepath)[1][1:] not in self.format_supported:
                    raise FileNotFoundError(f"暂不支持{splitext(filepath)[1][1:]}形式的文件格式")
                else:
                    if splitext(filepath)[1][1:] == self.format_supported[0]:
                        self.df = pd.read_csv(filepath)
                    elif splitext(filepath)[1][1:] == self.format_supported[1]:
                        self.df = pd.read_excel(filepath, sheet_name=0)
        else:
            if label is not None:
                self.label = label
                column_to_move = label
                self.df = df[[col for col in df.columns if col != column_to_move] + [column_to_move]]
            else:
                self.df = df

        self.X = self.df.iloc[:, :-1]
        self.Y = self.df.iloc[:, -1]

        self.model = None

        self.step = 0
        self.mission = '分类'

        self.__preprocess()
        self.__train()

    def predict(self, x):
        x = x.values

        x = torch.from_numpy(x).float().unsqueeze(0).to(self.device)

        x = x.view(-1)

        self.model.eval()
        with torch.no_grad():
            pred = self.model.forward(x)
            # 应用Softmax函数
            softmax_outputs = F.softmax(pred, dim=0)  # dim=1 指的是在类别维度上应用Softmax

            # 获取每个样本的最高置信度及其索引
            confidence, indices = softmax_outputs.max(dim=0)
            if self.mission == '分类':
                pred = self.class_names[indices]
        if self.mission == '分类':
            return str(pred), float(confidence)
        else:
            return float(pred[0])

    def __preprocess(self):
        print("主要信息:")
        print(self.df.info())
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("数据信息:")
        print(self.df.describe())
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("数据集前五项:")
        print(self.df.head())
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("数据集后五项:")
        print(self.df.tail())
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("重复值数量:")
        print(self.df.duplicated().sum())
        if self.df.duplicated().sum():
            self.df.drop_duplicates(inplace=True)
            print("已自动去重")
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("每一列列名:")
        print(self.df.columns)
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("自动判断任务类型:")
        num_class = self.df.iloc[:, -1].nunique()

        if num_class < 100:
            self.mission = '分类'
            print(self.mission)
        else:
            self.mission = '回归'
            print(self.mission)
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("数据集空值数量:")
        print(self.df.isnull().sum())
        self.df = self.df.dropna()
        print("已清除空值项")
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("修复数据集类型:")
        # 尝试将每个列转换为float
        object_columns = []
        for i, col in enumerate(self.df.columns[:-1]):
            try:
                self.df[col] = pd.to_numeric(self.df[col])
            except ValueError:
                object_columns.append(self.df.columns[i])

        new_columns = []
        # 对这些列进行独热编码，并使用0和1替代False和True
        for col in object_columns:
            new_columns.extend(pd.get_dummies(self.df[col], prefix=col).columns.tolist())
            self.df = pd.concat([self.df, pd.get_dummies(self.df[col], prefix=col)], axis=1)
            self.df.drop(col, axis=1, inplace=True)

        for col in new_columns:
            self.df[col] = self.df[col].astype(int)

        if self.mission == '分类':
            self.class_names = self.Y.unique().tolist()
            self.df[self.Y.name] = self.df[self.Y.name].astype('category').cat.codes
            self.class_names = [x for _, x in sorted(zip(self.df[self.Y.name].unique(), self.class_names), key=lambda pair: pair[0])]

        else:
            self.df[self.Y.name] = self.df[self.Y.name].astype('float64')

        # 创建一个新列顺序，其中包含除要移动的列之外的所有列，然后加上要移动的列
        new_column_order = self.df.columns.drop(self.Y.name).tolist() + [self.Y.name]
        self.df = self.df[new_column_order]
        print(self.df.dtypes)
        print("已成功修复数据集类型")
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("独特值信息及数量:")
        print(self.df.nunique())
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("数据预处理完成")
        print("数据集信息:")
        print(self.df.info())
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

    def __train(self):
        print("划分特征和标签:")
        self.X = self.df.iloc[:, :-1]
        self.Y = self.df.iloc[:, -1]
        print("特征前三项:")
        print(self.X.iloc[:3, :])
        print("标签前三项:")
        print(self.Y.iloc[:3])
        self.step += 1
        print(f"<-------------------------{self.step}------------------------->")

        print("初始化模型及参数:")
        self.model = NormalModel(self.X, self.Y, self.visualization, self.step, self.mission, self.class_names)
        self.step = self.model.step

        print("一键三连!!!")
        self.step += 1
        print(f"<-------------------------❤------------------------->")
