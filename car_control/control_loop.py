import cv2
from jetson.utils import videoSource, videoOutput, cudaToNumpy, cudaDeviceSynchronize


from time import perf_counter, sleep

from serial_car_control import SerialController
sc = SerialController("/dev/ttyUSB0", 9600, 0.1, 100)
camera = videoSource("csi://0")
cudaDeviceSynchronize()

while True:

    img = camera.Capture()
    array = cudaToNumpy(img)


    # Detect the lane (hints are in Day2/Morning-Session-1/lane_detection.ipynb)

    # then use sc control methods to drive.

    if no_lane:
        sc.stop()
# make sure you account for no lane and properly stop the car via 

sc.stop()