#!/usr/bin/python
import binascii
import serial
import struct
import RPi.GPIO as GPIO #require for accessing raspi gpio
import time

deviceDetect = 7 #pin 7 is wired to device detect, it must be pulled low to turn on the robot when it's off

GPIO.setmode(GPIO.BOARD) #sets python to identify pins by the board number 
GPIO.setup(deviceDetect, GPIO.OUT) 
GPIO.output(deviceDetect, GPIO.LOW)
time.sleep(0.25)
GPIO.output(deviceDetect, GPIO.HIGH)

ser = serial.Serial('/dev/ttyAMA0', 57600) #dirtdog 57600 roomba500 115200
print ser
opcode = ''
while 1:
    opcode = str(raw_input("Enter opcode: ")).strip()
    print( "opcode: " + opcode )
    if(opcode.strip() == 'exit'.strip()):
	print 'exiting'
	ser.close()
	GPIO.cleanup()
        exit()   
    if(opcode.strip() == 'on'.strip()):
        GPIO.output(deviceDetect, GPIO.LOW)
        time.sleep(0.25)
        GPIO.output(deviceDetect, GPIO.HIGH)
        continue       
    print("Sending: ", int(opcode))
    
    if(opcode.strip() == '142'): #142 is the opcode to get sensor data 
        ser.write(struct.pack('i', 142))
	#exit()
        output = []
        time.sleep(2)
        print("Waiting for: ", ser.inWaiting())
        while ser.inWaiting():
            output.append(ser.read(1))
            print("reading")
	print("done")	            	
        worked_output = ""
	for x in output:
            worked_output += str( binascii.hexlify(x) + ", ")
        print(worked_output)        
    else:
        ser.write(struct.pack('i', int(opcode)))

