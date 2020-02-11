from __future__ import print_function
import inputs
import datetime
from inputs import get_gamepad
#from nrf24 import NRF24
import time
import sys
# Set Code Conversion
#import colorama
Filename = 'Controller';
PreviousValue = 0
Average = 0
Xbox360 = [ "LeftJoyX","LeftJoyY", "LeftJoyClick" , "LeftTrig", "RightTrig", "RightBump","LeftBump","StartButton","MenuButton","XButton","YButton" ,"AButton","BButton" ,"dPadY","dPadx" ,"RightJoyX","RightJoyY","RightJoyClick","XboxButton"]
Values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Xbox360Values = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
InputCodes = [ 'ABS_X', 'ABS_Y', 'BTN_THUMBL', 'ABS_Z', 'ABS_RZ', 'BTN_TR', 'BTN_TL', 'BTN_START', 'BTN_SELECT', 'BTN_WEST', 'BTN_NORTH', 'BTN_SOUTH', 'BTN_EAST', 'ABS_HAT0Y', 'ABS_HAT0X', 'ABS_RX', 'ABS_RY',"BTN_THUMBR"]
JoySticks = [0,1,15,16]
print("Xbox Codes Lengths: " + str(len(Xbox360)))
print("Xbox Values Lengths: " + str(len(Values)))
print("Input Codes Lengths: " + str(len(InputCodes)))

time.sleep(2)
# Initilize gamepad

gamepad=None
if not gamepad:
        gamepad = inputs.devices.gamepads[0]
#colorama.init()
# Start the Radio
print("Running...")
"""
radio = NRF24()
radio.begin(1, 0, "P8_23", "P8_24") #Set CE and IRQ pins
radio.setRetries(15,15)
radio.setPayloadSize(8)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])

radio.startListening()
radio.stopListening()

radio.printDetails()


"""
def move_cursor(x,y):
    print ("\x1b[{};{}H".format(y+1,x+1))

def clear():
    print ("\x1b[2J")



def vibrateleft(time):
    gamepad.set_vibration(1, 0, time)

def vibrateRight(time):
    gamepad.set_vibration(0, 1, time)

def vibrateBoth(time):
    gamepad.set_vibration(1, 1, time)

def Transmit(data):
    radio.write(data)

def Receive():
    radio.startListening()
    pipe = [0]
    while not radio.available(pipe, True):
        time.sleep(1000/1000000.0)

    recv_buffer = []
    radio.read(recv_buffer)

    return recv_buffer

def Save(write,PreviousValue,Average):

    #print(str(write)[1:-1])
    After = datetime.datetime.now()
    TimeDiffrence = After - Now
    TimeDiffrence_ms = TimeDiffrence.total_seconds() * 1000

    if(TimeDiffrence_ms > PreviousValue):
        PreviousValue = TimeDiffrence_ms

    Latency  = (str(TimeDiffrence_ms)[:5] + '..') if len(str(TimeDiffrence_ms)) > 5 else str(TimeDiffrence_ms)
    MaxLatency  = (str(PreviousValue)[:5] + '..') if len(str(PreviousValue)) > 5 else str(PreviousValue)
    Average  = (str(Average)[:5] + '..') if len(str(Average)) > 5 else str(Average)
    Vroom = str(write)[1:-1] + " Latency: " + Latency + " (ms) Average Time: " + str(Average) + " (ms)"
    print(Vroom  , end="\r", flush=True)
    f = open(Filename + ".txt", "w")
    f.write(str(write)[1:-1])
    f.close()
    return PreviousValue

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

i = 0
while True:
        Now = datetime.datetime.now()
        GetEvents()
        PreValue = PreviousValue
        PreviousValue = Save(Values,PreviousValue,Average)
        i += 1
        time.sleep(.2)
        Value = PreviousValue + PreValue

        Average = Value / i
