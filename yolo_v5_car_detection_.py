# -*- coding: utf-8 -*-
"""YOLO V5 CAR DETECTION .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rmCnX5AQAlPaklz6bKljpy50Ap7w3R3W
"""

!pip install opencv-python==4.8.1.78
!pip install torch==2.1.0
!pip install matplotlib==3.8.0
!pip install ultralytics==8.0.203
!pip install pandas==2.1.2
!pip install requests==2.31.0

import cv2
from google.colab.patches import cv2_imshow
import torch

VIDEO_PATH="/content/traffic.mp4"
HUB="ultralytics/yolov5"
YOLO="yolov5n"

def count_cars(cap: cv2.VideoCapture):

    model = torch.hub.load(HUB, model=YOLO, pretrained=True)

    while cap.isOpened():
        status, frame = cap.read()

        if not status:
            break

        # Detection filtering and heuristic
        # will be implemented here.

        cv2_imshow(frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
             break

    cap.release()


if __name__ == '__main__':
    cap = cv2.VideoCapture(VIDEO_PATH)
    count_cars(cap)

import pandas as pd

def get_bboxes(preds: object):
    df = preds.pandas().xyxy[0]
    df = df[df["confidence"] >= 0.5]
    df = df[df["name"].isin(["car", "bus", "truck"])]

    return df[["xmin", "ymin", "xmax", "ymax"]].values.astype(int)

def get_center(bbox):
    center = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)
    return center

import cv2
import numpy as np
import matplotlib.path as mplPath

POLYGON = np.array([
    [333, 374],
    [403, 470],
    [476, 655],
    [498, 710],
    [1237, 714],
    [1217, 523],
    [1139, 469],
    [1009, 393],
])
def is_valid_detection(xc, yc):
    return mplPath.Path(POLYGON).contains_point((xc, yc))

def count_cars(cap: object):

    model = torch.hub.load(HUB, model=YOLO, pretrained=True)

    while cap.isOpened():
        status, frame = cap.read()

        if not status:
            break

        preds = model(frame)
        bboxes = get_bboxes(preds)

        detections = 0
        for box in bboxes:
            xc, yc = get_center(box)

            if is_valid_detection(xc, yc):
                detections += 1

            # Draw poit of reference for each detection
            cv2.circle(img=frame, center=(xc, yc), radius=5, color=(0,255,0), thickness=-1)
            # Draw bounding boxes for each detection
            cv2.rectangle(img=frame, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(255, 0, 0), thickness=1)
        # Draw the counter
        cv2.putText(img=frame, text=f"Cars: {detections}", org=(100, 100), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(0,0,0), thickness=3)
        # Draw the polygon
        cv2.polylines(img=frame, pts=[POLYGON], isClosed=True, color=(0,0,255), thickness=4)
        # Display frame
        cv2.imshow("frame", frame)