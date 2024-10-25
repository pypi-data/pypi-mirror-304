import onetouch as ot
import pandas as pd


df = pd.read_csv("datasets/climate_change_impact_on_agriculture_2024.csv")

# 指定要移动的列
column_to_move = 'Crop_Yield_MT_per_HA'

# 将指定列移动到最后
df = df[[col for col in df.columns if col != column_to_move] + [column_to_move]]

data = ot.One2Three(df)


