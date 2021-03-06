import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
from PIL import Image

HOST=''
PORT=1080

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        # print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]

    msg_size = struct.unpack(">L", packed_msg_size)[0]
    # print(msg_size)
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

    im = Image.frombytes('RGB', (320, 240), frame, "raw", "BGR")

    cv_arr = np.asarray(im)
    # print(cv_arr)
    cv2.imshow('ImageWindow', cv_arr)
    cv2.waitKey(1)