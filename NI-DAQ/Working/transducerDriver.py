from tracemalloc import start
import numpy as np
import nidaqmx
from nidaqmx.constants import LineGrouping
import csv
import time

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
    elapTime=time.time()-startTime
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

    while True:
        print(pressureTransducer())
        

def updatePres(pdata,tdata):
    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(pdata)
        writer.writerow(tdata)

try:
    startTime=time.time()
    loopData()

except KeyboardInterrupt:
    print("INTERRUPTED")

finally:
    updatePres(pressureAR,timeAR)
    pSenTask.stop
    pSenTask.close()