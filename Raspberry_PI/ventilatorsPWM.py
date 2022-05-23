import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)

p=GPIO.PWM(12, 800)
p1=GPIO.PWM(35, 800)

p.start(0)
p1.start(0)

def engagePump():#channel, dc):
    """Engage Pumps
    Channel 0 or 1
    0<=dc<=100
    """
    """
    if channel==0:
        p.ChangeDutyCycle(dc)
    elif channel==1:
        p1.ChangeDutyCycle(dc)
    """
    for dc in range(0, 101, 5):
        p.ChangeDutyCycle(dc)
        p1.ChangeDutyCycle(dc)
        time.sleep(0.1)
    for dc in range(100, -1, -5):
        p.ChangeDutyCycle(dc)
        p1.ChangeDutyCycle(dc)
        time.sleep(0.1)
try:
    """
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
    
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(5)
    """
    engagePump()
    engagePump()
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.HIGH)
    time.sleep(5)

except KeyboardInterrupt:
    print("\n")

finally:
    p.stop()
    p1.stop()
    GPIO.cleanup()