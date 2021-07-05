import redis
import time
import sys
import logging
from datetime import datetime

from sensor import DistanceSensor
import redis

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("distance")

rq = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)
ns = "DISTANCE"

def ultrasound():
    freq = config.INTERVAL
    logger.info("ultrasound started")
    with DistanceSensor(echo=config.ULTRASONIC_ECHO, trigger=config.ULTRASONIC_TRIGGER) as sensor:
        while True:
            try:
                distance = sensor.measure()
                if distance > 0:
                    rq.set("OBSTACLE", distance)
                    rq.set(f"{ns}:VALUE", distance)
                    rq.set(f"{ns}:TIME", datetime.utcnow().isoformat())
                time.sleep(freq)
            except Exception:
                logger.exception("ultrasound process errored")

if __name__ == '__main__':
    ultrasound()