import json

def get_camera_data(cam_mgmt_json_file):
    
    camera_list= []
    json_name_list = []
    rtsp_url_list = []
    picture_path_list = []
    zone_points_list = []
    detection_classes_list = []
    camera_running_list = []

    with open(cam_mgmt_json_file) as f:
        data = json.load(f)
        for item in data:
            camera_list.append(item['camera'])
            json_name_list.append(item['json-name'])
            rtsp_url_list.append(item['rtsp-url'])
            picture_path_list.append(item['picture_path'])
            zone_points_list.append(item['zone_points'])
            detection_classes_list.append(item['detection_classes'])
            camera_running_list.append(item['camera_status'])
        
    return camera_list, json_name_list, rtsp_url_list, picture_path_list, zone_points_list, detection_classes_list, camera_running_list