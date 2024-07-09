import os
import pandas as pd
import numpy as np
import torch


def get_tensor(file_label, f, size, dataset_path, label_path):

    gpu_np = np.empty(shape=0)
    cpu_np = np.empty(shape=0)

    f_cpu = os.path.join(f, 'cpu')
    f_gpu = os.path.join(f, 'gpu')
    
    cpu_list1 = os.listdir(f_cpu)
    _ = cpu_list1[0].split('-')
    cpu_label_before = _[0]
    
    gpu_list1 = os.listdir(f_gpu)
    _ = gpu_list1[0].split('-')
    gpu_label_before = _[0]
    
    label = []
    dataset = np.empty(shape=(0, 2, size * 2, size * 2))
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
        data_cpu = np.empty(shape=(0, size*2, size*2))
        for f in fs:
            csv_f = os.path.join(path, f)
            data = pd.read_csv(csv_f, header=None)

            data = np.array(data)
            data = np.log(data)

            cpu_np = np.concatenate([cpu_np, data.reshape(data.shape[0] * data.shape[1], )])
            data1 = data[range(0, size * 2), :].transpose()
            data2 = data[range(size * 2, size * 4), :].transpose()
            data = np.vstack((data1, data2))
            data = np.expand_dims(data, 0)
            data_cpu = np.vstack([data_cpu, data])
        data_gpu = np.empty(shape=(0, size*2, size*2))
       
        path = os.path.join(f_gpu, gpu_temp_file_name)
        fs = os.listdir(path)
        for f in fs:
            csv_f = os.path.join(path, f)
            data = pd.read_csv(csv_f, header=None)
            data = np.array(data)
            data = np.log(data)
            gpu_np = np.concatenate([gpu_np, data.reshape(data.shape[0] * data.shape[1], )])
            data1 = data[range(0, size * 2), :].transpose()
            data2 = data[range(size * 2, size * 4), :].transpose()
            data = np.vstack((data1, data2))
            data = np.expand_dims(data, 0)
            data_gpu = np.vstack([data_gpu, data])
        print(len(data_cpu), len(data_gpu))
        
        count = min(len(data_cpu), len(data_gpu))
        for j in range(count):
            d_cpu = np.expand_dims(data_cpu[j], 0)
            d_gpu = np.expand_dims(data_gpu[j], 0)
            data = np.concatenate((d_cpu, d_gpu), axis=0)
            data = np.expand_dims(data, 0)
            dataset = np.concatenate((dataset, data), axis=0)
        label += count * [i]
        print(f"{file_label[i]}  count: {count} label: {i}")
    label = np.array(label)
    label = torch.tensor(label).long()
    dataset = torch.tensor(dataset)
   
    torch.save(dataset, dataset_path)
    torch.save(label, label_path)

    return file_label



def get_tensor_choose(file_label, f, size, dataset_path, label_path, choose):

    cpu_np = np.empty(shape=0)

    f_cpu = os.path.join(f, choose)
    
    cpu_list1 = os.listdir(f_cpu)
    _ = cpu_list1[0].split('-')
    cpu_label_before = _[0]
  
    label = []
    dataset = np.empty(shape=(0, 1, size * 2, size * 2))
    for i in range(len(file_label)):
        
        cpu_temp_file_name = f'{cpu_label_before}-{file_label[i]}'
       
        if cpu_temp_file_name not in cpu_list1 :
            print("label error")
            exit()
        
        path = os.path.join(f_cpu, cpu_temp_file_name)
        fs = os.listdir(path)
        data_cpu = np.empty(shape=(0, size*2, size*2))
        for f in fs:
            csv_f = os.path.join(path, f)
            data = pd.read_csv(csv_f, header=None)

            data = np.array(data)
            data = np.log(data)

            cpu_np = np.concatenate([cpu_np, data.reshape(data.shape[0] * data.shape[1], )])
            data1 = data[range(0, size * 2), :].transpose()
            data2 = data[range(size * 2, size * 4), :].transpose()
            data = np.vstack((data1, data2))
            data = np.expand_dims(data, 0)
            data_cpu = np.vstack([data_cpu, data])
        
        count = len(data_cpu)
        for j in range(count):
            d_cpu = np.expand_dims(data_cpu[j], 0)
            # print(d_cpu.shape)
          
            dataset = np.concatenate((dataset, np.expand_dims(d_cpu, 0)), axis=0)
        label += count * [i]
        print(f"{file_label[i]}  count: {count} label: {i}")
    label = np.array(label)
    label = torch.tensor(label).long()
    dataset = torch.tensor(dataset)
   
    torch.save(dataset, dataset_path)
    torch.save(label, label_path)

    return file_label
