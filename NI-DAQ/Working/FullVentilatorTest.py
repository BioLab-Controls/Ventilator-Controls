#from unittest import TestResult
#from wsgiref.simple_server import sys_version
import time
import nidaqmx
from nidaqmx.constants import(LineGrouping)
#from numpy import promote_types
import csv
import matplotlib.pyplot as plt
#from transducerDriver import process

#instructions for test
inst=[0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,0,1,0,3,1,0,1,2.5,] #20 cycles
#New instruction set
#Index order
#0 = Valve B, 1 = Valve C, 2 = Pump No, 3 = Time
#[0,0,0,6]
#Fill instructions
#Drain pump = 1
#Fill pump = 0
#Fill with air = Valve C Open + Valve B closed
#[1,0,1,7]
#Push to patient = Valve B open + Valve C closed
#[0,1,0,7]

#pressure setup
pressureAR = []
pTimeAR = []

task_press = nidaqmx.Task()
pPort = "Dev1/ai0"
task_press.ai_channels.add_ai_voltage_chan(pPort)
task_press.start()

#flow setup
flowAR=[]
fTimeAR=[]

task_flow = nidaqmx.Task()
fPort = "/Dev1/ctr0"
task_flow.ci_channels.add_ci_count_edges_chan(fPort)#,initial_count=0)
task_flow.ci_channels[0].ci_count_edges_term="/Dev1/PFI0"
task_flow.start()

#valves setup
task_val = nidaqmx.Task()
task_val.do_channels.add_do_chan("Dev1/port1/line0:1", line_grouping=LineGrouping.CHAN_PER_LINE)
task_val.start()

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
    #calib_convertPSIG = (150.18 * dataIN) + 0.1156
        #Das said to use this^
        #convertcmH20 = m * 70.307
        #task_press.stop
        #task_press.close()
        #print(calib_convertPSIG)
    pressureAR.append(dataIN)#calib_convertPSIG)
    pTimeAR.append(elapTime)

    print(dataIN)#calib_convertPSIG)

    return dataIN, elapTime #changed calib to datain



def flowSense(task_PWM):

    """
    Calculates flowrate based on counter. 15000 ticks per gallon,
    so (ticks/15000)/time is equal to gallons/second
    """

    startTime=time.time()
    freq=[]

    while ((time.time()-startTime)<0.1): #increased sampling rate
        freq.append(task_flow.read())
        #KWABENA MADE THIS AND WHOAHHHHHHHHHHH
        task_PWM.write(True)

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

    """
    Plot obtained data
    """
    plt.scatter(timeData,data)
    plt.title(label +' Vs. Time')
    plt.xlabel('Time')
    plt.ylabel(label)
    plt.show()



def dataCollect(task_PWM):

    """
    an umbrella function that strings together data collection functions
    """

    pressureTransducer()

    flowSense(task_PWM)


def toggleValves(order):
    task_val.write(order)
    

def PWM(values, motor, runtime):

    """
    Runs motors using janky PWM function, takes pwm value, motor select (0,1), and time
    """

    toggle = True
    task_PWM = nidaqmx.Task()

    if motor == 0:
        task_PWM.do_channels.add_do_chan("Dev1/port0/line0")
    else:
        task_PWM.do_channels.add_do_chan("Dev1/port0/line1")
        
    task_PWM.start()
        
    time_init = time.time()
        
    while toggle:
        #calls function to collect data		
        dataCollect(task_PWM)
        for i in range(0, 255):
            if i < values:
                    task_PWM.write(True)
            else:
                    task_PWM.write(False)
                            
        i = 0

        if ((time.time() - time_init) >= runtime):
            task_PWM.write(False)
            toggle = False
            task_PWM.stop()
            task_PWM.close()


try:
    #Kwabena Edited this so now the instructions take 4 parameters
    totTimeInit=time.time()

    #index for testing instrucitons
    count=0

    while count<len(inst):

        motor = inst[count+2]

        timeD = inst[count+3]

        
        valveOrder = [bool(inst[count]),bool(inst[count + 1])]
        toggleValves(valveOrder)

        time_init = time.time()

        while (time.time() - time_init) <= int(timeD):
                PWM(245,int(motor),int(timeD))
       
        count +=4 #increment count to iterate through instructions


except KeyboardInterrupt:
	print ("\nProgram Terminated")



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

    task_val.stop()
    task_val.close()