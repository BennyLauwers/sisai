from flask import Blueprint
from flask import render_template

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

add_camera_bp = Blueprint('add_camera', __name__)

@add_camera_bp.route('/mycameras/settings/add_camera')
def add_camera():
    camera_list, _, _, _, _, _, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    return render_template(
        "/my_cameras/settings/add_camera.html",
        camera_list = camera_list
        )