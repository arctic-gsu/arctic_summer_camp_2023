from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
import cv2
import sys
import os
import numpy as np
vcap = cv2.VideoCapture("rtsp://10.51.225.51:8554/output")
home_dir=os.path.expanduser('~')+ '/Capture_Imeges/'
os.makedirs(home_dir)
i=1
j=1
while(True):
    i = i+1
    #img = camera.Capture()
    ret, frame = vcap.read()
    frame=cv2.flip(frame,0)
    img = np.float32(frame)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_n = cv2.normalize(src=img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow("output", img_n)
    key = cv2.waitKey(1)
    if (i==1000):
        j=j+1
        path = f'Frame_{str(j)}.jpg'
        #print(path)
        cv2.imwrite(os.path.join(home_dir ,path), img_n)
        i=0
    if key == 27:#if ESC is pressed, exit loop
        cv2.destroyAllWindows()
        break
