'''
This Python script takes as input the PPM timestamps read from Arduino and decodes them to obtain
a readable message. To do this, it first identifies the synchronization pattern to know when each
transmission begins and ends. After this, it takes the remainder of the timepulses and finds the
corresponding ASCII values, which later transforms to readable characters. Finally, it prints the
full message.
In order to log serial data from the Arduino console into a .txt file, I have been using the CoolTerm
software, which automatically records the data printed on Arduino.
'''

import numpy as np

# Define the same parameters of the durations of the PPM slots and the entire frame or period
PPM_PULSE_WIDTH = 1
PERIOD = 256
FILE_LOCATION = "" # Write here the location of the .txt file in your computer

file = open(FILE_LOCATION, "r") #  Open the .txt file
text = file.readlines() # Create a list where the elements are each of the lines from the file in string form
times = [int(float(element)) for element in text] # Convert each entry to an integer

differences = []
for i in range(len(times) - 1):
        # Add the differences between each pair of consecutive timestamps to this list
        differences.append(times[i+1] - times[i])


# Now we want to identify the syncronization pattern, which consists of 5 consists of 5 consecuitve pulses
# in the first PPM slot of each frame, i.e., the slot corresponding to 0 in ASCII. Thus, we are looking for 
# 4 consecutive values of the duration of the period or frame (256 in this case) in the 'differences' list.
frames_start_indices = [] # Create list for the indices where each transmission begins
for i in range(len(differences)):
    if ((differences[i] == PERIOD) and (differences[i+1] == PERIOD) and
        (differences[i+2] == PERIOD) and (differences[i+3] == PERIOD)):
        frames_start_indices.append(i) # Append indices to list

# Now we take all timestamps between the first and second values of the previously created indices list.
# This is because each transmission contains the same message, so we just select the timestamps in between
# any two consecutive indices of the list.         
frame_times = np.array(times[frames_start_indices[0]: frames_start_indices[1]])
frame_times -= frame_times[0] # Substract the timestamp of the beginning so that the timestamps start at 0
for i in range(len(frame_times)):
    frame_times[i] -= PERIOD*i # Subtract a multiple of the period to make all values range between 0 and 255 (ASCII values)
    
message = ''
for ASCII_val in frame_times[5:]:
    message += chr(ASCII_val) # Transform ASCII values to characters and append them on the message string
    
print(message) # Print final message