import pandas as pd
import numpy as np

d1 = {'a': [1, 2, 3], 'b': [None, 5, 6], 'c': [7, None, 9]}
d2 = {'b': [4, 89, 87], 'c': [54, 8, 35], 'd': [10, 11, 12]}

df1 = pd.DataFrame(d1)
df2 = pd.DataFrame(d2)

print(df1)
#    a    b    c
# 0  1  NaN  7.0
# 1  2  5.0  NaN
# 2  3  6.0  9.0

print(df2)
#     b   c   d
# 0   4  54  10
# 1  89   8  11
# 2  87  35  12

# Заполняем пропуски в df1 значениями из df2 по совпадающим колонкам
df3 = df1.fillna(df2)

# Приводим все значения к целочисленному типу
df3 = df3.astype(int)

print(df3)