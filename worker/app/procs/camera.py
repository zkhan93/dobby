from gpiozero import AngularServo
import time
import config
import json



def cam_action(msg):
    servo = AngularServo(config.CAMSERVO_TILT, 
        min_pulse_width=0.2/1000,
        max_pulse_width=1.8/1000,
        frame_width=20/1000,
    )
    angle = json.loads(msg["data"])["angle"]
    if angle <= 90 and angle >= -90:
        servo.angle = angle
    time.sleep(1)
    
