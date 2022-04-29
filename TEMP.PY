from unittest import TestResult
from wsgiref.simple_server import sys_version
import time
import nidaqmx
from nidaqmx.constants import(LineGrouping)
import numpy as np
import csv

pressureAR = []

def dataCollect():
    
    task_dataA = nidaqmx.Task()
    portA = "Dev1/ctr0"
    task_dataA.di_channels.add_di_chan(portA)
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
    pressureAR.append(freqA)

def updatePres(pdata,tdata):
    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(pdata)
        writer.writerow(tdata)

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
		
		dataCollect()
        
		i = 0

		if ((time.time() - time_init) >= runtime):
			task_PWM.write(False)
			toggle = False
			task_PWM.stop
			task_PWM.close()

        
while 1:
	motor = input("Enter motor: ")

	timeD = input("Enter Time: ")

	time_init = time.time()

	while(time.time() - time_init) <= int(timeD):
		PWM(245,int(motor),int(timeD))
		updatePres(pressureAR,timeD)

         
    