import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
ledpin = 18
GPIO.setup(ledpin, GPIO.OUT)
pwm=GPIO.PWM(ledpin, 1000) #1kHz
counter = 0
dc=0
pwm.start(dc)

try:
	for dc in range(0,101,5):
		pwm.ChangeDutyCycle(dc)
		sleep(.05)
		print (dc)
	for dc in range(95, 0, -5):    # Loop 95 to 5 stepping dc down by 5 each loop
		pwm.ChangeDutyCycle(dc)
		sleep(0.05)             # wait .05 seconds at current LED brightness
		print(dc)

	print ("done!")

except KeyboardInterrupt:

	print ("\nOh no!")

finally:
	GPIO.cleanup()
