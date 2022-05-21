import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 18
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
pwm=GPIO.PWM(RELAIS_1_GPIO, 1000) #1kHz
counter = 0
dc=0
pwm.start(dc)

try:
	for dc in range(0,101,5):
		pwm.ChangeDutyCycle(dc)
		time.sleep(.05)
		print (dc)
	for dc in range(95, 0, -5):    # Loop 95 to 5 stepping dc down by 5 each loop
		pwm.ChangeDutyCycle(dc)
		time.sleep(0.05)             # wait .05 seconds at current LED brightness
		print(dc)

	print ("done!")

except KeyboardInterrupt:

	print ("\nOh no!")

finally:
	GPIO.cleanup()
