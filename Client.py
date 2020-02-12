import socket
import RPi.GPIO as GPIO
# set the user varibles
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
Pins = [33,35,7,11,13,15,16,18,29,31,37,32,38,40,5,12,36]
# Start the System --------------
# Start GPIO, Set the pins to be in board mode and set all pins to be output
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
GPIO.setwarnings(False)
for pin in Pins:
    GPIO.setup(pin, GPIO.OUT)

PWM0 = GPIO.PWM(Pins[0],1000)
PWM1 = GPIO.PWM(Pins[1],1000)
PWM2 = GPIO.PWM(Pins[3],1000)
PWM3 = GPIO.PWM(Pins[4],1000)
PWM4 = GPIO.PWM(Pins[15],1000)
PWM5 = GPIO.PWM(Pins[16],1000)


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    dataText = str(data, 'utf-8')

    DataArray = dataText.split(',')
    print(DataArray , end="\r" , flush=True)
    #PWM Left Joystick
    pin0.start(int(DataArray[0])/255 * 100)
    pin1.start(int(DataArray[1])/255 * 100)
    #PWM Triggers
    pin3.start(int(DataArray[3])/255 * 100)
    pin4.start(int(DataArray[4])/255 * 100)
    #PWM Right Joy Stick
    pin15.start(int(DataArray[15])/255 * 100)
    pin16.start(int(DataArray[16])/255 * 100)

    if DataArray[2] == 1:
        GPIO.output(Pins[2], GPIO.HIGH)
    else:
        GPIO.output(Pins[2], GPIO.LOW)

    if DataArray[5] == 1:
        GPIO.output(Pins[5], GPIO.HIGH)
    else:
        GPIO.output(Pins[5], GPIO.LOW)

    if DataArray[6] == 1:
        GPIO.output(Pins[6], GPIO.HIGH)
    else:
        GPIO.output(Pins[6], GPIO.LOW)

    if DataArray[7] == 1:
        GPIO.output(Pins[7], GPIO.HIGH)
    else:
        GPIO.output(Pins[7], GPIO.LOW)
    
    pin8.start(int(DataArray[8])/255 * 100)
    pin9.start(int(DataArray[9])/255 * 100)
    pin10.start(int(DataArray[10])/255 * 100)
    pin11.start(int(DataArray[11])/255 * 100)
    pin12.start(int(DataArray[12])/255 * 100)
    pin13.start(int(DataArray[13])/255 * 100)
    pin14.start(int(DataArray[14])/255 * 100)


def __del__(self):
        print("Status led is going offline")
        GPIO.cleanup()
