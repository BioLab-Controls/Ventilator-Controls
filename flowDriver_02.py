import nidaqmx

def dataCollect():
    task = nidaqmx.Task()
    task.di_channels.add_di_chan("Dev1/port0/line1")
    task.start()

    value = task.read()
    
    if value == True:
        value = 1
    elif value == False:
        value = 0

    # flowData = []

    
    print(value)

    task.stop
    task.close()