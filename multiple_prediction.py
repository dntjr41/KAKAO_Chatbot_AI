# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import xgboost as xgb
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score

"""Prediction / 데이터 중요도을 보여줌
Prediction - Random Forest 모델을 사용하여 학습을 진행한 후 predict_proba를 사용하여 사용자가 입력한 샘플 데이터에 대한 각 클래스별의 확률 값을 리턴
데이터 중요도 - 학습된 모델을 기반으로 데이터 중요도를 시각화하여 사진 형태로 리턴
"""

# warnings 무시
import warnings
warnings.filterwarnings('ignore')

# 데이터 읽어오기
df = pd.read_csv("result.csv")
df.drop_duplicates(keep='first', inplace=True)
df.reset_index(inplace=True, drop=True)

column_list = df.columns
print(column_list)

df.head()
df.info()

"""PREDICTION"""
# Y가 타겟
# X는 feature_columns = ['']  # json
feature_columns = [1, 2, 3, 4, 5]
X1 = df[feature_columns]
Y1 = df[0]

X_features = X1

label_encoder = LabelEncoder()
target_encoded = label_encoder.fit_transform(Y1)

# 데이터 오버샘플링
ros = RandomOverSampler(sampling_strategy='all')
X_features, target_encoded = ros.fit_resample(X_features, target_encoded)
X_train, X_test, y_train, y_test = train_test_split(X_features, target_encoded, test_size=0.2, random_state=21)


rf = RandomForestClassifier()

random_grid_rf = {'max_features': ['auto', 'sqrt'], 'min_samples_split': [2, 3, 4],
                  'min_samples_leaf': [1, 2, 3], 'max_depth': [4, 6, 8, 10, 12],
                  'n_estimators': [50, 100, 200, 250]}

rf_random = GridSearchCV(estimator=rf, param_grid=random_grid_rf, cv=3)
rf_params = rf_random.fit(X_train, y_train)
print("Hyperparameters Chosen:", rf_params.best_params_)

# 데이터 피팅
rf_classifier = RandomForestClassifier(max_depth=10, max_features='sqrt', min_samples_split=3, min_samples_leaf=1,
                                       n_estimators=200)
rf_classifier.fit(X_train, y_train)

y_test_pred = rf_classifier.predict(X_test)
y_train_pred = rf_classifier.predict(X_train)

# 모델 퍼포먼스
print("Random Forest Test Accuracy: ", round(accuracy_score(y_test, y_test_pred) * 100, 2), "%")
print("Random Forest Train Accuracy: ", round(accuracy_score(y_train, y_train_pred) * 100, 2), "%")

rf_classifier.fit(X_features, target_encoded)
y_pred = rf_classifier.predict(X_features)
print("Random Forest Model Accuracy: ", round(accuracy_score(target_encoded, y_pred) * 100, 2), "%")
print("Model F1 Score: ", round(f1_score(target_encoded, y_pred, average='weighted') * 100, 2), "%")


#Decision Tree(타겟 문항의 수가 2개면 좋은 성능을 보이긴함. 하지만 2개의 모델을 사용하고 F1 스코어를 비교하여 사용하기엔
#시간이 너무 부족하여 일단은 주석 처리
"""
dct = DecisionTreeClassifier()
dt_param = {'criterion': ['gini', 'entropy'], 'max_depth': [4, 6, 8, 10, 12]}
dt_random = GridSearchCV(dct, dt_param, cv=3)
dt_parameters = dt_random.fit(X_train, y_train)
print("Hyperparameters Chosen:", dt_parameters.best_params_)
print()

# Fitting our train data to predict sentiment on our test data
dtcModel = DecisionTreeClassifier(criterion='entropy', max_depth=12)
dtcModel.fit(X_train, y_train)
y_test_pred = dtcModel.predict(X_test)
y_train_pred = dtcModel.predict(X_train)

# Model Accuracy
print("Decision tree Test Accuracy: ", round(accuracy_score(y_test, y_test_pred) * 100, 2), "%")
print("Decision tree Train Accuracy: ", round(accuracy_score(y_train, y_train_pred) * 100, 2), "%")

# Overall Model Performance
dtcModel.fit(X_features, target_encoded)
y_pred = dtcModel.predict(X_features)
print("Decision tree Model Accuracy: ", round(accuracy_score(target_encoded, y_pred) * 100, 2), "%")
print("Model F1 Score: ", round(f1_score(target_encoded, y_pred, average='weighted') * 100, 2), "%")
"""

# 샘플데이터에 대한 예측 결과 값
X_Samples = [] # React에서 유저가 값을 보낸 것을 JSON으로 받아야함
probability = rf_classifier.predict_proba(X_Samples)
print(probability)


# 각 항목의 중요도
features = X_features.columns
importances = rf_classifier.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(8, 15))
plt.title('각 항목 중요도')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.savefig('SurMoonVey_importances.png') # 이 저장된 파일을 react가 경로로 불러와야함






