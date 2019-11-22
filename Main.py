from __future__ import print_function
import inputs
from inputs import get_gamepad
#from nrf24 import NRF24
import time
import sys
# Set Code Conversion

Xbox360 = [ "LeftJoyX","LeftJoyY", "LeftJoyClick" , "LeftTrig", "RightTrig", "RightBump","LeftBump","StartButton","MenuButton","XButton","YButton" ,"AButton","BButton" ,"dPadY","dPadx" ,"RightJoyX","RightJoyY","RightJoyClick","XboxButton"]
Values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Xbox360Values = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
InputCodes = [ 'ABS_X', 'ABS_Y', 'BTN_THUMBL', 'ABS_Z', 'ABS_RZ', 'BTN_TR', 'BTN_TL', 'BTN_START', 'BTN_SELECT', 'BTN_WEST', 'BTN_NORTH', 'BTN_SOUTH', 'BTN_EAST', 'ABS_HAT0Y', 'ABS_HAT0X', 'ABS_RX', 'ABS_RY',"BTN_THUMBR"]
JoySticks = [0,1,15,16]
PreviousVals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Update = []
print("Xbox Codes Lengths: " + str(len(Xbox360)))
print("Xbox Values Lengths: " + str(len(Values)))
print("Input Codes Lengths: " + str(len(InputCodes)))
time.sleep(2)
# Initilize gamepad
gamepad=None
if not gamepad:
        gamepad = inputs.devices.gamepads[0]
        
# Start the Radio
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


def VibrateBase(time):
        from evdev import ecodes, InputDevice, ff

# Find first EV_FF capable event device (that we have permissions to use).
        for name in evdev.list_devices():
          dev = InputDevice(name)
          if ecodes.EV_FF in dev.capabilities():
            break

        rumble = ff.Rumble(strong_magnitude=0x0000, weak_magnitude=0xffff)
        effect_type = ff.EffectType(ff_rumble_effect=rumble)
        duration_ms = 1000 * time

        effect = ff.Effect(
                ecodes.FF_RUMBLE, -1, 0,
        ff.Trigger(0, 0),
        ff.Replay(duration_ms, 0),
          ff.EffectType(ff_rumble_effect=rumble)
        )

        repeat_count = 1
        effect_id = dev.upload_effect(effect)
        dev.write(e.EV_FF, effect_id, repeat_count)
        dev.erase_effect(effect_id)


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

def GetEvents():
    events = get_gamepad()
    PreviousValue = Values
    for event in events:
        #Discard Sync Function
        if event.code != "SYN_REPORT":
            Place = InputCodes.index(event.code)
            #print(Place)
            Code = Xbox360Values[Place]
            PartName = ""
                #Remap Values to 0 - 255 instead of -32,000 - 32000
            if Place in JoySticks:
                NewValue = (((event.state - -32762) * 255 )/ 65555)
                Values[Place] = round(NewValue)
                #print(Values)
                code = Xbox360Values[Place]
                print( Xbox360[code] + ": " + str(Values[Place]))
                
            else:
                Values[Place] = event.state
                #print(Values)
                code = Xbox360Values[Place]
                print( Xbox360[code] + ": " + str(Values[Place]))
            
while True:
        GetEvents()
        
        
        
        
