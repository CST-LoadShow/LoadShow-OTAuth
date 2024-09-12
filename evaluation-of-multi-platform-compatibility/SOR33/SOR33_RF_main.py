import gc
import logging
import os
import sys
sys.path.append('..')
sys.path.append('../../')

from utils.get_feature_csv import getCsv
from utils.program_class import program_class, program_name
from random_forest import modelTrain

if __name__ == "__main__":

    # get feature csv
    print("=========== get feature csv ===========")
    feature_list = ['mean', 'std', 'max', 'min', 'range', 'CV', 'RMS', 'MAD', 'skew', 'kurt',
                    'Q1', 'Median', 'Q3', 'IQR', 'SF', 'IF', 'CF']
    file_label = os.listdir('../../dataset/9600k-2060/cpu')
    tmp = file_label[0].index("-")
    file_label = [s[tmp+1:] for s in file_label]
    file_label = ['tencent_meeting', 'formatfactory', 'wechat', 'baseline', 'matlab', 'tencent_video', 
                  'utorrent', 'qq_music', 'BaiduNetdisk', 'obs', 'spotify', 'hogwarts', 
                  'cloudmusic', 'bilibili', 'mpcbe', 'lol', 'altium_designer', 'AliyunNetdisk',
                    'pr2023', 'sunlogin', 'iQiYi', '7zip', 'zoom', 'huorong', 'audition', 'vlc', 
                    'bandicam', 'bandizip', 'unity', 'switch_audio_convert', 'potplayer', 'iZotopeRX8', 
                    'csgo', 'winrar']
    print(len(file_label))
    file = "../../dataset/9600k-2060"
    save_file = "9600_feature.csv"

    # labels = getCsv(file_label, file, 64, save_file, 16, feature_list)
    labels = file_label
    # sort labels by category
    color = ['b', 'c', 'g', 'k', 'r', 'y', 'b', 'c', 'g', 'k', 'r', 'y', 'b', 'c', 'g', 'k', 'r', 'w', 'y']
    label_text = []
    label_index = []
    color_list = []
    n = 0
    temp = "baseline"
    for key in program_class:
        if key in labels and key in file_label:
            label_text.append(key)
            label_index.append(file_label.index(key))
            if program_class[key] != temp:
                n += 1
                temp = program_class[key]
            color_list.append(color[n])
    for i in range(len(label_text)):
        label_text[i] = program_name[label_text[i]]
    # random forest train
    print("=========== train random forest ===========")
    model_save = "9600_feature.pickle"
    pic_save = 'matrix.png'
    log_save = 'log_9600_feature.txt'
    logging.basicConfig(level=logging.DEBUG,
                        filename=log_save,
                        filemode='w')

    message = modelTrain(save_file, model_save, pic_save, label_text, label_index, color_list)
    message = 'class' + str(label_text) + '\n' + message
    print(message)
    logging.info(message)
    gc.collect()
