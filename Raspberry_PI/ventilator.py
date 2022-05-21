from rpi_hardware_pwm import HardwarePWM as hPWM
from time import sleep

#using ssh from VSCode into pi seems to eliminate the missing imports issue... good to know

#some setup
dc=0 #initial duty cycle value of 0%

pwm0=hPWM(pwm_channel=0,hz=1000)
pwm0.start(dc) #starts the pwm0 at 0% duty cycle

pwm1=hPWM(pwm_channel=1,hz=1000)
pwm1.start(dc) #starts the pwm1 at 0% duty cycle

def engagePump(pumpNo, time, duty):
    if pumpNo==0:
        pwm0.change_duty_cycle(duty)
        sleep(time)
    elif pumpNo==1:
        pwm1.change_duty_cycle(duty)
        sleep(time)

try:
    engagePump(1,10,50)

except KeyboardInterrupt:
    print ("\nTerminating Program")

finally:
    pwm0.stop
    pwm1.stop

    