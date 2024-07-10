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


def modelTrain(dataset_path, save_model, save_pic, label_text, label_index, color_list):

    my_traces_timer = pd.read_csv(dataset_path)
    y = my_traces_timer.iloc[:, 0]
    X = my_traces_timer.iloc[:, 1:]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    forest100 = RandomForestClassifier(n_estimators=100, random_state=42)
    forest100.fit(X_train, y_train)
    y_pred = forest100.predict(X_test)

    forest_5k = RandomForestClassifier(n_estimators=100, random_state=42)
    # forest_5k.fit(X_train, y_train)
    scores = cross_val_score(forest_5k, X, y, cv=5)
    print("scores ", scores)
    print("mean scores", np.mean(scores))
    print("std scores", np.std(scores))


    message = 'testing n_estimators=100\n' + \
              "Accuracy on test set: {:.3f}".format(forest100.score(X_test, y_test)) + '\n' + \
              classification_report(y_test, y_pred) + '\n'
   
    y_train_pred = cross_val_predict(forest_5k, X, y, cv=5)
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

    cm = confusion_matrix(y_test, y_pred)
    
    plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plot_confusion_matrix(conf_mat=cm,
                                    show_absolute=True,
                                    show_normed=False,
                                    colorbar=False,
                                    class_names=label_text,
                                    figsize=(10, 10),
                                    cmap='Blues',
                                    )
    for i in range(len(label_text)):
        ax.get_xticklabels()[i].set_color(color_list[i])  
        ax.get_yticklabels()[i].set_color(color_list[i])

    plt.xlabel("Predicted Label", fontsize=14)
    plt.ylabel("True Label", fontsize=14)
    plt.savefig(save_pic, dpi=300, bbox_inches='tight')  # , bbox_inches='tight'
    plt.close('all')

    f = open(save_model, 'wb')
    pickle.dump(forest100, f)
    f.close()

    return message

