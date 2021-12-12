import inputs
from inputs import get_gamepad
import RPi.GPIO as GPIO  # import gpio
import time      #import time library
import spidev
from lib_nrf24 import NRF24

GPIO.setmode(GPIO.BCM)       # set the gpio mode


JoySticks = ['ABS_Y','ABS_X','ABS_RX','ABS_RY']
Triggers = ['ABS_Z','ABS_RZ']
PacketCodes=['ABS_Y','ABS_X','ABS_RX','ABS_RY','ABS_Z','ABS_RZ','BTN_START','BTN_SELECT']
Packet = [0,0,0,0,0,0,0,0]

print( "Starting Transmitter")

# set the pipe address. this address shoeld be entered on the receiver alo
pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]
radio = NRF24(GPIO, spidev.SpiDev())   # use the gpio pins
radio.begin(0, 25)   # start the radio and set the ce,csn pin ce= GPIO08, csn= GPIO25
radio.setPayloadSize(32)  #set the payload size as 32 bytes
radio.setChannel(0x76) # set the channel as 76 hex
radio.setDataRate(NRF24.BR_1MBPS)    # set radio data rate
radio.setPALevel(NRF24.PA_MIN)  # set PA level

radio.setAutoAck(True)       # set acknowledgement as true
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])     # open the defined pipe for writing
radio.printDetails()      # print basic detals of radio

print("Transmitter Started, Ready To Send")

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
            if event.code in PacketCodes:
                Place = PacketCodes.index(event.code)
                if event.code in JoySticks:
                    NewValue = (((event.state - -32762) * 255 )/ 65534)
                    Packet[Place] = round(NewValue)
                elif event.code in Triggers:
                    Packet[Place] = event.state
                else:
                    if event.state == 1:
                        Packet[Place] = 255
                    else:
                        Packet[Place] = event.state


# Create A nice user readout of the system working
# also calculates the time from starting each Loop to time that it takes to end each loop
def PrintScreen():
    After = datetime.datetime.now()
    TimeDiffrence = After - Now
    TimeDiffrence_ms = TimeDiffrence.total_seconds() * 1000
    Latency  = (str(TimeDiffrence_ms)[:5] + '..') if len(str(TimeDiffrence_ms)) > 5 else str(TimeDiffrence_ms)
    print(str(Packet)[1:-1] + " Latency: " + Latency + " (ms)                   "  , end="\r", flush=True)

def UDP():
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.sendto(str.encode(str(Packet)[1:-1]), (CLIENT_IP, UDP_PORT))
def Transmit():
    sendMessage = list(str(Packet)[1:-1])  #the message to be sent
    while len(sendMessage) < 32:
        sendMessage.append(0)

    start = time.time()      #start the time for checking delivery time
    radio.write(sendMessage)   # just write the message to radio
    print("Sent the Packet: {}".format(sendMessage))  # print a message after succesfull send
    radio.startListening()        # Start listening the radio

    while not radio.available(0):
        time.sleep(1/100)
        if time.time() - start > 2:
            print("Timed out.")  # print errror message if radio disconnected or not functioning anymore
            break

while True:
    #Now = datetime.datetime.now()
    GetEvents()
    #PrintScreen()
    Transmit()
