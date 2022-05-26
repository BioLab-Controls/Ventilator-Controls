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
pTimeAR = []

flowAR=[]
fTimeAR=[]


#pressure setup
task_press = nidaqmx.Task()
pPort = "Dev1/ai0"
task_press.ai_channels.add_ai_voltage_chan(pPort)
task_press.start()

#flow setup
task_flow = nidaqmx.Task()
fPort = "/Dev1/ctr0"
task_flow.ci_channels.add_ci_count_edges_chan(fPort)#,initial_count=0)
task_flow.ci_channels[0].ci_count_edges_term="/Dev1/PFI0"
task_flow.start()

def pressureTransducer():
    """
    This queries for pressure data while the motors are running
    """
        #Create task 
        #task_press = nidaqmx.Task()
        #IO
        #1 = "Dev1/ai0"
        #task_press.ai_channels.add_ai_voltage_chan(port)
        #task_press.start()
    dataIN = task_press.read()
    elapTime=time.time()-totTimeInit
        #linearconvertPSIG = np.interp(256,[5,1000],[0,5])
        #Map values using calibration function (to psia)
    calib_convertPSIG = (150.18 * dataIN) + 0.1156
        #Das said to use this^
        #convertcmH20 = m * 70.307
        #task_press.stop
        #task_press.close()
        #print(calib_convertPSIG)
    pressureAR.append(calib_convertPSIG)
    pTimeAR.append(elapTime)

    print(calib_convertPSIG)

    return calib_convertPSIG, elapTime

def flowSense():
    """
    Calculates flowrate based on counter. 15000 ticks per gallon,
    so (ticks/15000)/time is equal to gallons/second
    """

    startTime=time.time()
    freq=[]

    while ((time.time()-startTime)<1): #total time of 1 second
        freq.append(task_flow.read())

    ticks=sum(freq)
    flowRate=(ticks/15000)

    elapTime=time.time()-totTimeInit

    flowAR.append(flowRate)
    fTimeAR.append(elapTime)

    print(flowRate)

    return flowRate, elapTime


def updatePres(filename,pdata,tdata):
    """
    Updates the csv file with data acquired. Takes: filename, data, time data
    """
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(pdata)
        writer.writerow(tdata)
def plot(label,data,timeData):
    plt.scatter(data,timeData)
    plt.title(label +' Vs. Time')
    plt.ylabel('Time')
    plt.xlabel(label)
    plt.show()



def dataCollect():
    """
    an umbrella function that strings together data collection functions
    """

    pressureTransducer()

    flowSense()

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
		
        
            dataCollect()
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
                task_PWM.stop()
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
    plot('Pressure',pressureAR,pTimeAR)
    plot('Flow',flowAR,fTimeAR)
    #update the data.csv files
    updatePres("PressureData.csv",pressureAR,pTimeAR)
    updatePres("FlowData.csv",flowAR,fTimeAR)
    #kill NI Tasks
    task_press.stop()
    task_press.close()

    task_flow.stop()
    task_flow.close()

