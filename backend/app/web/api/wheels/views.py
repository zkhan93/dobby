import json
from flask import Blueprint, jsonify
import logging
from web import queue

channel = "WHEELS"
wheels = Blueprint("wheels_api_app", __name__, url_prefix="/api/wheels")


@wheels.route("/<string:direction>/<float:speed>/<float:secs>", defaults={"secs": 1.0, "speed": 1})
@wheels.route("/<string:direction>/<float:speed>", defaults={"speed": 1.0,})
@wheels.route("/<string:direction>")
def back(direction, speed=1, secs=1.0):
    queue.put(channel, dict(direction=direction, duration=secs, speed=speed))
    return jsonify(dict(res="success"))

@wheels.route("/keep/<string:direction>")
def keep_moving(direction):
    if direction not in "forward back right left".split():
        return jsonify(dict(result="Invalid direction"))
    queue.put(channel, dict(direction=direction, duration=5))
    return jsonify(dict(res="job queued"))
