import nidaqmx
from nidaqmx.stream_writers import CounterWriter
from nidaqmx.constants import *

with nidaqmx.Task() as task:
    task.co_channels.add_co_pulse_chan_time(counter = "Dev1/PFI1:0")
    task.timing.cfg_implicit_timing(sample_mode=AcquisitionType.CONTINUOUS)
    cw = CounterWriter(task.out_stream, True)
    task.start()
    cw.write_one_sample_pulse_frequency(100, 0.1, 10)

