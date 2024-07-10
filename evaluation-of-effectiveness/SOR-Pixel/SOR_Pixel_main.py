import gc
import logging
import os
import sys

import numpy as np
sys.path.append('..')
sys.path.append('../..')
from utils.program_class import program_class, program_name
from utils.get_feature_csv import getCsv, getCsvChoose2

from RF import modelTrain
import pandas as pd

if __name__ == "__main__":

    # get feature csv
    print("=========== get feature csv ===========")
    feature_list = ['mean', 'std', 'max', 'min', 'range', 'CV', 'RMS', 'MAD', 'skew', 'kurt',
                    'Q1', 'Median', 'Q3', 'IQR', 'SF', 'IF', 'CF']
    file_cpu = "../../dataset/pixel-OTAuth"
    file_gpu = "../../dataset/pixel-OTAuth"
   

    file_label = os.listdir(os.path.join(file_cpu, "gpu"))
    tmp = file_label[0].index("-")
    file_label = [s[tmp+1:] for s in file_label]

    file_label = ['1688', 'keep', 'eleme', 'meitu', 'bilibili', 'zybang', 'iqiyi', 'redbook', 'taobao', 'mango', 
                  'fliggy', 'karaok', 'txvideo', 'baidudisk', 'amap', 
                  'anipop', 'goofish', 'migu', 'alipay', 'kuaishou', 'jd', 'yangshipin', 'homelink', 
                  'csdn', 'alidisk', 'vipshop', 'kugou_music', 'huya', 'wps', 'xigua', 'meituan', 'blackbox',
                  'zhihu', 'poizon', 'xiecheng', 'toutiao', 'netease_music', 'weibo', 'tiktok', 'tomato']


    print(len(file_label))
    
    labels = file_label
    
    save_file_cpu = "pixel_feature_cpu.csv"
    save_file_gpu = "pixel_feature_gpu.csv"

    
    # print("cpu")
    # getCsvChoose2(file_label, file_cpu, 64, save_file_cpu, 16, feature_list, choose_cpu_gpu = "cpu", size_max=32)
    # print("gpu")
    # getCsvChoose2(file_label, file_gpu, 64, save_file_gpu, 16, feature_list, choose_cpu_gpu = "gpu", size_max=32)
    

    save_file = "pixel_feature.csv"
    my_traces_timer_cpu = pd.read_csv(save_file_cpu)
    my_traces_timer_gpu = pd.read_csv(save_file_gpu)
    my_traces_timer_cpu = my_traces_timer_cpu.iloc[:, :]
    my_traces_timer_gpu = my_traces_timer_gpu.iloc[:, 1:]
    my_traces_timer = pd.concat([my_traces_timer_cpu, my_traces_timer_gpu], axis=1)
    my_traces_timer.to_csv(save_file, index=False)
    
    label_text = labels
    model_save = "feature.pickle"
    
    print("=========== dataset ===========")
    modelTrain(save_file, model_save, 'matrix.png', label_text)
    
    
    