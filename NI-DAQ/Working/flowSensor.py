from curses import keyname
import nidaqmx
from nidaqmx.constants import LineGrouping
import time
import numpy as np

task_data = nidaqmx.Task()
port = "Dev1/port0/line6"

def dataCollect():
    toggle = True
    while toggle:
        task_data.di_channels.add_di_chan(port)
        task_data.start()
        freq = task_data.read(port)

    return freq

try:
    dataCollect()
except KeyboardInterrupt:
    print("INTERRUPT")
finally:
    task_data.close()