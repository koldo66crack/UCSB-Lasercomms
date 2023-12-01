# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 13:23:37 2023

@author: Ramon
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

FILE_LOCATION = 'C:\\Users\Ramon\Documents\Study Abroad\Verano\Reseach\Reed-Solomon final\Reed-Solomon simulation 3 data - BER.csv'
BACKGROUND_RATE = 0.0001

def read_file():
    with open(FILE_LOCATION, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_counter = 0
        for row in csv_reader:
            # print(row)
            if line_counter == 0:
                columns = row
                df = pd.DataFrame(columns=columns)
            else:
                row = [float(element) for element in row]
                df.loc[len(df)] = row
            line_counter += 1
    df.sort_values('Symbol erasure rate', inplace=True)
    return df

def plot(background_rate):
    data = read_file()
    data.sort_values(by='Background rate', inplace=True)
    data.reset_index(drop=True, inplace=True)
    indices = np.argwhere(np.array(data['Background rate']) == background_rate).reshape(-1)
    BER_array = data['Bit error rate'][indices]
    error_rate = data['Symbol erasure rate'][indices]
    SBR_array = (1 - error_rate) / background_rate

    plt.scatter(SBR_array, 100*BER_array)
    plt.xlabel('Signal to Background Ratio')
    plt.ylabel('Bit error rate (%)')
    plt.title('RS simulation for code rate of 0.2 and background rate of {}'.format(background_rate))
    plt.savefig('RS simulation 3 plot {} background rate - BER.png'.format(background_rate), dpi=1000)
    plt.show()

plot(BACKGROUND_RATE)