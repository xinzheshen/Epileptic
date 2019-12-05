import os
import re

import pyedflib
import torch
import numpy as np
import matplotlib.pyplot as plt


base_path = r"D:\personal\dataset\epilepsy"
IDs = ['01', '03', '07', '09', '10', '20', '21', '23']
chb = "chb"
MD5SUMS = "MD5SUMS"
summary_txt = "-summary.txt"
edf = ".edf"

file_name_compile = re.compile(r'^File Name: (.*)')
file_start_time_compile = re.compile(r'^File Start Time: (.*)')
file_end_time_compile = re.compile(r'^File End Time: (.*)')
num_seizure_compile = re.compile(r'Number of Seizures in File: (.*)')
seizure_start_time_compile = re.compile(r'^Seizure Start Time: (.*) seconds')
seizure_end_time_compile = re.compile(r'^Seizure End Time: (.*) seconds')

def read_md5(id):
    file_name = os.path.join(base_path, chb + id, MD5SUMS)
    files = []
    with open(file_name) as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                texts = line.split()
                if texts[1].endswith(edf):
                    files.append(texts[1])

    return files


def read_summary(id):
    dir_name = chb + id
    file_name_summary = os.path.join(base_path, dir_name, dir_name + summary_txt)
    file_info_dict = {}
    with open(file_name_summary) as f:
        for line in f.readlines():
            line = line.strip()
            result = re.match(file_name_compile, line)
            if result:
                file_name = result.group(1)
                file_info_dict[file_name] = []
                continue

            result = re.match(file_start_time_compile, line)
            if result:
                file_info_dict[file_name].append(result.group(1))
                continue

            result = re.match(file_end_time_compile, line)
            if result:
                file_info_dict[file_name].append(result.group(1))
                continue

            result = re.match(num_seizure_compile, line)
            if result:
                file_info_dict[file_name].append(result.group(1))
                continue

            result = re.match(seizure_start_time_compile, line)
            if result:
                file_info_dict[file_name].append(result.group(1))
                continue

            result = re.match(seizure_end_time_compile, line)
            if result:
                file_info_dict[file_name].append(result.group(1))
                continue
    return file_info_dict





def read_edf():
    f = pyedflib.EdfReader(r"D:\personal\dataset\epilepsy\chb01\chb01_04.edf")
    f1 = pyedflib.EdfReader(r"D:\personal\dataset\epilepsy\chb01\chb01_01.edf")
    n = f.signals_in_file
    print("signal numbers:", n)
    signal_labels = f.getSignalLabels()
    print("Labels:", signal_labels)
    signal_headers = f.getSignalHeaders()
    print("Headers:", signal_headers)

    signal_datas = f.readSignal(0)
    # signal_datas_torch = torch.from_numpy(signal_datas)
    # torch.save(signal_datas_torch, 'chb01_01.pt')
    # signal_datas_torch2 = torch.load("chb01_01.pt")


def process_data(id):
    # files = read_md5(id)
    files_info = read_summary(id)
    print('end')


def main():
    for id in IDs:
        process_data(id)


if __name__ == '__main__':
    main()

