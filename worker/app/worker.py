import redis
import time
import json
import sys
import logging
from multiprocessing import Pool, Process

from procs.wheels import wheel_action
from procs.camera import cam_action

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("main")

# in main process to crash so that it can be restarted if redis is not yet up
rq = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)

def listener_loop(channel, fn):    
    p = rq.pubsub()
    p.subscribe(channel)
    logger.info(f"listening to {channel} channel")
    while True:
        try:
            message = p.get_message()
        except redis.ConnectionError:
            # Do reconnection attempts here such as sleeping and retrying
            p = rq.pubsub()
            p.subscribe(channel)
        else:
            if message and message["type"] == "message":
                logger.info(str(message))
                try:
                    fn(message)
                except Exception:
                    logger.exception("failed to performa action")
        time.sleep(0.01)

channels = [("WHEELS", wheel_action), ("CAM", cam_action)]
with Pool(len(channels)) as pool:
    pool.starmap(listener_loop, channels)
    
