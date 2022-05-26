#from unittest import TestResult
#from wsgiref.simple_server import sys_version
import time
import nidaqmx
#from nidaqmx.constants import(LineGrouping)
#from numpy import promote_types
import csv
import matplotlib.pyplot as plt
#from transducerDriver import process

pressureAR = []
timeAR = []

#setup
pSenTask = nidaqmx.Task()
port = "Dev1/ai0"
pSenTask.ai_channels.add_ai_voltage_chan(port)
pSenTask.start()

def pressureTransducer():
        #Create task 
        #pSenTask = nidaqmx.Task()
        #IO
        #port = "Dev1/ai0"
        #pSenTask.ai_channels.add_ai_voltage_chan(port)
        #pSenTask.start()
    dataIN = pSenTask.read()
    elapTime=time.time()-totTimeInit
        #linearconvertPSIG = np.interp(256,[5,1000],[0,5])
        #Map values using calibration function (to psia)
    calib_convertPSIG = (150.18 * dataIN) + 0.1156
        #Das said to use this^
        #convertcmH20 = m * 70.307
        #pSenTask.stop
        #pSenTask.close()
        #print(calib_convertPSIG)
    pressureAR.append(calib_convertPSIG)
    timeAR.append(elapTime)

    return calib_convertPSIG, elapTime


def loopData():

    #    while True:
        print(pressureTransducer())
            

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
		
        
            loopData()
            for i in range(0, 255):
                if i < values:
                    task_PWM.write(True)
                else:
                    task_PWM.write(False)
                    
            i = 0
		#process()
		#calls the transducer driver junk

            if ((time.time() - time_init) >= runtime):
                task_PWM.write(False)
                toggle = False
                task_PWM.stop
                task_PWM.close()

try:
    totTimeInit=time.time()
    while 1:
        motor = input("Enter motor: ")

        timeD = input("Enter Time: ")

        time_init = time.time()

        while (time.time() - time_init) <= int(timeD):
                PWM(245,int(motor),int(timeD))

except KeyboardInterrupt:
	print ("Program Terminated")

finally:
    #plot the data
    plt.scatter(pressureAR,timeAR)
    plt.ylabel('Time')
    plt.xlabel('Pressure')
    plt.show()
    #update the data.csv
    updatePres(pressureAR,timeAR)
    #kill NI Tasks
    pSenTask.stop
    pSenTask.close()

