import gc
import logging
import os
import sys
sys.path.append("..")
from utils.get_feature_csv import getCsvGet
from RF import modelTrain

def testOneCase(file):
     # get feature csv
    # print("=========== get feature csv ===========")
    feature_list = ['mean', 'std', 'max', 'min', 'range', 'CV', 'RMS', 'MAD', 'skew', 'kurt',
                    'Q1', 'Median', 'Q3', 'IQR', 'SF', 'IF', 'CF']
    
    file_label = os.listdir(file)
    tmp = file_label[0].index("-")
    file_label = [s[tmp+1:] for s in file_label]
    _ = file.split("/")[-1]
    save_file = f"./file/{_}.csv"

    labels = getCsvGet(file_label, file, 64, save_file, 16, feature_list)
   
    # print("=========== train random forest ===========")
    model_save = f"./file/{_}_feature.pickle"
    pic_save = f'./file/{_}_matrix.png'
    label_text = labels
    message, acc= modelTrain(save_file, model_save, pic_save, label_text)
    # message = 'class' + str(label_text) + '\n' + message
    # print(message)
    return acc


if __name__ == "__main__":

    file_list = [
        "../dataset/div_firstpeak/cause/case1",
        "../dataset/div_firstpeak/cause/case2",
        "../dataset/div_firstpeak/cause/case3",
        "../dataset/div_firstpeak/cause/case4",
        "../dataset/div_firstpeak/cause/case5",
        "../dataset/div_firstpeak/cause/case6",
    ]
    acc_list = []
    for file in file_list:
        acc = testOneCase(file)
        print(f'{file.split("/")[-1]} acc: {acc}')
        acc_list.append(acc)
   
    print(acc_list)


