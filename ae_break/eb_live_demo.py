# kate.brighteyes@gmail.com
# 20210720

gst_str = ("v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, format=(string)YUY2,framerate=30/1 ! videoconvert ! video/x-raw,width=640,height=480,format=BGR ! appsink")

#gst_str = ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)224, height=(int)224, format=(string)NV12, framerate=(fraction)60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)224, height=(int)224, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

import cv2
import numpy as np
from motor.MotorDriver import MotorDriver

import torch
import torchvision

import torch.nn.functional as F
import time

mean = 255.0 * np.array([0.485, 0.456, 0.406])
stdev = 255.0 * np.array([0.229, 0.224, 0.225])

normalize = torchvision.transforms.Normalize(mean, stdev)

def preprocess(camera_value):
    global device, normalize
    x = camera_value
    x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    x = x.transpose((2, 0, 1))
    x = torch.from_numpy(x).float()
    x = normalize(x)
    x = x.to(device)
    x = x[None, ...]
    return x

def imageProcessing(frame):
    x = preprocess(frame)
    y = model(x)
    
    # we apply the `softmax` function to normalize the output vector so it sums to 1 (which makes it a probability distribution)
    y = F.softmax(y, dim=1)
    
    prob_blocked = float(y.flatten()[0])
    #print('prob_blocked')

    if prob_blocked < 0.5:
        Motor.MotorRun(0, 'forward', 0.5)
        Motor.MotorRun(1, 'forward', 0.5)
    else :
        Motor.AllMotorStop()

    return

def videoProcess(openpath, savepath = None):
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
    #fourcc = cv2.VideoWriter_fourcc('m','p','4','v') with *.mp4 save
    cv2.namedWindow("Output", cv2.WINDOW_GUI_EXPANDED)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Our operations on the frame come here
                #frame = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_AREA) 
                imageProcessing(frame)
                cv2.imshow("Output", frame)
            else:
                break

            if cv2.waitKey(int(1000.0/fps)) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:  
        print("key int")
        all_stop()
        cap.release()
        cv2.destroyAllWindows()
        return
    # When everything done, release the capture
    Motor.AllMotorStop()
    cap.release()

    cv2.destroyAllWindows()
    return
   
model = torchvision.models.alexnet(pretrained=False)
model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, 2)
print("alexnet")
model.load_state_dict(torch.load('best_model.pth'))
print("best_model.pth")
device = torch.device('cuda')
model = model.to(device)

Motor = MotorDriver()
print("PCA9685 MotorDriver")

videoProcess(gst_str)

