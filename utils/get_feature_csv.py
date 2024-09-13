import os

import numpy as np
import pandas as pd

from utils.feature_api import getFeature


def getCsv(file_label, f, length, save_path, size, feature_list, size_max=128):
    feature_n = len(feature_list)
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
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path,  fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu = np.concatenate((feature_cpu, feature), axis=0)

        feature_gpu = np.empty(shape=(0, 16 * feature_n))
        
        path = os.path.join(f_gpu, gpu_temp_file_name)
        fs = os.listdir(path)

        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length:, j])))
                feature = np.expand_dims(feature, 0)
                feature_gpu = np.concatenate((feature_gpu, feature), axis=0)

        count = min(feature_cpu.shape[0], feature_gpu.shape[0])
        feature_cpu_gpu = np.hstack((feature_cpu[:count, :], feature_gpu[:count, :]))
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[i]]
        print(f"{file_label[i]}  count: {count} label: {i}")
        
    label = np.array(label)
    last_data = np.hstack((label, dataset))
    s = []
    for i in range(size):
        for j in range(feature_n):
            s.append(str(i) + feature_list[j])
    s = s + s
    head = ['label'] + s
    df = pd.DataFrame(data=last_data)
    df.columns = head
    df.to_csv(save_path, index=False)
    return file_label


def getCsvNp(file_label, f, length, size, feature_list, size_max=128):
    feature_n = len(feature_list)
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
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path,  fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu = np.concatenate((feature_cpu, feature), axis=0)

        feature_gpu = np.empty(shape=(0, 16 * feature_n))
        
        path = os.path.join(f_gpu, gpu_temp_file_name)
        fs = os.listdir(path)

        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length:, j])))
                feature = np.expand_dims(feature, 0)
                feature_gpu = np.concatenate((feature_gpu, feature), axis=0)

        count = min(feature_cpu.shape[0], feature_gpu.shape[0])
        feature_cpu_gpu = np.hstack((feature_cpu[:count, :], feature_gpu[:count, :]))
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[i]]
        print(f"{file_label[i]}  count: {count} label: {i}")
        
    label = np.array(label)
    last_data = np.hstack((label, dataset))

    return last_data


def getCsvNpSoftware(f, length, size, feature_list, name, label_input, size_max=128):
    feature_n = len(feature_list)

    f_cpu = os.path.join(f, 'cpu')
    f_gpu = os.path.join(f, 'gpu')

    cpu_list1 = os.listdir(f_cpu)
    gpu_list1 = os.listdir(f_gpu)
    # program_list = []
    # for i in range(len(cpu_list1)):
    #     if name in cpu_list1[i]:
    #         program_list.append(cpu_list1[i].split('-')[-1].split('(')[0])
    # program_list = list(set(program_list))
    # _ = cpu_list1[0].index('-')
    print(name)
    print(label_input)
    action_list = []
    for i in range(len(cpu_list1)):
        if name == 'baseline':
            action_list.append('chrome')
            break
        elif name in cpu_list1[i] and cpu_list1[i].split('(')[-1][:-1] != 'file_preview':
            action_list.append(cpu_list1[i].split('(')[-1][:-1])

    action_list.sort()
    print(action_list)
    cpu_prefix = cpu_list1[0].split('-')[0]
    gpu_prefix = gpu_list1[0].split('-')[0]

    dataset = np.empty(shape=(0, 16 * feature_n * 2))
    label = []
    for i in range(len(action_list)):
        if name == 'baseline':
            path = os.path.join(f_cpu, f"{cpu_prefix}-{name}")
        else:
            path = os.path.join(f_cpu, f"{cpu_prefix}-{name}({action_list[i]})")
        fs = os.listdir(path)
        feature_cpu = np.empty(shape=(0, 16 * feature_n))
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu = np.concatenate((feature_cpu, feature), axis=0)

        feature_gpu = np.empty(shape=(0, 16 * feature_n))
        if name == 'baseline':
            path = os.path.join(f_gpu, f"{gpu_prefix}-{name}")
        else:
            path = os.path.join(f_gpu, f"{gpu_prefix}-{name}({action_list[i]})")
        fs = os.listdir(path)

        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length:, j])))
                feature = np.expand_dims(feature, 0)
                feature_gpu = np.concatenate((feature_gpu, feature), axis=0)

        count = min(feature_cpu.shape[0], feature_gpu.shape[0])
        feature_cpu_gpu = np.hstack((feature_cpu[:count, :], feature_gpu[:count, :]))
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[label_input]]
    label = np.array(label)
    last_data = np.hstack((label, dataset))

    return last_data


