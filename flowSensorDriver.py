

def dataCollect(values,flowOn,runtime):
    toggle = True
    while toggle:
        task_data = nidaqmx.Task()
        portA = "Dev1/port1/line0" # Counter
        portB = "Dev1/port1/line1" # Frequency
        task_data.ci_channels.add_ci_count_edges_chan(portA,initial_count=0)
        task_data.ci_channels.add_ci_count_edges_chan(name_to_assign_to_channel = portB, edge = Edge.RISING)

        task_data.start()
        freq = task_data.read(portA)
        #freq = task_data.read(portB)
        task_data.close()

    return freq    