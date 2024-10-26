import pandas as pd
import onetouch as ot


def parse_arff_to_df(arff_file_path):
    # 读取ARFF文件内容
    with open(arff_file_path, 'r') as file:
        lines = file.readlines()

    # 初始化变量
    data_lines = False
    attribute_lines = []
    data = []

    # 遍历ARFF文件的每一行
    for line in lines:
        # 去除行首尾的空格
        line = line.strip()

        # 如果是数据部分，则开始读取数据
        if data_lines:
            if line != '@DATA':
                data.append(line.split(','))

        # 检查数据开始的标记
        if line == '@DATA':
            data_lines = True

        # 读取属性行
        if line.startswith('@ATTRIBUTE'):
            attribute_lines.append(line.split('@ATTRIBUTE')[1].strip())

    # 创建DataFrame
    df = pd.DataFrame(data, columns=attribute_lines)

    return df


file_path = 'datasets/Dry_Bean_Dataset/Dry_Bean_Dataset.arff'

# 使用定义的函数将ARFF文件转换为DataFrame
example_data = parse_arff_to_df(file_path)

df = pd.DataFrame(example_data)

data = ot.One2Three(df)

x = pd.DataFrame([31178, 636.888, 212.9759252, 186.5620882, 1.141582018, 0.482352224, 31520, 199.2412169, 0.764110482, 0.989149746, 0.965899596, 0.935510513, 0.006830968, 0.003227429, 0.875179919, 0.999089658])

print(data.predict(x))