def getCsvNpSoftware2(file_label, f, length, size, feature_list, name, size_max=128):
    feature_n = len(feature_list)

    f_cpu = os.path.join(f, 'cpu')
    f_gpu = os.path.join(f, 'gpu')

    cpu_list1 = os.listdir(f_cpu)
    gpu_list1 = os.listdir(f_gpu)
    # program_list = []
    # for i in range(len(cpu_list1)):
    #     if name in cpu_list1[i]:
    #         program_list.append(cpu_list1[i].split('-')[-1].split('(')[0])
    # program_list = list(set(program_list))
    # _ = cpu_list1[0].index('-')

    action_list = []
    for i in range(len(cpu_list1)):
        if name in cpu_list1[i] and cpu_list1[i].split('(')[-1][:-1] != 'file_preview':
        # if name in cpu_list1[i] and cpu_list1[i].split('(')[-1][:-1] != 'video' and cpu_list1[i].split('(')[-1][:-1] != 'file_preview':
            action_list.append(cpu_list1[i].split('(')[-1][:-1])

    action_list.sort()
    cpu_prefix = cpu_list1[0].split('-')[0]
    gpu_prefix = gpu_list1[0].split('-')[0]

    dataset = np.empty(shape=(0, 16 * feature_n * 2))
    label = []
    for i in range(len(action_list)):
        path = os.path.join(f_cpu, f"{cpu_prefix}-{name}({action_list[i]})")
        fs = os.listdir(path)
        feature_cpu = np.empty(shape=(0, 16 * feature_n))
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu = np.concatenate((feature_cpu, feature), axis=0)

        feature_gpu = np.empty(shape=(0, 16 * feature_n))
        path = os.path.join(f_gpu, f"{gpu_prefix}-{name}({action_list[i]})")
        fs = os.listdir(path)

        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length:, j])))
                feature = np.expand_dims(feature, 0)
                feature_gpu = np.concatenate((feature_gpu, feature), axis=0)

        count = min(feature_cpu.shape[0], feature_gpu.shape[0])
        feature_cpu_gpu = np.hstack((feature_cpu[:count, :], feature_gpu[:count, :]))
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[i]]
    label = np.array(label)
    last_data = np.hstack((label, dataset))

    return last_data, action_list


def getCsvChoose(file_label, f, length, save_path, size, feature_list, choose_cpu_gpu='cpu', size_max=128):

    feature_n = len(feature_list)
    f_cpu_gpu = os.path.join(f, choose_cpu_gpu)
    list1 = os.listdir(f_cpu_gpu)
    _ = list1[0].index('-')
    list2 = [s[_ + 1:] for s in list1]
    dataset = np.empty(shape=(0, 16 * feature_n))
    label = []
    for i in range(len(list1)):
        if list2[i] not in file_label:
            continue
        path = os.path.join(f_cpu_gpu, list1[i])
        fs = os.listdir(path)
        feature_cpu_gpu = np.empty(shape=(0, 16 * feature_n))
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path,  fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu_gpu = np.concatenate((feature_cpu_gpu, feature), axis=0)
        print(f'name: {list2[i]}; counet: {feature_cpu_gpu.shape[0]}; label: {file_label.index(list2[i])}')
        count = feature_cpu_gpu.shape[0]
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[file_label.index(list2[i])]]
    label = np.array(label)
    last_data = np.hstack((label, dataset))
    s = []
    for i in range(size):
        for j in range(feature_n):
            s.append(str(i) + feature_list[j])
    # s = s + s
    head = ['label'] + s
    df = pd.DataFrame(data=last_data)
    df.columns = head
    df.to_csv(save_path, index=False)
    return list2

