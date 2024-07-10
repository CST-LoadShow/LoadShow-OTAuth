import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import sys
sys.path.append("..")
from utils.feature_api import getFeature



def getCsv_matrix(f, size, n, dataset_list, _file, maximum=200):

    f_cpu = os.path.join(f, 'cpu')
    f_gpu = os.path.join(f, 'gpu')
    cpu_list1 = os.listdir(f_cpu)
    _ = cpu_list1[0].split('-')
    cpu_label_before = _[0]
    
    gpu_list1 = os.listdir(f_gpu)
    _ = gpu_list1[0].split('-')
    gpu_label_before = _[0]

    dataset = np.empty(shape=(0, size * 2 * n))
    label = []
    for i in range(len(file_label)):
        cpu_temp_file_name = f'{cpu_label_before}-{file_label[i]}'
        gpu_temp_file_name = f'{gpu_label_before}-{file_label[i]}'
       
        if cpu_temp_file_name not in cpu_list1 or gpu_temp_file_name not in gpu_list1:
            print("label error")
            exit()
       
        path = os.path.join(f_cpu, cpu_temp_file_name)
        fs = os.listdir(path)
        # print(path)
        data_cpu = np.empty(shape=(0, size * n))
        for j in range(len(dataset_list)):
            if j >= maximum:
                break
            csv_f = os.path.join(path, str(dataset_list[j]) + '.csv')
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)
            data = data.reshape(-1, size * n)
            data_cpu = np.vstack([data_cpu, data])
        data_gpu = np.empty(shape=(0, size * n))
        path = os.path.join(f_gpu, gpu_temp_file_name)
        fs = os.listdir(path)
        for j in range(len(dataset_list)):
            if j >= maximum:
                break
            csv_f = os.path.join(path, str(dataset_list[j]) + '.csv')
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)
            data = data.reshape(-1, size * n)
            data_gpu = np.vstack([data_gpu, data])
        count = min(len(data_cpu), len(data_gpu))
        data_cpu_gpu = np.hstack((data_cpu[:count, :], data_gpu[:count, :]))
        dataset = np.vstack([dataset, data_cpu_gpu])
        label += count * [[file_label[i]]]
        # print(f"{file_label[i]}  count: {count} label: {i}")

    label = np.array(label)
    last_data = np.hstack((label, dataset))
    head = ['label'] + list(range(size * 2 * n))
    df = pd.DataFrame(data=last_data)
    df.columns = head
    df.to_csv(_file, index=False)
    return file_label


def getCsvFeature(f, size, dataset_list, _file, f_list, maximum=200):
    feature_n = len(f_list)
    f_cpu = os.path.join(f, 'cpu')
    f_gpu = os.path.join(f, 'gpu')
    
    cpu_list1 = os.listdir(f_cpu)
    _ = cpu_list1[0].split('-')
    cpu_label_before = _[0]
    
    gpu_list1 = os.listdir(f_gpu)
    _ = gpu_list1[0].split('-')
    gpu_label_before = _[0]

    dataset = np.empty(shape=(0, 16 * feature_n * 2))
    label = []
    for i in range(len(file_label)):
        cpu_temp_file_name = f'{cpu_label_before}-{file_label[i]}'
        gpu_temp_file_name = f'{gpu_label_before}-{file_label[i]}'
       
        if cpu_temp_file_name not in cpu_list1 or gpu_temp_file_name not in gpu_list1:
            print("label error")
            exit()
       
        path = os.path.join(f_cpu, cpu_temp_file_name)
        fs = os.listdir(path)
        feature_cpu = np.empty(shape=(0, 16 * feature_n))
        for f in dataset_list:
            csv_f = os.path.join(path, str(f) + '.csv')
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // size):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * size:(x + 1) * size, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu = np.concatenate((feature_cpu, feature), axis=0)

        feature_gpu = np.empty(shape=(0, 16 * feature_n))
        path = os.path.join(f_gpu, gpu_temp_file_name)

        for f in dataset_list:
            csv_f = os.path.join(path, str(f) + '.csv')
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)
            for x in range(data.shape[0] // size):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * size:(x + 1) * size:, j])))
                feature = np.expand_dims(feature, 0)
                feature_gpu = np.concatenate((feature_gpu, feature), axis=0)

        count = min(feature_cpu.shape[0], feature_gpu.shape[0])
        feature_cpu_gpu = np.hstack((feature_cpu[:count, :], feature_gpu[:count, :]))
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[file_label[i]]]
        # print(f"{file_label[i]}  count: {count} label: {i}")

    label = np.array(label)
    last_data = np.hstack((label, dataset))
    s = []
    for i in range(16):
        for j in range(feature_n):
            s.append(str(i) + f_list[j])
    s = s + s
    head = ['label'] + s
    df = pd.DataFrame(data=last_data)
    df.columns = head
    df.to_csv(_file, index=False)
    return file_label


