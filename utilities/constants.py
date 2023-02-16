import datetime

CAMERA_MGMT_JSON_FILE = "static/json/camera_mgmt.json"
PROCESS_REGISTER_JSON_FILE = "static/json/process_register.json"
CAMERA_DATA_JSON_PATH = "static/json/camera_data/"
IMAGE_PATH = "/static/images/"

TODAY = datetime.date.today()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TODAY_FORMATTED = TODAY.strftime('%d-%m-%Y')
YESTERDAY_FORMATTED = YESTERDAY.strftime('%d-%m-%Y')