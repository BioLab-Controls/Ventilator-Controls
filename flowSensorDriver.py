import nidaqmx
from nidaqmx.constants import LineGrouping
import time
import numpy as np

def dataCollect(values,flowOn,runtime):
    toggle = True
    while toggle:
        task_data = nidaqmx.Task()
        portA = "Dev1/port0/line6" # Counter
        #portB = "Dev1/port0/line7" # Frequency
        task_data.ci_channels.add_ci_count_edges_chan(portA,initial_count=0)
        #task_data.ci_channels.add_ci_count_edges_chan(portB)

        task_data.start()
        freq = task_data.read(portA)
        #freq = task_data.read(portB)
        task_data.close()

    return freq    