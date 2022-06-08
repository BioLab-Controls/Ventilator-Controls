import time
import nidaqmx
from nidaqmx.constants import(LineGrouping)

inst=[0,1,0,3]

def toggleValves(task_val,order):
    task_val.do_channels.add_do_chan("Dev1/port1/line0:1", line_grouping=LineGrouping.CHAN_PER_LINE)
    task_val.start()
    task_val.write(order)


def killTasks(task_val,task_PWM):
    #kill NI Tasks
    task_PWM.stop()
    task_PWM.close()
    task_val.stop()
    task_val.close()

def motorToggle(task_PWM,values, motor, runtime):

    """
    Runs motors using janky PWM function, takes pwm value, motor select (0,1), and time
    """

    toggle = True

    if motor == 0:
        task_PWM.do_channels.add_do_chan("Dev1/port0/line0")
    else:
        task_PWM.do_channels.add_do_chan("Dev1/port0/line1")
        
    task_PWM.start()
        
    time_init = time.time()
        
    while toggle:
        #calls function to collect data		
        for i in range(0, 255):
            if i < values:
                    task_PWM.write(True)
            else:
                    task_PWM.write(False)
                            
        i = 0

        if ((time.time() - time_init) >= runtime):
            task_PWM.write(False)
            toggle = False



def main():
    #New instruction set
    #Index order
    #0 = Valve B, 1 = Valve C, 2 = Pump No, 3 = Time
    #[0,0,0,6]
    #Fill instructions
    #Drain pump = 1
    #Fill pump = 0
    #Fill with air = Valve C Open + Valve B closed
    #[1,0,1,7]
    #Push to patient = Valve B open + Valve C closed
    #[0,1,0,7]

    #Motor
    task_PWM = nidaqmx.Task()
    #Valve
    task_val = nidaqmx.Task()

    #index for testing instrucitons
    count=0

    while count<len(inst):

        motor = inst[count+2]

        timeD = inst[count+3]

        
        valveOrder = [bool(inst[count]),bool(inst[count + 1])]
        toggleValves(task_val,valveOrder)

        time_init = time.time()

        while (time.time() - time_init) <= int(timeD):
                motorToggle(task_PWM,245,int(motor),int(timeD))
       
        count +=4 #increment count to iterate through instructions
    
    killTasks(task_val,task_PWM)
    

try:
    main()

except KeyboardInterrupt:
    print ("\nProgram Terminated")
