import cv2

import inference.ita_update_alerts as update

def tracking(camera_id, detections, frame, object_trackers, label_list, track_id_histories, alert_amount):
    if label_list[0] == "Person":
        tracks_person = object_trackers[0].update_tracks(detections[0], frame=frame)
    
        for track_person in tracks_person:
            if not track_person.is_confirmed():
                continue
            track_id_person= track_person.track_id
            ltrb_person = track_person.to_ltrb()
        
            ltrb_box_person = ltrb_person

            cv2.putText(frame, "Person: " + str(track_id_person), (int(ltrb_box_person[0]) + 10, int(ltrb_box_person[1])+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if int(track_id_person) > track_id_histories[0]:
                alert_amount+=1
                update.update_json_alerts(camera_id, alert_amount)
            
            if  int(track_id_person) > track_id_histories[0]:
                track_id_histories[0] = int(track_id_person)

    if label_list[1] == "Car":
        tracks_car = object_trackers[1].update_tracks(detections[1], frame=frame)
    
        for track_car in tracks_car:
            if not track_car.is_confirmed():
                continue
            track_id_car= track_car.track_id
            ltrb_car = track_car.to_ltrb()
        
            ltrb_box_car = ltrb_car

            cv2.putText(frame, "Car: " + str(track_id_car), (int(ltrb_box_car[0]) + 10, int(ltrb_box_car[1])+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if int(track_id_car) > track_id_histories[1]:
                alert_amount+=1
                update.update_json_alerts(camera_id, alert_amount)
            
            if  int(track_id_car) > track_id_histories[1]:
                track_id_histories[1] = int(track_id_car)

    if label_list[2] == "Truck":
        tracks_truck = object_trackers[2].update_tracks(detections[2], frame=frame)
    
        for track_truck in tracks_truck:
            if not track_truck.is_confirmed():
                continue
            track_id_truck= track_truck.track_id
            ltrb_truck = track_truck.to_ltrb()
        
            ltrb_box_truck = ltrb_truck

            cv2.putText(frame, "Truck: " + str(track_id_truck), (int(ltrb_box_truck[0]) + 10, int(ltrb_box_truck[1])+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if int(track_id_truck) > track_id_histories[2]:
                alert_amount+=1
                update.update_json_alerts(camera_id, alert_amount)
            
            if  int(track_id_truck) > track_id_histories[2]:
                track_id_histories[2] = int(track_id_truck)
            

    return frame, track_id_histories, alert_amount