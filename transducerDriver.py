import numpy as np

def pressureTransducer():
    #Create task 
    pSenTask = nidaqmx.Task()
    #IO
    port = "Dev1/port0/line0"
    pSenTask.ai_channels.add_ai_func_gen_chan(port)
    pSenTask.start()
    dataIN = pSenTask.read()
    #Map values fro 0 - 5 Vdc to 5 - 1000 psia
    conv = np.interp(dataIN,[5,1000],[0,5])
    return conv

	






