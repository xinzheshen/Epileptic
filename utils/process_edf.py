import os
import re
import time

import pyedflib
import torch
import numpy as np
import matplotlib.pyplot as plt


base_path = r"D:\personal\dataset\epilepsy"
IDs = ['01', '03', '07', '09', '10', '20', '21', '22']
IDs = ['22']
chb = "chb"
MD5SUMS = "MD5SUMS"
summary_txt = "-summary.txt"
edf = ".edf"

file_name_compile = re.compile(r'^File Name: (.*)')
file_start_time_compile = re.compile(r'^File Start Time: (.*)')
file_end_time_compile = re.compile(r'^File End Time: (.*)')
num_seizure_compile = re.compile(r'Number of Seizures in File: (.*)')
seizure_start_time_compile = re.compile(r'^Seizure \d?\s?Start Time: (.*) seconds')
seizure_end_time_compile = re.compile(r'^Seizure \d?\s?End Time: (.*) seconds')

preictal_start = 65 * 60
preictal_end = 5 * 60
interictal_interval = 4 * 60 * 60

sample_rate = 256
sample_duration = 5

def read_md5(id):
    file_name = os.path.join(base_path, chb + id, MD5SUMS)
    files = []
    with open(file_name) as f:
        for line in f:
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
        for line in f:
            line = line.strip()
            result = re.match(file_name_compile, line)
            if result:
                file_name = result.group(1)
                file_info_dict[file_name] = []
                continue

            result = re.match(file_start_time_compile, line)
            if result:
                time_str = re.sub("^24", "00", result.group(1))
                file_info_dict[file_name].append(time_str)
                continue

            result = re.match(file_end_time_compile, line)
            if result:
                time_str = re.sub("^24", "00", result.group(1))
                file_info_dict[file_name].append(time_str)
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


def get_edf_date(id, file_name):
    file_name = os.path.join(base_path, chb + id, file_name)
    f = pyedflib.EdfReader(file_name)
    n = f.signals_in_file
    assert f.signals_in_file == 23

    y = f.startdate_year
    m = f.startdate_month
    d = f.startdate_day

    signal_datas = f.readSignal(0)
    return str(y) + "-" + str(m) + "-" + str(d)
    # signal_datas_torch = torch.from_numpy(signal_datas)
    # torch.save(signal_datas_torch, 'chb01_01.pt')
    # signal_datas_torch2 = torch.load("chb01_01.pt")


def cal_duration(id, files_info):
    files_info_with_timestamp = {}
    last_file_name = ""
    for file_name, info in files_info.items():
        files_info_with_timestamp[file_name] = [0, 0, 0, -1]
        date = get_edf_date(id, file_name)
        file_start_timestamp = int(time.mktime(time.strptime(date + " " + info[0], "%Y-%m-%d %H:%M:%S")))
        files_info_with_timestamp[file_name][0] = file_start_timestamp
        file_end_timestamp = int(time.mktime(time.strptime(date + " " + info[1], "%Y-%m-%d %H:%M:%S")))
        files_info_with_timestamp[file_name][1] = file_end_timestamp

        if int(info[2]) > 0:
            print(id, file_name, info)
            preictal_start_timestamp = file_start_timestamp + int(info[3]) - preictal_start
            preictal_end_timestamp = file_start_timestamp + int(info[3]) - preictal_end

            # 这里默认preictal开始时间最早为上一个文件的起始时间，即使前者比后者更早，也不去继续往前追加了，
            # 因为一个文件时长最少为一小时，误差最多五分钟
            if preictal_start_timestamp > file_start_timestamp:
                files_info_with_timestamp[file_name][2] = preictal_end_timestamp
            elif last_file_name and files_info[last_file_name][2] == 0:
                files_info_with_timestamp[last_file_name][2] = preictal_end_timestamp

            if preictal_end_timestamp > file_start_timestamp:
                files_info_with_timestamp[file_name][3] = preictal_end_timestamp
            elif last_file_name and files_info[last_file_name][2] == 0:
                files_info_with_timestamp[last_file_name][3] = preictal_end_timestamp

            # if preictal_start_timestamp
            # files_info_with_timestamp[file_name][3] = preictal_end_timestamp

    return files_info_with_timestamp


def process_data(id):
    # files = read_md5(id)
    files_info = read_summary(id)
    cal_duration(id, files_info)


def main():
    for id in IDs:
        process_data(id)


if __name__ == '__main__':
    main()

