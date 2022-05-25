import numpy as np
import nidaqmx
from nidaqmx.constants import LineGrouping

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
    linearconvertPSIG = np.interp(256,[5,1000],[0,5])
    #Map values using calibration function (to psia)
    calib_convertPSIG = (150.18 * dataIN) + 0.1156
    #convertcmH20 = m * 70.307
    #pSenTask.stop
    #pSenTask.close()
    #print(calib_convertPSIG)
    return calib_convertPSIG


def loopData():
    while True:
        print(pressureTransducer())

try:
    loopData()

except KeyboardInterrupt:
    print("INTERUPTED")

finally:
    pSenTask.stop
    pSenTask.close()