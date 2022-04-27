#Important for PID process identification
kp = 0.5
ki = 0.2
kd = 0.1
error_previous = 0
error_integral = 0

dt = 0

error = 0
processVar = 0
derivative = 0
proportional = 0
integral = 0

def getProportional():
    proportional = kp * error
    return proportional


def getIntegral():
    integral = ki * error_integral
    return integral


def getDerivative():
    derivative = kd * derivative
    return derivative


def PID_MAIN(current,setpoint):
    processVar = current
    error = setpoint - processVar
    error_integral += error * dt
    derivative = (error - error_previous) / dt
    error_previous = error
    dv = getDerivative()
    it = getIntegral()
    prop = getProportional()
    result = proportional + integral + derivative
    return result
