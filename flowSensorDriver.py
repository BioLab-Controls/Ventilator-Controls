import nidaqmx
from nidaqmx.constants import LineGrouping
import time
import numpy as np

def dataCollect():
    toggle = True
    
    task_dataA = nidaqmx.Task()
    portA = "Dev1/ctr0"
    task_dataA.ci_channels.add_ci_count_edges_chan(portA)
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
    
def loopData():
    while True:
        dataCollect()

loopData()


        