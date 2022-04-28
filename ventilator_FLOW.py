from wsgiref.simple_server import sys_version
import nidaqmx
from nidaqmx.constants import(LineGrouping)
import time
import numpy as np
import transducerDriver as pressure


state_sys = 1
'''
Code runs the pumps, fills and empties, and records 0s from flow sensor in the terminal.
Occasionally reports a 1 when filling is complete.
'''

def dataCollect():
    
    task_dataA = nidaqmx.Task()
    portA = "Dev1/ctr0"
    task_dataA.ci_channels.add_ci_count_edges_chan(portA)
    freqA = task_dataA.read()
    task_dataA.stop
    task_dataA.close()
    
    #task_dataB = nidaqmx.Task()
    #portB = "Dev1/ctr1"
    #task_dataB.ci_channels.add_ci_count_edges_chan(portB)
    #freqB = task_dataB.read()
    #task_dataB.stop
    #task_dataB.close()
    
    print(freqA)
    #print(freqB)

def PWM(values, motor, runtime):

	toggle = True
	
	task_PWM = nidaqmx.Task()
	flw = nidaqmx.Task()

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
		
		dataCollect()
		
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