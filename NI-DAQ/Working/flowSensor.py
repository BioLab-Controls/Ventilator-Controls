import nidaqmx
from nidaqmx.constants import LineGrouping
import time
import numpy as np

def dataCollect(values,flowOn,runtime):
    toggle = True
    while toggle:
        task_data = nidaqmx.Task()
        port = "Dev1/port0/line6"
        task_data.ci_channels.add_ci_count_edges_chan(port,initial_count=0)
        task_data.start()
        freq = task_data.read(port)
        task_data.close()

    return freq

