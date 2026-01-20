import numpy as np
import pandas as pd
import matplotlib .pyplot as plt
import seaborn as sns



# 表示制限を解除する設定
pd.set_option('display.max_columns', None)  # 全ての列を表示
pd.set_option('display.expand_frame_repr', False)  # 折り返しを禁止

#データの読み込み
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# trainデータ testデータの結合
df = pd.concat([train, test], ignore_index=True,sort=False)
df = df.sort_values("ID")
df = df.reset_index(drop=True)

# データの行数・列数を並べて表示
print(f"Train shape: {train.shape} | Test shape: {test.shape}")

# 欠損値の数を並べて表示
print("\n--- Missing Values (Train) ---")
print(train.isnull().sum())

print("\n--- Missing Values (Test) ---")
print(test.isnull().sum())