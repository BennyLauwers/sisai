import json

from flask import Blueprint
from flask import Response

import utilities.constants as cnst

import utilities.open_stream as opst 

video_feed_bp = Blueprint('video_feed', __name__)

@video_feed_bp.route('/video_feed/<camera_id>')
def video_feed(camera_id):
    status = "start"
    with open(cnst.CAMERA_MGMT_JSON_FILE) as f:
        data = json.load(f)
        zone_points = []
        rtsp = ""
        for item in data:
            if item['camera'] in [camera_id]:
                zone_points = item['zone_points']
                rtsp = item['rtsp-url']

    return Response((opst.open_stream(rtsp, zone_points, camera_id, status)), mimetype='multipart/x-mixed-replace; boundary=frame')