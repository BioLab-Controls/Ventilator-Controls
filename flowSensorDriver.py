import nidaqmx
from nidaqmx.constants import LineGrouping
import time
import numpy as np

def dataCollect(values,flowOn,runtime):
    toggle = True
    task_data = nidaqmx.Task()
    portA = "Dev1/port0/line6" # Counter
    portB = "Dev1/port0/line7" # Frequency
    task_data.ci_channels.add_ci_count_edges_chan(portA)
    task_data.ci_channels.add_ci_count_edges_chan(portB)

    task_data.start()
    count = task_data.read(portA)
    freq = task_data.read(portB)

    return count
    return freq
    