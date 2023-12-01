# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:24:36 2023

@author: Ramon
"""

from reedsolo import RSCodec, ReedSolomonError
import numpy as np

ERASURE_PROBABILITY = 0.1
INFO_LENGTH = 4
EEC_LENGTH = 8
CHUNKS_LENGTH = INFO_LENGTH + EEC_LENGTH

codec = RSCodec(EEC_LENGTH)
trans_msg = b'Test message for laser comms 2023'
trans_msg = list(trans_msg)

msg_chunks = []
for i in range(0, len(trans_msg), INFO_LENGTH):
    msg_chunks.append(trans_msg[i:i+INFO_LENGTH])

encoded_msg = []
for chunk in msg_chunks:
    encoded_msg += codec.encode(chunk)



# ============== SIMULATE TRANSMISSION ERRORS ================

for i  in range(len(encoded_msg)):
    if np.random.rand() < ERASURE_PROBABILITY:
        encoded_msg[i] = 256
