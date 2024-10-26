import pandas as pd
import onetouch as ot


file_path = 'datasets/BostonHousing.csv'

# 使用定义的函数将ARFF文件转换为DataFrame
example_data = pd.read_csv(file_path)

df = pd.DataFrame(example_data)

data = ot.One2Three(df)

x = df.loc[1].iloc[:-1]

print(data.predict(x))
