import numpy as np
import nidaqmx
from nidaqmx.constants import LineGrouping

def pressureTransducer():
    #Create task 
    pSenTask = nidaqmx.Task()
    #IO
    port = "Dev1/port0/line0"
    pSenTask.ai_channels.add_ai_func_gen_chan(port)
    pSenTask.start()
    dataIN = pSenTask.read()
    #Map values using calibration function (to psia)
    convertPSIG = (150.18 * dataIN) + 0.1156
    convertcmH20 = convertPSIG * 70.307
    pSenTask.stop
    pSenTask.close()
    return convertcmH20


	






