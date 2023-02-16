import torch

def initialize_yolo():
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=False)

    model.iou = 0.45
    model.classes = [0, 2, 7, 30]
    model.multi_label = False
    model.max_det = 1000

    return model