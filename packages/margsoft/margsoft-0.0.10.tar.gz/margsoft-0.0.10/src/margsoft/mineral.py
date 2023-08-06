import cv2
import time
import numpy as np
import os
import pathlib
from datetime import datetime
import sys
CONFIDENCE_THRESHOLD = 0.7
NMS_THRESHOLD = 0.1
def collectdataset(rtsp,names_file,weight_file,cfg_file,path,dir_n,x_1,y_1,w_1,z_1):
    print("inside the function")
    cap = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)
    prevTime = 0
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #cv2.namedWindow("output", cv2.WINDOW_NORMAL)    
    class_names = []
    with open(names_file, "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]

        
    # frame_width = int(cap.get(3))
    # frame_height = int(cap.get(4))
    # size = (frame_width, frame_height)
    #colors = np.random.uniform(0,255,size=(len(class_names),3))
    net = cv2.dnn.readNet(weight_file,cfg_file)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(640, 640), scale=1/255, swapRB=True)
    pathlib.Path(path+str(dir_n)).mkdir(parents=True, exist_ok=True)
    print("Is rtsp stream opend :",cap.isOpened())
    try:
        while cap.isOpened(): 
            ret, frame = cap.read()
            frame_crop=frame[y_1:z_1,x_1:w_1]
            frame_crop= np.array(frame_crop)
            frame=cv2.resize(frame, (720, 720))
            frame = np.array(frame)
            classes, scores, boxes = model.detect(frame_crop, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
            for (classid, score, box) in zip(classes, scores, boxes):
                if(class_names[classid] not in ["other"]):
                    print(class_names[classid],score)
                    print("found!!!")
                    curr_datetime = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                    f_name = path+dir_n+"/"+str(curr_datetime)+".jpg"
                    cv2.imwrite(f_name, frame)
                    print(f_name)
    except KeyboardInterrupt:
        print("Bye")
        sys.exit()
