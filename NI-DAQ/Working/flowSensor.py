import nidaqmx
#import time

toggle = True
task_data = nidaqmx.Task()
port = "/Dev1/ctr0"
task_data.ci_channels.add_ci_count_edges_chan(port)#,initial_count=0)
task_data.ci_channels[0].ci_count_edges_term="/Dev1/PFI0"
task_data.start()

#it works
def dataCollect():
    
    while toggle:

        freq = task_data.read()
        print(freq)
        

    return freq

try:
    dataCollect()
except KeyboardInterrupt:
    print("INTERRUPTED")
finally:
    task_data.close()
