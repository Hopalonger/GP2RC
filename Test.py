"""Simple example showing how to get gamepad events."""

#Varaibles for Packets
from __future__ import print_function
from inputs import get_gamepad
from nrf24 import NRF24
import time
Xbox360 = [ "LeftJoyX","LeftJoyY", "LeftJoyClick" , "LeftTrig", "RightTrig", "RightBump","LeftBump","XboxButton","StartButton","MenuButton","XButton","YButton" ,"AButton","BButton" ,"DpadUp","DpadDown" ,"DpadLeft","DpadRight","RightJoyX","RightJoyY","RightJoyClick"]
Xbox360Values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

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

def main():
    """Just print out some event infomation when the gamepad is used."""
    while 1:
        events = get_gamepad()
        for event in events:
            prin(event.ev_type, event.code, event.state)
            if (event.ev_type == "Absolute"):
                if(event.ev_type == "ABS_X"):
                    LeftJoyX = event.state
                 elif(event.ev_type == "ABS_Y"):
                    LeftJoyY == event.state
                 

def ResetVarible():
    #Varibles For Packets 0 = off 1 = on
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
 

if __name__ == "__main__":
    main()
    ResetVarible()
