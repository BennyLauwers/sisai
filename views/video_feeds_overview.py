import json

from flask import Blueprint
from flask import Response

import utilities.constants as cnst

import utilities.open_streams_overview as opsto

video_feeds_overview_bp = Blueprint('video_feeds_overview', __name__)

@video_feeds_overview_bp.route('/video_feeds_overview/<camera_id>')
def video_feeds_overview(camera_id):
    status = "start"
    with open(cnst.CAMERA_MGMT_JSON_FILE) as f:
        data = json.load(f)
        zone_points = []
        rtsp = ""
        for item in data:
            if item['camera'] in [camera_id]:
                zone_points = item['zone_points']
                rtsp = item['rtsp-url']
        
    return Response((opsto.open_streams_overview(rtsp, zone_points, status)), mimetype='multipart/x-mixed-replace; boundary=frame')