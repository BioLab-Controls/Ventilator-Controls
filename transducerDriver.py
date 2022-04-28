import numpy as np
import nidaqmx
from nidaqmx.constants import LineGrouping

def pressureTransducer():
    #Create task 
    pSenTask = nidaqmx.Task()
    #IO
    port = "Dev1/port1/line1"
    pSenTask.di_channels.add_di_chan(port)
    pSenTask.start()
    dataIN = pSenTask.read()
    #Map values using calibration function (to psia)
    convertPSIG = (150.18 * dataIN) + 0.1156
    convertcmH20 = convertPSIG * 70.307
    pSenTask.stop
    pSenTask.close()
    return convertcmH20


def loopData():
    while True:
        print(pressureTransducer())
