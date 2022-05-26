import nidaqmx
#import time

#toggle = True
task_flow = nidaqmx.Task()
fPort = "/Dev1/ctr0"
task_flow.ci_channels.add_ci_count_edges_chan(fPort)#,initial_count=0)
task_flow.ci_channels[0].ci_count_edges_term="/Dev1/PFI0"
task_flow.start()

#it works
def flowData():
    
    #while toggle:

    freq = task_flow.read()
    print(freq)
        

    return freq

try:
    flowData()
except KeyboardInterrupt:
    print("INTERRUPTED")
finally:
    task_flow.stop()
    task_flow.close()
