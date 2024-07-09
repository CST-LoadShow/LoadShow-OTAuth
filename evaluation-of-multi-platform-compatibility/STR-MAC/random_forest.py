import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.calibration import cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, cross_val_score


def modelTrain(dataset_path, k):

    my_traces_timer = pd.read_csv(dataset_path)
    y = my_traces_timer.iloc[:, 0]
    X = my_traces_timer.iloc[:, 1:]

    forest_5k = RandomForestClassifier(n_estimators=100, random_state=42)
    # forest_5k.fit(X_train, y_train)
    scores = cross_val_score(forest_5k, X, y, cv=k)
    print("scores ", scores)
    print("mean scores", np.mean(scores))
    print("std scores", np.std(scores))

    print("五折的")
    y_train_pred = cross_val_predict(forest_5k, X, y, cv=5)
    # TODO:可以输出五折的混淆矩阵
    cm = confusion_matrix(y,y_train_pred)
    FP = cm.sum(axis=0) - np.diag(cm)  
    FN = cm.sum(axis=1) - np.diag(cm)
    TP = np.diag(cm)
    TN = cm.sum() - (FP + FN + TP)
    TPR = TP / (TP + FN)
    FPR = FP / (FP + TN)
    # print("TPR", TPR)
    # print("FPR", FPR)
    print("avg TPR", np.mean(TPR))
    print("avg FPR", np.mean(FPR))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    forest100 = RandomForestClassifier(n_estimators=100, random_state=42)
    forest100.fit(X_train, y_train)
    y_pred = forest100.predict(X_test)

    print("单次的")
    cm = confusion_matrix(y_test, y_pred)
    # print(cm)

    FP = cm.sum(axis=0) - np.diag(cm)  
    FN = cm.sum(axis=1) - np.diag(cm)
    TP = np.diag(cm)
    TN = cm.sum() - (FP + FN + TP)
    TPR = TP / (TP + FN)
    FPR = FP / (FP + TN)
    # print("TPR", TPR)
    # print("FPR", FPR)
    print("avg TPR", np.mean(TPR))
    print("avg FPR", np.mean(FPR))

    return

