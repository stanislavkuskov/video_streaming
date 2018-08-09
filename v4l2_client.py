import cv2
import io
import socket
import struct
import time
import pickle
import zlib
from PyV4L2Camera.camera import Camera
from PIL import Image
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.100', 1080))
# connection = client_socket.makefile('wb')

camera = Camera('/dev/video0', 320, 240)
img_size = [240, 320, 3]


img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    frame = camera.get_frame()
    # print(frame)
    # Decode the image
    # im = Image.frombytes('RGB', (camera.width, camera.height), frame, "raw", "BGR")
    # print(im)
    # Convert the image to a numpy array
    # cv_arr = np.asarray(im)
    #
    # resized = cv2.resize(cv_arr.copy(), (img_size[1], img_size[0]))
    #
    # result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
#     data = pickle.dumps(frame, 0)
    data = pickle.dumps(frame, 0)
    size = len(data)

    # print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()