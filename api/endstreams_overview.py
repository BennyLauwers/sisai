import json
from flask import request

from flask import Blueprint

end_streams_overview_bp = Blueprint('end_streams_overview', __name__)

@end_streams_overview_bp.route('/api/endstreamsoverview', methods=['POST'])
def end_streams_overview_post():
    result = request.json
    end_stream = result['end_stream']

    return json.dumps(end_stream), 200, {'ContentType': 'application/json'} 