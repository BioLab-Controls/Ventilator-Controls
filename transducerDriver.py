import numpy as np

def pressureTransducer():
    #Create task 
    pSenTask = nidaqmx.Task()
    #IO
    port = "Dev1/port0/line0"
    pSenTask.do_channels.add_do_chan(port)
    pSenTask.start()
    dataIN = pSenTask.read()
    #Map values fro 0 - 5 Vdc to 5 - 1000 psia
    conv = np.interp(dataIN,[5,1000],[0,5])
    return conv

	






