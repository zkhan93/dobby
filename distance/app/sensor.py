import RPi.GPIO as GPIO
import time

class DistanceSensor:

    def __init__(self, trigger, echo):
        self.trig = int(trigger)
        self.echo = int(echo)
        self.distance = 0

    def __enter__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        return self

    def __exit__(self, type, value, traceback):
        GPIO.cleanup()

    def measure(self):
        ''' return how far the path is clear in cm
            by default to 45cm
        '''

        GPIO.output(self.trig, False)
        time.sleep(0.2)

        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        pulse_start = pulse_end = time.time()
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()

        duration = pulse_end - pulse_start  # in sec
        # 34300 (sound speed)/2(time for reaching back to origin) = 17150
        distance = duration * 17150
        distance = round(distance, 2)
        distance = distance if distance >= 2 and distance <= 400 else 0
        self.distance = distance
        return self.distance