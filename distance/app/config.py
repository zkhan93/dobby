import os

DEBUG = os.getenv("DEBUG", False)
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
INTERVAL = int(os.getenv("INTERVAL"))

# BOARD numbering
ULTRASONIC_ECHO = 8
ULTRASONIC_TRIGGER = 7
