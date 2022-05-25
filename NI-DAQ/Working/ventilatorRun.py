from unittest import TestResult
from wsgiref.simple_server import sys_version
import time
import nidaqmx
from nidaqmx.constants import(LineGrouping)

def PWM(values, motor, runtime):

	toggle = True
	
	task_PWM = nidaqmx.Task()

	if motor == 0:
		task_PWM.do_channels.add_do_chan("Dev1/port0/line0")
	else:
		task_PWM.do_channels.add_do_chan("Dev1/port0/line1")
	
	task_PWM.start()
	
	time_init = time.time()
	
	while toggle:
		
		for i in range(0, 255):
			if i < values:
				task_PWM.write(True)
			else:
				task_PWM.write(False)
				
		i = 0

		if ((time.time() - time_init) >= runtime):
			task_PWM.write(False)
			toggle = False
			task_PWM.stop
			task_PWM.close()
try:
	while 1:
		motor = input("Enter motor: ")

		timeD = input("Enter Time: ")

		time_init = time.time()

		while (time.time() - time_init) <= int(timeD):
			PWM(245,int(motor),int(timeD))

except KeyboardInterrupt:
	print ("Program Terminated")