def getCsvGet(file_label, f, length, save_path, size, feature_list, size_max=128):

    feature_n = len(feature_list)
    f_cpu_gpu = f
    list1 = os.listdir(f_cpu_gpu)
    _ = list1[0].split('-')
    label_before = _[0]
    
    dataset = np.empty(shape=(0, 16 * feature_n))
    label = []
    for i in range(len(file_label)):
        temp_file_name = f'{label_before}-{file_label[i]}'
        if temp_file_name not in list1:
            continue
        path = os.path.join(f_cpu_gpu, temp_file_name)
        fs = os.listdir(path)
        fs.sort()
        # print(fs)
        feature_cpu_gpu = np.empty(shape=(0, 16 * feature_n))
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path,  fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu_gpu = np.concatenate((feature_cpu_gpu, feature), axis=0)
        # print(f'name: {list2[i]}; counet: {feature_cpu_gpu.shape[0]}; label: {file_label.index(list2[i])}')
        count = feature_cpu_gpu.shape[0]
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[i]]
    label = np.array(label)
    last_data = np.hstack((label, dataset))
    s = []
    for i in range(size):
        for j in range(feature_n):
            s.append(str(i) + feature_list[j])
    # s = s + s
    head = ['label'] + s
    df = pd.DataFrame(data=last_data)
    df.columns = head
    df.to_csv(save_path, index=False)
    return file_label


def mergeCSV(file_list, save_file):
    data = ''
    for j in range(len(file_list)):
        if j == 0:
            data = pd.read_csv(file_list[j])
        else:
            data = pd.concat([data, pd.read_csv(file_list[j])], axis=0)
    data.to_csv(save_file, index=False)
    return


def getCsvChoose2(file_label, f, length, save_path, size, feature_list, choose_cpu_gpu='cpu', size_max=128):
    feature_n = len(feature_list)
    f_cpu_gpu = os.path.join(f, choose_cpu_gpu)
    list1 = os.listdir(f_cpu_gpu)
    _ = list1[0].split('-')
    label_before = _[0]
    
    dataset = np.empty(shape=(0, 16 * feature_n))
    label = []
    for i in range(len(file_label)):
        temp_file_name = f'{label_before}-{file_label[i]}'
        if temp_file_name not in list1:
            continue
       
        path = os.path.join(f_cpu_gpu, temp_file_name)
        fs = os.listdir(path)
        feature_cpu_gpu = np.empty(shape=(0, 16 * feature_n))
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path,  fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)
            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu_gpu = np.concatenate((feature_cpu_gpu, feature), axis=0)
        print(f'name: {file_label[i]}; counet: {feature_cpu_gpu.shape[0]}; label: {i}')
        count = feature_cpu_gpu.shape[0]
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[i]]
    label = np.array(label)
    last_data = np.hstack((label, dataset))
    s = []
    for i in range(size):
        for j in range(feature_n):
            s.append(str(i) + feature_list[j])
    # s = s + s
    head = ['label'] + s
    df = pd.DataFrame(data=last_data)
    df.columns = head
    df.to_csv(save_path, index=False)
    return 


def mergeCSV(file_list, save_file):
    data = ''
    for j in range(len(file_list)):
        if j == 0:
            data = pd.read_csv(file_list[j])
        else:
            data = pd.concat([data, pd.read_csv(file_list[j])], axis=0)
    data.to_csv(save_file, index=False)
    return


