import nidaqmx
from nidaqmx.constants import LineGrouping
import time
import numpy as np

toggle = True
task_data = nidaqmx.Task()
port = "Dev1/port0/line6"

def dataCollect():
    
    while toggle:

        task_data.ci_channels.add_ci_count_edges_chan(port,initial_count=0)
        task_data.start()
        freq = task_data.read(port)
        

    return freq

try:
    dataCollect()
except KeyboardInterrupt:
    task_data.close()
