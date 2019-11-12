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
pwm.start(2)
flag = 0
gyroXAngle, gyroYAngle, compAngleX, compAngleY, kalAngleX, kalAngleY = ang.init()
angle = 0
while(True):
    try:
        angles = ang.get_angles(gyroXAngle, gyroYAngle, compAngleX, compAngleY, kalAngleX, kalAngleY)
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
        angle = min(angle + kalAngleX, 180)
        angle = max(angle, 0)
        pwm.ChangeDutyCycle(angle/18 + 2)
        sleep(0.5)
    except KeyboardInterrupt: 
        pwm.stop()
        GPIO.cleanup() 
        break 