def getCsv_p(file_label, f, length, save_path, size, feature_list, size_max=128):
    feature_n = len(feature_list)
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
        # print(cpu_temp_file_name)
        # print(gpu_temp_file_name)
        # print(cpu_list1)
        if cpu_temp_file_name not in cpu_list1 or gpu_temp_file_name not in gpu_list1:
            print("label error")
            exit()
        
        path = os.path.join(f_cpu, cpu_temp_file_name)
        fs = os.listdir(path)
        # fs.sort(key=lambda x: int(x[0:-4]))
        # fs = fs[0: size_max]
        feature_cpu = np.empty(shape=(0, 16 * feature_n))
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path,  fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu = np.concatenate((feature_cpu, feature), axis=0)

        feature_gpu = np.empty(shape=(0, 16 * feature_n))
        path = os.path.join(f_gpu, gpu_temp_file_name)
        fs = os.listdir(path)
        # fs.sort(key=lambda x: int(x[0:-4]))
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length:, j])))
                feature = np.expand_dims(feature, 0)
                feature_gpu = np.concatenate((feature_gpu, feature), axis=0)

        count = min(feature_cpu.shape[0], feature_gpu.shape[0])
        feature_cpu_gpu = np.hstack((feature_cpu[:count, :], feature_gpu[:count, :]))
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[i]]
        print(f"{file_label[i]}  count: {count} label: {i}")
    label = np.array(label)
    # print(label.shape)
    # print(dataset.shape)
    last_data = np.hstack((label, dataset))
    s = []
    for i in range(size):
        for j in range(feature_n):
            s.append(str(i) + feature_list[j])
    s = s + s
    head = ['label'] + s
    df = pd.DataFrame(data=last_data)
    df.columns = head
    df.to_csv(save_path, index=False)
    return file_label



def get_csv_multi(file_label, f, length, save_path, size, feature_list, size_max=128):
    feature_n = len(feature_list)
    f_cpu = os.path.join(f, 'cpu')
    f_gpu = os.path.join(f, 'gpu')
    cpu_list1 = os.listdir(f_cpu)
    _ = cpu_list1[0].index('-')
    cpu_list2 = [s[_ + 1:] for s in cpu_list1]
    gpu_list1 = os.listdir(f_gpu)
    name_label = -1
    dataset = np.empty(shape=(0, 16 * feature_n * 2))
    label = []
    for i in range(len(cpu_list1)):
        l1 = cpu_list1[i].split("-")[1]
        if l1 not in file_label:
            continue
        name_label += 1
        # l1 = cpu_list1[i][temp1 + 1:temp2]
        # l2 = cpu_list1[i][temp2 + 1:]
        path = os.path.join(f_cpu, cpu_list1[i])
        fs = os.listdir(path)
        feature_cpu = np.empty(shape=(0, 16 * feature_n))
        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length, j])))

                feature = np.expand_dims(feature, 0)
                feature_cpu = np.concatenate((feature_cpu, feature), axis=0)

        feature_gpu = np.empty(shape=(0, 16 * feature_n))
        path = os.path.join(f_gpu, gpu_list1[i])
        fs = os.listdir(path)

        for k in range(len(fs)):
            if k >= size_max:
                break
            csv_f = os.path.join(path, fs[k])
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)

            for x in range(data.shape[0] // length):
                feature = np.empty(shape=0)
                for j in range(data.shape[1]):
                    feature = np.concatenate((feature, getFeature(data[x * length:(x + 1) * length:, j])))
                feature = np.expand_dims(feature, 0)
                feature_gpu = np.concatenate((feature_gpu, feature), axis=0)

        count = min(feature_cpu.shape[0], feature_gpu.shape[0])
        feature_cpu_gpu = np.hstack((feature_cpu[:count, :], feature_gpu[:count, :]))
        dataset = np.vstack([dataset, feature_cpu_gpu])
        label += count * [[file_label.index(l1)]]

    label = np.array(label)
    last_data = np.hstack((label, dataset))
    s = []
    for i in range(size):
        for j in range(feature_n):
            s.append(str(i) + feature_list[j])
    s = s + s
    head = ['label'] + s
    df = pd.DataFrame(data=last_data)
    df.columns = head
    df.to_csv(save_path, index=False)
    return cpu_list2