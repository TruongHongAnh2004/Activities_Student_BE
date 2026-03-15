from numpy import ndarray
from ultralytics import YOLO
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

model =YOLO(os.path.join(script_dir, 'face.pt'))



def detect_face(
    img: ndarray,
    conf: float = 0.05,
    iou: float = 0.1
) -> str:
    return model(source=img, stream=True, conf=conf, iou=iou)