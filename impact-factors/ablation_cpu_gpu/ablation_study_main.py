import gc
import logging
import os
import sys
sys.path.append("..")
sys.path.append("../../")
from utils.get_feature_csv import getCsvChoose2, mergeCSV, getCsv
from utils.program_class import program_class, program_name
from random_forest import modelTrain


def ablation_cpu_gpu(file, device):
    feature_list = ['mean', 'std', 'max', 'min', 'range', 'CV', 'RMS', 'MAD', 'skew', 'kurt',
                    'Q1', 'Median', 'Q3', 'IQR', 'SF', 'IF', 'CF']


    print(f"+++++++++++++++ {device} +++++++++++++++")
    file_label = os.listdir(os.path.join(file, 'cpu'))
    tmp = file_label[0].index("-")
    file_label = [s[tmp + 1:] for s in file_label]
    save_file = [f"./file/{device}_cpu.csv", f"./file/{device}_gpu.csv", f"./file/{device}.csv"]
    # getCsvChoose2(file_label, file, 64, save_file[0], 16, feature_list, choose_cpu_gpu='cpu')
    # getCsvChoose2(file_label, file, 64, save_file[1], 16, feature_list, choose_cpu_gpu='gpu')
    # getCsv(file_label, file, 64, save_file[2], 16, feature_list)
    # random forest train
    print("=========== CPU ===========")
    modelTrain(save_file[0], 5)
    print("=========== GPU ===========")
    modelTrain(save_file[1], 5)
    print("=========== CPU+GPU ===========")
    modelTrain(save_file[2], 5)
    return


if __name__ == "__main__":
    file_list = ['../../dataset/9600k-2060',
                 '../../dataset/Mac',
                 '../../dataset/pixel-OTAuth']
    ablation_cpu_gpu(file_list[0], 'SOR33')
    ablation_cpu_gpu(file_list[1], 'STR_MAC')
    ablation_cpu_gpu(file_list[2], 'STR_Pixel')

