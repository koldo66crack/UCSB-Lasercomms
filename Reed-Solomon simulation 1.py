# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 17:37:25 2023

@author: Ramon
"""

from reedsolo import RSCodec, ReedSolomonError
import numpy as np
import csv

INFO_LENGTH = 4
EEC_LENGTH = 4
ERASURE_RATE = 0.2
FILE_LOCATION = 'C:\\Users\Ramon\Documents\Study Abroad\Verano\Reseach\Reed-Solomon final\Reed-Solomon simulation 1 data.csv'

codec = RSCodec(EEC_LENGTH)

def create_chunk():
    chunk = np.random.randint(0, 256, size=INFO_LENGTH)
    for index in range(len(chunk)):
        symbol = chunk[index]
        while symbol == 88:
            new_symbol = np.random.randint(0, 256)
            chunk[index] = new_symbol
            symbol = new_symbol
    return list(chunk)

def run_simulation():
    error_count = 0
    total_count = 0
    while error_count < 100:
        chunk = create_chunk()
        encoded_msg = codec.encode(chunk)
        erasure_indices = []
        for index in range(len(encoded_msg)):
            if np.random.rand() < ERASURE_RATE:
                encoded_msg[index] = 88
                erasure_indices.append(index)
        try:
            decoded_msg = codec.decode(encoded_msg, erase_pos=erasure_indices)[0]
            if list(chunk) != list(decoded_msg):
                error_count += 1
        except ReedSolomonError:
            error_count += 1
        total_count += 1
    return error_count/total_count

def save_data(new_header=False):
    header = ['Info symbols', 'EEC symbols', 'Symbol erasure rate', 'Message error rate', 'Message error uncertainty']
    data = [INFO_LENGTH, EEC_LENGTH, ERASURE_RATE, message_error_rate, message_error_uncertainty]
    with open(FILE_LOCATION, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        if new_header:
            writer.writerow(header)
        writer.writerow(data)
    return None
            
error_rates = []
for i in range(3):
    error = run_simulation()
    error_rates.append(error)
error_rates = np.array(error_rates)

message_error_rate = np.mean(error_rates)
message_error_uncertainty = np.std(error_rates)

save_data(new_header=True)