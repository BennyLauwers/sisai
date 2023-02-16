from flask import Blueprint
from flask import render_template

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

livestreams_bp = Blueprint('livestreams', __name__)

@livestreams_bp.route('/livestreams_overview/<page_id>')
def livestreams(page_id):
    camera_list, _, _, _, _, _, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)

    amount_pages = len(camera_list) // 4
    remainder = len(camera_list) % 4

    if remainder == 0:
        remainder_page = 0
    else:
        remainder_page = 1
    total_pages = amount_pages + remainder_page
    pages_array = []
    for i in range(1, total_pages+1):
        pages_array.append(i)
    
    streams_range = (int(page_id) - 1) * 4
    streams_on_page = []
    if (int(page_id) == pages_array[-1]) and (remainder != 0):
        for i in range(0+streams_range, remainder+streams_range):
            streams_on_page.append(camera_list[i])
    else:
        for i in range(0+streams_range, 4+streams_range):
            streams_on_page.append(camera_list[i])

    return render_template('/livestream/livestreams_overview.html', len = len(streams_on_page), camera_list = streams_on_page, pages = pages_array, page_array_len = len(pages_array), page_id = int(page_id))