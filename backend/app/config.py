import os

DEBUG = os.getenv('DEBUG', False)

REDISTOGO_URL = os.getenv('REDISTOGO_URL', 'redis://redis:6379')

WHEEL_GPIO = (22, 24, 16,18)
ULTRASONIC_GPIO = (7, 8)
CAMSERVO_GPIO = (13, 15)
