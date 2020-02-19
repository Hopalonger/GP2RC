import inputs
from inputs import get_gamepad
import threading
import time
import datetime
import socket
Filename = 'Controller';
PreviousValue = 0
Average = 0
Xbox360 = [ "LeftJoyX","LeftJoyY", "LeftJoyClick" , "LeftTrig", "RightTrig", "RightBump","LeftBump","StartButton","MenuButton","XButton","YButton" ,"AButton","BButton" ,"dPadY","dPadx" ,"RightJoyX","RightJoyY","RightJoyClick","XboxButton"]
Values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Xbox360Values = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
InputCodes = [ 'ABS_X', 'ABS_Y', 'BTN_THUMBL', 'ABS_Z', 'ABS_RZ', 'BTN_TR', 'BTN_TL', 'BTN_START', 'BTN_SELECT', 'BTN_WEST', 'BTN_NORTH', 'BTN_SOUTH', 'BTN_EAST', 'ABS_HAT0Y', 'ABS_HAT0X', 'ABS_RX', 'ABS_RY',"BTN_THUMBR"]
JoySticks = [0,1,15,16]
CLIENT_IP = "192.168.1.160"
UDP_PORT = 5005
print( "UDP target IP:", CLIENT_IP)
print( "UDP target port:", UDP_PORT)
print("Xbox Codes Lengths: " + str(len(Xbox360)))
print("Xbox Values Lengths: " + str(len(Values)))
print("Input Codes Lengths: " + str(len(InputCodes)))
time.sleep(2)
# Initilize gamepad
gamepad=None
if not gamepad:
        gamepad = inputs.devices.gamepads[0]
print("Running...")

# ------------------------ ALl ABOVE COPYED FROM V1 ----------------------------- #
# ABSTRACT
# This software was created for all functions to be called and all useful data to be stored in global functions
# this is so the Timer interupt threads can run functions on certian invervals
# Run This event constantly to get all of the input from the game controllers
def GetEvents():
    events = get_gamepad()
    for event in events:
        if event.code != "SYN_REPORT" and event.code != "SYN_DROPPED":
            Place = InputCodes.index(event.code)
            Code = Xbox360Values[Place]

            if Place in JoySticks:
                NewValue = (((event.state - -32762) * 255 )/ 65534)
                Values[Place] = round(NewValue)
            #    print(Values)

            else:
                Values[Place] = event.state
            #    print(Values)

# Create A nice user readout of the system working
# also calculates the time from starting each Loop to time that it takes to end each loop
def PrintScreen():
    After = datetime.datetime.now()
    TimeDiffrence = After - Now
    TimeDiffrence_ms = TimeDiffrence.total_seconds() * 1000
    Latency  = (str(TimeDiffrence_ms)[:5] + '..') if len(str(TimeDiffrence_ms)) > 5 else str(TimeDiffrence_ms)
    print(str(Values)[1:-1] + " Latency: " + Latency + " (ms)                   "  , end="\r", flush=True)
def Save():
    f = open(Filename + ".txt", "w")
    f.write(str(Values)[1:-1])
    f.close()
    print('saved')
def UDP():
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.sendto(str.encode(str(Values)[1:-1]), (CLIENT_IP, UDP_PORT))
while True:
    Now = datetime.datetime.now()
    GetEvents()
    PrintScreen()
    UDP()
