import redis
import json
import time
from web import rq
import logging

logger = logging.getLogger("app.api.wheels")

def put(name, data):
    while True:
        try:
            rcvd = rq.publish(name, json.dumps(data))
            if rcvd > 0:
                break
            logger.warning("not published")
        except redis.ConnectionError as ex:
            logger.exception(f"Error publishing to {name}")
        time.sleep(0.1)
