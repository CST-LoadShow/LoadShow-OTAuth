import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, cross_val_score, KFold


def modelTrain(dataset_path):

    my_traces_timer = pd.read_csv(dataset_path)
    y = my_traces_timer.iloc[:, 0]
    X = my_traces_timer.iloc[:, 1:]

    forest_5k = RandomForestClassifier(n_estimators=100, random_state=42)
    scores = cross_val_score(forest_5k, X, y, cv=5)
    print('5-k fold cross validation:')
    print("scores ", scores)
    print("mean scores", np.mean(scores))
    print("std scores", np.std(scores))
    return
