import gc
import logging
import os
import sys
sys.path.append("..")
sys.path.append("../../")
from utils.get_feature_csv import getCsvChoose, getCsvChoose2, mergeCSV, getCsv
from utils.program_class import program_class, program_name
from random_forest import modelTrain
if __name__ == "__main__":

    # get feature csv
    print("=========== get feature csv ===========")
    feature_list = ['mean', 'std', 'max', 'min', 'range', 'CV', 'RMS', 'MAD', 'skew', 'kurt',
                    'Q1', 'Median', 'Q3', 'IQR', 'SF', 'IF', 'CF']
    file_label = os.listdir('../../dataset/div_firstpeak/Mac1/cpu')
    tmp = file_label[0].index("-")
    file_label = [s[tmp+1:] for s in file_label]

    save_file_cpu = "mac2_cpu.csv"
    save_file_gpu = "mac2_gpu.csv"
    
    # labels =['wechat', 'zoom', 'bandizip', 'qq_music', 'AliyunNetdisk', 'obs', 'BaiduNetdisk', 'bilibili', 'vlc', 'baseline', 'iQiYi', 'tencent_meeting', 'cloudmusic', 'pr2023', 'tencent_video']
  
    file2 = "../../dataset/div_firstpeak/Mac2"
    save_file2 = "STR_MAC2.csv"
    labels = ['wechat', 'zoom', 'bandizip', 'qq_music', 'AliyunNetdisk', 'obs', 'BaiduNetdisk', 'bilibili', 'vlc', 'baseline', 'iQiYi', 'tencent_meeting', 'cloudmusic', 'pr2023', 'tencent_video']

    print("cpu")
    getCsvChoose2(file_label,file2, 64, save_file_cpu, 16, feature_list, choose_cpu_gpu = "cpu", size_max=32)
    print("gpu")
    getCsvChoose2(file_label,file2, 64, save_file_gpu, 16, feature_list, choose_cpu_gpu = "gpu", size_max=32)
  
    # getCsv(file_label, file2, 64, save_file2, 16, feature_list)
    print('labels', labels)
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
   
    print("=========== STR_MAC2 ===========")
    modelTrain(save_file2, 5)
    
    print("=========== mac cpu ==============")
    modelTrain(save_file_cpu, 5)

    print("=========== mac gpu ==============")
    modelTrain(save_file_gpu, 5)


    
   