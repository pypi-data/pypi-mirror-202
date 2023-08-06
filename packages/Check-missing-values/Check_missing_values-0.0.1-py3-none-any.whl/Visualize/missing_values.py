
import pandas as pd
import seaborn as sns
import numpy as np


# 판다스로 결측치를 확인한 후 결측치가 있는 열을 도표 출력하는 함수
def visualizing_missing_values(link):
  df = pd.read_csv(link,encoding='utf-8') # read to csv
  null_count = df.isnull().sum() # null count
  print(null_count) 
  null_count.plot.barh(figsize=(10,7))

