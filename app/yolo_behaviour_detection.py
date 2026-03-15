from numpy import ndarray
from ultralytics import YOLO
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# model =YOLO(os.path.join(script_dir, 'best1.pt'))
model =YOLO(os.path.join(script_dir, 'behavior.pt'))



def detect_behaviour(
    img: ndarray,
    conf: float = 0.05,
    iou: float = 0.1
) -> str:
    return model(source=img, stream=True, conf=conf, iou=iou)
