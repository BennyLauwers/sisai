from flask import Blueprint
from flask import render_template

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

add_zone_bp = Blueprint('add_zone', __name__)

@add_zone_bp.route('/my_cameras/settings/<camera_id>/add_zone')
def addzone(camera_id):
    camera_list, _, _, picture_path_list, _, _, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    index_value = camera_list.index(camera_id)

    image_file_path = picture_path_list[index_value]

    return render_template(
        "/my_cameras/settings/add_zone.html",
        camera = camera_id,
        path = image_file_path,
        camera_list=camera_list
        )