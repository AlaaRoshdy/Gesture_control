import numpy as np
from time import sleep
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
flag = 0
gyroXAngle, gyroYAngle, compAngleX, compAngleY, kalAngleY = ang.init()
while(True):
    try:
        angles = ang.get_angles(gyroXAngle, gyroYAngle, compAngleX, compAngleY, kalAngleY)
        if angles is None:
            flag += 1
        else:
            kalAngleX, kalAngleY, gyroXAngle, gyroYAngle, compAngleX, compAngleY = angles
        if(flag >100): #Problem with the connection
            print("There is a problem with the connection")
            flag=0
            continue

        if(kalAngleY >= 45):
            pwm.ChangeDutyCycle(0)
            continue
        DC = kalAngleX/18 + 2
        pwm.ChangeDutyCycle(DC)
    except KeyboardInterrupt: 
        pwm.stop()
        GPIO.cleanup() 
        break