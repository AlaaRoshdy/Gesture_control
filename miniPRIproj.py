from pykalman import KalmanFilter
import numpy as np
from time import sleep
from scipy.interpolate import interp1d
import RPi.GPIO as GPIO
import smbus
import math


# FOR MPU

# Register
power_mgmt_1 = 0x6b
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def get_y_rotation(x,y,z):
    dist = math.sqrt((y*y)+(z*z))
    radians = math.atan2(x, dist)
    return -math.degrees(radians)

# FOR SERVO
GPIO.setmode(GPIO.BOARD)
servopin = 11
# Setting up servopin as output pin
GPIO.setup(servopin,GPIO.OUT)

# Created  PWM channels at 50Hz frequency
PWM = GPIO.PWM(servopin,50)
# Initial duty cycle
PWM.start(0)


 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) for Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

print "accelerationssensor"
print "---------------------"
 
acceleration_xout = read_word_2c(0x3b)
acceleration_yout = read_word_2c(0x3d)
acceleration_zout = read_word_2c(0x3f)

acceleration_xout_remapped = interp1d([-17000,17000],[0,180])
acceleration_yout_remapped = interp1d([-17000,17000],[0,180])
acceleration_zout_remapped = interp1d([-17000,17000],[0,180])
 
print "acceleration_xout: ", ("%6d" % acceleration_xout), " scaled: ", acceleration_xout_remapped
print "acceleration_yout: ", ("%6d" % acceleration_yout), " scaled: ", acceleration_yout_remapped
print "acceleration_zout: ", ("%6d" % acceleration_zout), " scaled: ", acceleration_zout_remapped
 
y_rot = get_y_rotation(acceleration_xout_remapped, acceleration_yout_remapped, acceleration_zout_remapped) 
print "Y Rotation: " , y_rot

while(acceleration_xout_remapped>0)
    y_rot = get_y_rotation(acceleration_xout_remapped, acceleration_yout_remapped, acceleration_zout_remapped) 
    if(y_rot>=45)
        pwm.stop()
        GPIO.cleanup()
        break
    acceleration_xout = read_word_2c(0x3b)
    DC = acceleration_xout_remapped = interp1d([-17000,17000],[0,180])
    pwm.ChangeDutyCycle(DC)    