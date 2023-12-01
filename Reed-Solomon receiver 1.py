# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:58:20 2023

@author: Ramon
"""

from reedsolo import RSCodec, ReedSolomonError
import numpy as np

INFO_LENGTH = 4
EEC_LENGTH = 8
CHUNKS_LENGTH = INFO_LENGTH + EEC_LENGTH

PPM_PULSE_WIDTH = 1
PERIOD = 256
FILE_LOCATION = "C:\\Users\Ramon\Documents\Study Abroad\Verano\Reseach\PPM_times.txt"

codec = RSCodec(EEC_LENGTH)

file = open(FILE_LOCATION, "r") #  Open the .txt file
text = file.readlines() # Create a list where the elements are each of the lines from the file in string form
times = [int(float(element)) for element in text] # Convert each entry to an integer

differences = []
for i in range(len(times) - 1):
        # Add the differences between each pair of consecutive timestamps to this list
        differences.append(times[i+1] - times[i])


frames_start_indices = [] # Create list for the indices where each transmission begins
for i in range(len(differences) - 4):
    if ((differences[i] == PERIOD) and (differences[i+1] == PERIOD) and
        (differences[i+2] == PERIOD) and (differences[i+3] == PERIOD)):
        frames_start_indices.append(i) # Append indices to list

frame_differences = np.array(differences[frames_start_indices[0]: frames_start_indices[1]])    
frame_times = np.array(times[frames_start_indices[0]: frames_start_indices[1]])
frame_times -= frame_times[0] # Substract the timestamp of the beginning so that the timestamps start at 0
for i in range(len(frame_times)):
    frame_times[i] -= PERIOD*i # Subtract a multiple of the period to make all values range between 0 and 255 (ASCII values)

for i in range(len(frame_times) + 100):
    indices_displaced = 0
    try:
        while frame_times[i + indices_displaced] >= PERIOD:
            frame_times[i + indices_displaced:] -= PERIOD
            frame_times = np.insert(frame_times, i, 88)
            indices_displaced += 1
    except IndexError:
        break

# =============== NEW STUFF ============    

rec_msg = frame_times[5:]

rec_msg_chunks = []
for i in range(0, len(rec_msg), CHUNKS_LENGTH):
    rec_msg_chunks.append(rec_msg[i:i+CHUNKS_LENGTH])

decoded_msg = []
for chunk in rec_msg_chunks:
    if np.any(chunk == 88):
        chunk = list(chunk)
        erasures_indices = [index for index, value in enumerate(chunk) if value == 88]
        decoded_chunk = codec.decode(chunk, erase_pos=erasures_indices)[0]
        # decoded_chunk = codec.decode(chunk)[0]
    else:
        decoded_chunk = list(chunk[0:INFO_LENGTH])
    
    if len(chunk) == CHUNKS_LENGTH:
        decoded_msg += decoded_chunk
    else:
        decoded_msg += decoded_chunk[:CHUNKS_LENGTH - len(chunk)]

message = ''
for ASCII_val in decoded_msg:
    message += chr(ASCII_val) # Transform ASCII values to characters and append them on the message string
    
print(message) # Print final message
