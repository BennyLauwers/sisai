import cv2
import json
import os

from shapely.geometry import Polygon as plg

import utilities.constants as cnst
import utilities.def_get_camera_data as gcd

import inference.ita_object_tracking as tracking

def read_classes_to_detect(camera_id):
    camera_list, _, _, _, zone_points_list, detection_classes_list, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    index_value = camera_list.index(camera_id)
    classes_to_detect = detection_classes_list[index_value]
    zone = zone_points_list[index_value]

    return classes_to_detect,zone


def calculate_iou(box_1, box_2):
    poly_1 = plg(box_1)
    poly_2 = plg(box_2)
    
    iou = False
    
    if poly_1.intersection(poly_2).area > 0.15 * poly_1.area: #15% of the box is in the danger zone 
        iou = True
    
    return iou

def model_inference_and_render(camera_id, model, frame, object_trackers, track_id_histories, alert_amount):
    classes_to_detect, zone = read_classes_to_detect(camera_id)

    results = model(frame)
    
    labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
    x_shape, y_shape = frame.shape[1], frame.shape[0]

    person_detections = []
    car_detections = []
    truck_detections = []
    fire_detections = []

    for i in range(len(labels)):
        label = ""
        row = cord[i]
        if row[4] >= 0.5: #0.5 = detection threshold
            x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
            object_box = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            confidence = row[4]
            bgr_ok = (0, 255, 0)
            bgr_not_ok = (0, 0, 255)
            if labels[i] == 0.0:
                if ("Person" in classes_to_detect):
                    label = "Person"
                    iou = (calculate_iou(object_box, zone[0]))
                    print(f"IOU Person {camera_id}: ", iou)
                    if iou:
                        person_detections.append(([x1, y1, int(x2-x1), int(y2-y1)], row[4].item(), label))

            if labels[i] == 2.0:
                if ("Car" in classes_to_detect):
                    label = "Car"
                    iou = (calculate_iou(object_box, zone[0]))
                    print(f"IOU Car {camera_id} : ", iou)
                    if iou:
                        car_detections.append(([x1, y1, int(x2-x1), int(y2-y1)], row[4].item(), label))

            if labels[i] == 3.0:
                if ("Truck" in classes_to_detect):
                    label = "Truck"
                    iou = (calculate_iou(object_box, zone[0]))
                    print(f"IOU Truck {camera_id}: ", iou)
                    if iou:
                        truck_detections.append(([x1, y1, int(x2-x1), int(y2-y1)], row[4].item(), label))
                        

    detections = [person_detections, car_detections, truck_detections]
    label_list = ["Person", "Car", "Truck"]

    if ("Person" in classes_to_detect):
        frame, track_id_histories, alert_amount = tracking.tracking(camera_id, detections, frame, object_trackers, label_list, track_id_histories, alert_amount)
    if ("Car" in classes_to_detect):
        frame, track_id_histories, alert_amount = tracking.tracking(camera_id, detections, frame, object_trackers, label_list, track_id_histories, alert_amount)
    if ("Truck" in classes_to_detect):
        frame, track_id_histories, alert_amount = tracking.tracking(camera_id, detections, frame, object_trackers, label_list, track_id_histories, alert_amount)

    return frame, track_id_histories, alert_amount