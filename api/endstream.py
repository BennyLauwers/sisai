import json
from flask import request

from flask import Blueprint

end_stream_bp = Blueprint('end_stream', __name__)

@end_stream_bp.route('/api/endstream', methods=['POST'])
def end_stream_post():
    result = request.json
    end_stream = result['end_stream']

    return json.dumps(end_stream), 200, {'ContentType': 'application/json'} 