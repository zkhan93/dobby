import logging
import json
import time
import config
from gpiozero import Robot

logger = logging.getLogger("main.wheels")

def wheel_action(msg):
    data = json.loads(msg["data"])
    duration = data["duration"]
    speed = data.get("speed", 1)
    direction = data["direction"]
    robot = Robot(left=config.WHEEL_LEFT, right=config.WHEEL_RIGHT)
    if direction in "left right forward backward".split():
        getattr(robot, direction)(speed)
        time.sleep(duration)