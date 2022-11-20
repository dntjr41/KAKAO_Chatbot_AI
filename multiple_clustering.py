# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from autoelbow_rukabob import autoelbow

"""클러스터링/ 데이터 연관성을 보여줌
클러스터링 - elbow 값을 기준으로 최적의 클러스터 개수를 자동으로 계산 후, 각 데이터를 군집화하여 csv로 리턴
데이터 연관성 - 상관계수 값을 구하고 seabbons의 heatmap을 이용하여 plot 시각화 후 사진 리턴
"""

# warnings 무시
import warnings

warnings.filterwarnings('ignore')

"""데이터 로드"""
df = pd.read_csv("result.csv")
df.drop_duplicates(keep='first', inplace=True)
df.reset_index(inplace=True, drop=True)

column_list = df.columns

df.head()
df.info()

"""클러스터링"""
df = df.dropna(how='any', axis=0)

# elbow 값을 기준으로 최적의 군집 갯수 설정
n = autoelbow.auto_elbow_search(df)

# Finding cluster using Kmeans
kmean = KMeans(n_clusters=n, init="random", n_init=5)
labels = kmean.fit_predict(df)

"""결과"""
# Number of records in each cluster
for i in range(n):
    print("Cluster Predicted - ", i, ": ", len(labels[labels == i]))

df_cluster = df
df_cluster['Cluster_Predicted'] = labels
df_cluster.head()

# clustering 된 dataframe 및 각 컬럼에 대한 군집화 산점도 리턴
df_cluster.to_csv('SurMoonVey_Clustering_result.csv', index=False)


# 각 항목의 연관성 리턴
sns.set(style="white")
cor = regular_y2.corr()
f, ax = plt.subplots(figsize=(12, 12))
sns.heatmap(cor, annot=True)

plt.title('Survey data correlation', size=30)
ax.set_xticklabels(list(df.columns), size=15, rotation=90)
ax.set_yticklabels(list(df.columns), size=15, rotation=0)

plt.savefig('SurMoonVey_Corrleation.png') # 이 저장된 파일을 react가 경로로 불러와야함

