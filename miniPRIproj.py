import numpy as np
from time import sleep
from scipy.interpolate import interp1d
import RPi.GPIO as GPIO
import smbus
import math

import Kalman_Filter_Python_for_mpu6050.AngleOMeter as ang


# FOR MPU

# FOR SERVO
GPIO.setmode(GPIO.BOARD)
servopin = 11
# Setting up servopin as output pin
GPIO.setup(servopin, GPIO.OUT)

# Created  PWM channels at 50Hz frequency
pwm = GPIO.PWM(servopin, 50)
# Initial duty cycle
pwm.start(0)

while(True):
    try:
        kalAngleX,kalAngleY = ang.get_angles()
        if(kalAngleY >= 45)
            pwm.ChangeDutyCycle(0)
            continue
        DC = kalAngleX
        pwm.ChangeDutyCycle(DC)
    except KeyboardInterrupt: 
        pwm.stop()
        GPIO.cleanup() 
        break