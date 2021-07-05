from flask import Blueprint, jsonify, request
from web import queue

cam = Blueprint("cam_api_app", __name__, url_prefix="/api/cam")
channel = "CAM"


@cam.route("/angle/<string:angle>")
def move(angle):
    # -90 to 90 angle
    queue.put(channel, dict(angle=int(angle)))
    return jsonify(dict(res="success"))
