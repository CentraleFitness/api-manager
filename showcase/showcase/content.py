
from flask import jsonify

def render_json_resp(**kwargs) -> dict:
    status = 'ko' if kwargs.get('status_code', 200) != 200 else 'ok'
    resp = jsonify(status=status, **kwargs)
    resp.status_code = kwargs.get('status_code', 200)
    return resp
