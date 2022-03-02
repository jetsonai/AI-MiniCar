# kate.brighteyes@gmail.com
# 20210720

#gst_str = ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)224, height=(int)224, format=(string)NV12, framerate=(fraction)60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)224, height=(int)224, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
gst_str = ("v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, format=(string)YUY2,framerate=30/1 ! videoconvert ! video/x-raw,width=640,height=480,format=BGR ! appsink")

import cv2
import numpy as np
import datetime
import time
import os
from uuid import uuid1
import sys

blocked_dir = 'dataset/blocked'
free_dir = 'dataset/free'
free_count = 0	
blocked_count = 0

bExit = 0

save_block=0 # 0: free, 1:block

def filename_free():
    global free_dir, free_count
    free_count= len(os.listdir(free_dir))
    image_path = os.path.join(free_dir, str(uuid1()) + '.jpg')
    return image_path
    
def filename_blocked():
    global blocked_dir, blocked_count
    blocked_count= len(os.listdir(blocked_dir))
    image_path = os.path.join(blocked_dir, str(uuid1()) + '.jpg')
    return image_path

def imageCopy(src):
    return np.copy(src)

def videoProcess(openpath):
    
    cap = cv2.VideoCapture(openpath)
    if cap.isOpened():
        print("Video Opened")
    else:
        print("Video Not Opened")
        print("Program Abort")
        exit()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

    cv2.namedWindow("Input", cv2.WINDOW_GUI_EXPANDED)
    print(save_block)
    if save_block == '1':
        print("push s button to save blocked image.")
    else:
        print("push s button to save free image.")

    try:
        while cap.isOpened() and bExit == 0:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:
                #frame = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_AREA)
                cv2.imshow("Input", frame)
            else:
                break
    
            if cv2.waitKey(int(1000.0/fps)) & 0xFF == ord('s'):
                if save_block == '1':
                    filename = filename_blocked()
                else:
                    filename = filename_free()

                print(filename)
                cv2.imwrite(filename, frame)
    
    except KeyboardInterrupt:  
        print("key int")
        cap.release()
        cv2.destroyAllWindows()
        time.sleep(0.5)
        return
	
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return
   
if __name__=="__main__":

    save_block = sys.argv[1]


    try:
        os.makedirs(free_dir)
        os.makedirs(blocked_dir)
    except FileExistsError:
        print('Directories not created becasue they already exist')

    videoProcess(gst_str)
