import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

p=GPIO.PWM(12, 50)

p.start(0)
try:
    """
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
    """
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(5)
except KeyboardInterrupt:
    print("\n")

finally:
    p.stop()
    GPIO.cleanup()