def modelTrain(train_dataset_path, test_dataset_path):
    my_traces_timer = pd.read_csv(train_dataset_path)
    y_train = my_traces_timer.iloc[:, 0]
    X_train = my_traces_timer.iloc[:, 1:]

    my_traces_timer_test = pd.read_csv(test_dataset_path)
    y_test = my_traces_timer_test.iloc[:, 0]
    X_test = my_traces_timer_test.iloc[:, 1:]

    forest100 = RandomForestClassifier(n_estimators=100, random_state=0)
    forest100.fit(X_train, y_train)
    test_acc = forest100.score(X_test, y_test)

    return test_acc


if __name__ == "__main__":
    # random choose 20% of data as test data
    np.random.seed(42)
    E = np.arange(1, 33)
    np.random.shuffle(E)
    print(E)
    file = "../../dataset/pixel-OTAuth/"
    global_list = file_label = ['1688', 'keep', 'eleme', 'meitu', 'bilibili', 'zybang', 'iqiyi', 'redbook', 'taobao', 'mango', 
                  'fliggy', 'karaok', 'txvideo', 'baidudisk', 'amap', 
                  'anipop', 'goofish', 'migu', 'alipay', 'kuaishou', 'jd', 'yangshipin', 'homelink', 
                  'csdn', 'alidisk', 'vipshop', 'kugou_music', 'huya', 'wps', 'xigua', 'meituan', 'blackbox',
                  'zhihu', 'poizon', 'xiecheng', 'toutiao', 'netease_music', 'weibo', 'tiktok', 'tomato']

 
  
    global_acc_no_feature = []
    global_acc_feature = []

    test_size = 6  # int  (32*0.2)  26
    train_size = [2,4,8,16,22,26]
    split_list = [8, 16, 32, 64]
                  
    test_list = E[:test_size]

    # no feature
    print("==============  no feature test ==============")
    for j in range(len(split_list)):
        print(f'---------- split {split_list[j]} ------------')
        save_file_test = "./file/pixel_test%d.csv" % split_list[j]
        # labels = getCsv_matrix(file, 16, split_list[j], test_list, save_file_test)
        same_split_acc = []
        for k in range(len(train_size)):
            print(f'---------- train size {train_size[k]} ------------')
            save_file = "./file/pixel_train_%d_%d.csv" % (train_size[k], split_list[j])
            train_list = E[test_size: train_size[k] + test_size]
            # labels = getCsv_matrix(file, 16, split_list[j], train_list, save_file)
            acc = modelTrain(save_file, save_file_test)
            same_split_acc.append(acc)
            print("acc", acc)
        global_acc_no_feature.append(same_split_acc)
    print("==============  no feature test acc ==============")
    print(global_acc_no_feature)

    # have feature
    print("==============  have feature test ==============")
    feature_list = ['mean', 'std', 'max', 'min', 'range', 'CV', 'RMS', 'MAD', 'skew', 'kurt',
                    'Q1', 'Median', 'Q3', 'IQR', 'SF', 'IF', 'CF']
    for j in range(len(split_list)):
        print(f'---------- split {split_list[j]} ------------')
        save_file_test = "./file/pixel_test_feature_%d.csv" % split_list[j]
        # labels = getCsvFeature(file, split_list[j], test_list, save_file_test, feature_list)
        same_split_acc = []
        for k in range(len(train_size)):
            print(f'---------- train size {train_size[k]} ------------')
            save_file = "./file/pixel_train_feature_%d_%d.csv" % (train_size[k], split_list[j])
            train_list = E[test_size: train_size[k] + test_size]
            # labels = getCsvFeature(file, split_list[j],  train_list, save_file, feature_list)
            acc = modelTrain(save_file, save_file_test)
            same_split_acc.append(acc)
            print("acc", acc)
        global_acc_feature.append(same_split_acc)
    print("==============  have feature test acc ==============")
    print(global_acc_feature)