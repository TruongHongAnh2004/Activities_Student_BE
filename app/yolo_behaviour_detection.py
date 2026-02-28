from ultralytics import YOLO
import cv2
import math
import datetime
import os
import torch

script_dir = os.path.dirname(os.path.abspath(__file__))

# model =YOLO(os.path.join(script_dir, 'best1.pt'))
model =YOLO(os.path.join(script_dir, 'best2.pt'))



def detect_behaviour(
    input_image_path: str,
    output_dir: str = "output",
    conf: float = 0.05,
    iou: float = 0.1
) -> str:
    """
    Detect objects and draw bounding boxes on image

    Returns:
        output_image_path (str)
    """

    os.makedirs(output_dir, exist_ok=True)

    # inference
    results = model(input_image_path, stream=True, conf=conf, iou=iou)

    # load image
    img = cv2.imread(input_image_path)

    # draw settings
    text_color = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    text_thickness = 2
    
    behaviour_results = []
    
    for result in results:
        names = [result.names[cls.item()] for cls in result.boxes.cls.int()]
        
        for index, item in enumerate(result.boxes.xyxy):
            x1, y1, x2, y2 = map(int, item)
            behaviour_results.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'name': names[index]})

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img,
                names[index],
                (x1, y1 - 10),
                font,
                font_scale,
                text_color,
                text_thickness
            )

    # save output
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"output_{timestamp}.jpg")
    cv2.imwrite(output_path, img)

    return behaviour_results
