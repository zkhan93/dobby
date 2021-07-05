from flask import Blueprint, jsonify
from web import rq

path = Blueprint("path_api_app", __name__, url_prefix="/api/path")


@path.route("/")
def distance():
    distance = rq.get("OBSTACLE")
    distance = float(distance) if distance is not None else distance
    return jsonify(dict(res="success", distance=distance, unit="cms"))
