#!/usr/bin/python
import time
import atexit

import Adafruit_MCP3008

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from client import capture_video
import cv2

#Software SPI
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
mh = Adafruit_MotorHAT(addr=0x60)

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
cap1.set(3, 80)
cap1.set(4, 60)
cap2.set(3, 80)
cap2.set(4, 60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

left_sensor_port = 0 # Left sensor port
right_sensor_port = 1 # Right sensor port
sleep_time = 0.5 # Time in seconds to wait before next reading

left_motor_terminal = 2 # Left motor port
right_motor_terminal = 4 # Right motor port
left_motor = mh.getMotor(left_motor_terminal)
right_motor = mh.getMotor(right_motor_terminal)

# Set default direction to forward
left_motor.run(Adafruit_MotorHAT.FORWARD)
right_motor.run(Adafruit_MotorHAT.BACKWARD)

# Turn speeds
regular_speed = 50 # Forward speed between 0 to 255 
slow_speed = 20 # Wheel that moves slowly speed


threshold = 400 # Threshold value for detection between 0 to 1023

ii = 0

while True:
	left_sensor_value = mcp.read_adc(left_sensor_port)
	right_sensor_value = mcp.read_adc(right_sensor_port)
	print("Left:  %d, Right: %d" % (left_sensor_value, right_sensor_value))

	if(left_sensor_value > threshold and right_sensor_value > threshold): # Go straight
		if ii % 10 == 0:
			ii = 0
			left_motor.setSpeed(0)
			right_motor.setSpeed(0)
			capture_video(cap1, cap2)
		left_motor.setSpeed(regular_speed)
		right_motor.setSpeed(regular_speed)
	elif(left_sensor_value > threshold and right_sensor_value < threshold): # Turn right
		if ii % 10 == 0:
			ii = 0
			left_motor.setSpeed(0)
			right_motor.setSpeed(0)
			capture_video(cap1, cap2)
		left_motor.setSpeed(regular_speed)
		right_motor.setSpeed(slow_speed)
	elif(left_sensor_value < threshold and right_sensor_value > threshold): # Turn left
		if ii % 10 == 0:
			ii = 0
			left_motor.setSpeed(0)
			right_motor.setSpeed(0)
			capture_video(cap1, cap2)
		left_motor.setSpeed(slow_speed)
		right_motor.setSpeed(regular_speed)
	else: # Stop motors
		if ii % 10 == 0:
			ii = 0
			left_motor.setSpeed(0)
			right_motor.setSpeed(0)
			capture_video(cap1, cap2)
		left_motor.setSpeed(slow_speed)
		right_motor.setSpeed(slow_speed)

	time.sleep(sleep_time)
	ii+=1
