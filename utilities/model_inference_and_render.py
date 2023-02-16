import cv2

from shapely.geometry import Polygon as plg

import utilities.constants as cnst
import utilities.def_get_camera_data as gcd

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

def model_inference_and_render(camera_id, model, frame):
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
                    print("IOU: ", iou)
                    if iou:
                        person_detections.append(([x1, y1, int(x2-x1), int(y2-y1)], row[4].item(), label))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_not_ok, 3)
                        cv2.rectangle(frame, (x1-2, y1), (x1 + 375, y1 - 40), bgr_not_ok, -1)
                        cv2.putText(frame, str(label + " " + str(confidence)), (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    else:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_ok, 3)
                        cv2.rectangle(frame, (x1-2, y1), (x1 + 375, y1 - 40), bgr_ok, -1)
                        cv2.putText(frame, str(label + " " + str(confidence)), (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            if labels[i] == 2.0:
                if ("Car" in classes_to_detect):
                    label = "Car"
                    iou = (calculate_iou(object_box, zone[0]))
                    print("IOU: ", iou)
                    if iou:
                        car_detections.append(([x1, y1, int(x2-x1), int(y2-y1)], row[4].item(), label))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_not_ok, 3)
                        cv2.rectangle(frame, (x1-2, y1), (x1 + 375, y1 - 40), bgr_not_ok, -1)
                        cv2.putText(frame, str(label + " " + str(confidence)), (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    else:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_ok, 3)
                        cv2.rectangle(frame, (x1-2, y1), (x1 + 375, y1 - 40), bgr_ok, -1)
                        cv2.putText(frame, str(label + " " + str(confidence)), (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            if labels[i] == 3.0:
                if ("Truck" in classes_to_detect):
                    label = "Truck"
                    iou = (calculate_iou(object_box, zone[0]))
                    print("IOU: ", iou)
                    if iou:
                        truck_detections.append(([x1, y1, int(x2-x1), int(y2-y1)], row[4].item(), label))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_not_ok, 3)
                        cv2.rectangle(frame, (x1-2, y1), (x1 + 375, y1 - 40), bgr_not_ok, -1)
                        cv2.putText(frame, str(label + " " + str(confidence)), (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    else:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_ok, 3)
                        cv2.rectangle(frame, (x1-2, y1), (x1 + 375, y1 - 40), bgr_ok, -1)
                        cv2.putText(frame, str(label + " " + str(confidence)), (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    return frame