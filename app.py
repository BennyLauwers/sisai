from flask import Flask
from flask import render_template

from views.add_camera import add_camera_bp
from views.live_video import live_video_bp
from views.video_feed import video_feed_bp
from views.my_cameras import my_cameras_bp
from views.camera_settings import my_camera_settings_bp
from views.camera_initialization import camera_initialization_bp
from views.add_zone import add_zone_bp
from views.livestreams_overview import livestreams_bp
from views.video_feeds_overview import video_feeds_overview_bp

from api.getdaysspan import get_days_span_bp
from api.getdaysintervalpicker import get_days_interval_picker_bp
from api.connectcamera import connect_camera_bp
from api.createimage import create_image_bp
from api.deletecamera import delete_camera_bp
from api.resetparameters import reset_parameters_bp
from api.getzonepoints import get_zone_points_bp
from api.endstream import end_stream_bp
from api.endstreams_overview import end_streams_overview_bp
from api.passcamerastatus import pass_camera_status_bp

import datetime
from datetime import datetime as dt

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd
import utilities.def_get_daily_alert_ticker as gdat

app = Flask(__name__)
app.register_blueprint(add_camera_bp)
app.register_blueprint(live_video_bp)
app.register_blueprint(video_feed_bp)
app.register_blueprint(my_cameras_bp)
app.register_blueprint(my_camera_settings_bp)
app.register_blueprint(camera_initialization_bp)
app.register_blueprint(add_zone_bp)
app.register_blueprint(livestreams_bp)
app.register_blueprint(video_feeds_overview_bp)

app.register_blueprint(get_days_span_bp)
app.register_blueprint(get_days_interval_picker_bp)
app.register_blueprint(connect_camera_bp)
app.register_blueprint(create_image_bp)
app.register_blueprint(delete_camera_bp)
app.register_blueprint(reset_parameters_bp)
app.register_blueprint(get_zone_points_bp)
app.register_blueprint(end_stream_bp)
app.register_blueprint(end_streams_overview_bp)
app.register_blueprint(pass_camera_status_bp)


@app.route('/')
def index():
    today = datetime.date.today()
    now = dt.now().strftime("%H:%M:%S")
    today_formatted = today.strftime('%d %b %Y')
    yesterday = today - datetime.timedelta(days=1)

    cnst.TODAY = datetime.date.today()
    cnst.YESTERDAY = today - datetime.timedelta(days=1)
    cnst.TODAY_FORMATTED = today_formatted
    cnst.YESTERDAY_FORMATTED = yesterday.strftime('%d-%m-%Y')
    
    camera_list, json_name_list, _, _, _, _, _= gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    array_todays_alert_values = []
    array_delta_values = []
    for i in range(len(camera_list)):
        todays_alert_values, alerts_delta = gdat.get_daily_alert_ticker(cnst.CAMERA_DATA_JSON_PATH+json_name_list[i])
        array_todays_alert_values.append(todays_alert_values)
        array_delta_values.append(alerts_delta)

    #define rows and columns for visualisation
    amount_full_rows = len(camera_list) // 4

    return render_template('index.html', len = len(camera_list), full_rows = amount_full_rows, todays_alert_values=array_todays_alert_values, delta = array_delta_values, camera_list = camera_list, today_formatted=today_formatted)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")