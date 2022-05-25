from wsgiref.simple_server import sys_version
import nidaqmx
from nidaqmx.constants import(LineGrouping)
import time
import numpy as np

state_sys = 1
'''
UPDATES: Code currently receives True/False datapoints when passing through the sensor.
Prints to console slower than freqency, need new way to analyze individual points.
'''



def PWM(values, motor, runtime):
    
	toggle = True
	
	task_PWM = nidaqmx.Task()
	flw = nidaqmx.Task()

	if motor == 0:
		task_PWM.do_channels.add_do_chan("Dev1/port0/line2")
	else:
		task_PWM.do_channels.add_do_chan("Dev1/port0/line3")
	
	task_PWM.start()
	
	time_init = time.time()
	
	while toggle:
		
		for i in range(0, 255):
			if i < values:
				task_PWM.write(True)
			else:
				task_PWM.write(False)
		
		#pressureTransducer();
		
		i = 0

		if ((time.time() - time_init) >= runtime):
			task_PWM.write(False)
			toggle = False
			task_PWM.stop
			task_PWM.close()

def switch_valves(state_sys_local):

	task_val = nidaqmx.Task()
	task_val.do_channels.add_do_chan("Dev1/port1/line0:1", line_grouping=LineGrouping.CHAN_PER_LINE)
	task_val.start()
	
	global state_sys
	
	valves_0 = [True, False]
	valves_1 = [False, True]
	
	if state_sys_local == 1:
		
		task_val.write(valves_1)
		state_sys = 0
		print(state_sys)
	
	else: 

		task_val.write(valves_0)
		state_sys = 1
		print(state_sys)
		
	task_val.stop
	task_val.close()



def loopRun(inputSpeed, inputTime, outputSpeed, outputTime):
	while True:

		switch_valves(state_sys)
		PWM(inputSpeed, 1, inputTime)
		
		switch_valves(state_sys)
		PWM(outputSpeed, 0 ,outputTime)

# 1 -in
# 0 - out

loopRun(245,2.4,255,1.9)
