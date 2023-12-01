# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 12:32:28 2023

@author: Ramon
"""

from reedsolo import RSCodec, ReedSolomonError
import numpy as np
import csv
import copy

TOTAL_LENGTH = 255
INFO_LENGTH = 51 # Code rate of ~ 0.2
EEC_LENGTH = TOTAL_LENGTH - INFO_LENGTH # 216
BACKGROUND_RATE = 0.01
FILE_LOCATION = 'C:\\Users\Ramon\Documents\Study Abroad\Verano\Reseach\Reed-Solomon final\Reed-Solomon simulation 3 data - first trial.csv'
M_BITS = 8

ER_range = np.linspace(0.72, 0.86, 16)

codec = RSCodec(EEC_LENGTH)

def create_chunk():
    chunk = np.random.randint(0, 256, size=INFO_LENGTH)
    return list(chunk)

def run_simulation(erasure_rate):
    error_count = 0
    total_count = 0
    bit_errors = 0
    while error_count < 100:
        hard_errors = 0
        chunk = create_chunk()
        encoded_msg = codec.encode(chunk)
        encoded_msg_copy = copy.copy(encoded_msg)
        erasure_indices = []
        for index in range(len(encoded_msg)):
            if np.random.rand() < BACKGROUND_RATE:
                encoded_msg[index] = np.random.randint(255)
                hard_errors += 1
            else:
                if np.random.rand() < erasure_rate:
                    encoded_msg[index] = 88
                    erasure_indices.append(index)
        try:
            decoded_msg, decoded_msg_eec, _ = codec.decode(encoded_msg, erase_pos=erasure_indices)
            if list(encoded_msg_copy) != list(decoded_msg_eec):
                error_count += 1
                print(error_count)
        except ReedSolomonError:
            error_count += 1
            print(error_count)
        total_count += 1
    return error_count/total_count

def save_data(erasure_rate, new_header=False):
    message_error_rate = run_simulation(erasure_rate)
    header = ['Info symbols', 'EEC symbols', 'Symbol erasure rate', 'Background rate', 'Message error rate']
    data = [INFO_LENGTH, EEC_LENGTH, erasure_rate, BACKGROUND_RATE, message_error_rate]
    with open(FILE_LOCATION, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        if new_header:
            writer.writerow(header)
        writer.writerow(data)
    return None

for i in ER_range:
    print('Erasure rate:', i)
    save_data(i)