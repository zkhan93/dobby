from flask import Flask
import redis
import logging

logging.basicConfig(level=logging.INFO)

rq = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)
channel = "main"


def create_app():

    app = Flask(__name__)
    app.config.from_object("config")

    from .api.wheels.views import wheels as wheelsapi
    from .api.cam.views import cam as camapi
    from .api.ultrasonic.views import path as pathapi

    app.register_blueprint(wheelsapi)
    app.register_blueprint(camapi)
    app.register_blueprint(pathapi)

    return app
