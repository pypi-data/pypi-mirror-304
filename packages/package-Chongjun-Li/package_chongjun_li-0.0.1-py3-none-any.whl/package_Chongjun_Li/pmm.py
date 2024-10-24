import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import random


def nearest_neighbour(X_train, y_train, X_test):
    # 线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 预测缺失值
    predict_missing = model.predict(X_test)
    predict_obs = model.predict(X_train)

    # PMM 最近邻填补
    closest_indices = []
    for missing in predict_missing:
        differences = np.abs(predict_obs - missing)
        closest_index = np.argmin(differences)  # 找到最接近的那个观测值的索引
        closest_indices.append(closest_index)  # 直接添加最接近的索引

    drawn_value = y_train.iloc[closest_indices]
    return np.array(drawn_value).flatten()


def impute_missing_values(data, target_column='x', feature_column='y', iterations=50, datasets_count=5):
    imputed_datasets = []

    for dataset_num in range(datasets_count):
        data_imputed = data.copy()

        for iteration in range(iterations):
            # 获取已观察值和缺失值的训练集和测试集
            x_train_df = data_imputed.dropna(subset=[target_column])
            x_test_df = data_imputed[data_imputed[target_column].isna()]

            X_train = x_train_df[[feature_column]]
            y_train = x_train_df[target_column]
            X_test = x_test_df[[feature_column]]

            if len(X_test) > 0:
                x_filled_values = fill_missing_values(X_train, y_train, X_test)
                data_imputed.loc[data_imputed[target_column].isna(), target_column] = x_filled_values

        imputed_datasets.append(data_imputed)

    # 随机选择一个填补后的数据集
    selected_dataset = random.choice(imputed_datasets)
    return selected_dataset

# 使用示例
# 假设你有一个数据框 data，其中包含列 'x' 和 'y'
# result = impute_missing_values(data, target_column='x', feature_column='y')
# print(result)
