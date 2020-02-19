import socket
import RPi.GPIO as GPIO
# set the user varibles
UDP_IP = "192.168.1.160"
UDP_PORT = 5005
Pins = [33,35,7,11,13,15,16,18,29,31,37,32,38,40,5,12,36]
NON_PWM = [2,5,6,7,8,9,10,11,12,13,14]
# Start the System --------------
# Start GPIO, Set the pins to be in board mode and set all pins to be output
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
GPIO.setwarnings(False)
for pin in Pins:
    GPIO.setup(pin, GPIO.OUT)

PWM0 = GPIO.PWM(Pins[0],80)
PWM1 = GPIO.PWM(Pins[1],80)
PWM2 = GPIO.PWM(Pins[3],80)
PWM3 = GPIO.PWM(Pins[4],80)
PWM4 = GPIO.PWM(Pins[15],80)



sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    dataText = str(data, 'utf-8')

    DataArray = dataText.split(',')
    print(DataArray , end="\r" , flush=True)
    #PWM Left Joystick
    PWM0.start(int(DataArray[0])/255 * 9 + 5)
    PWM1.start(int(DataArray[1])/255 * 9 + 5)
    #PWM Triggers
    #break / Reverse
    forward = int(DataArray[4])
    reverse = int(DataArray[3])
    if reverse > forward:
        PWM2.start(int(DataArray[3])/255 * 9)
    else:
        PWM2.start(int(DataArray[4])/255 * 9)

    #PWM Right Joy Stick
    PWM3.start(int(DataArray[15])/255 * 9 + 5)
    PWM4.start(int(DataArray[16])/255 * 9 + 5)

    for NoPWM in NON_PWM:
        if DataArray[NoPWM] == 1:
            GPIO.output(Pins[NoPWM], GPIO.HIGH)
        else:
            GPIO.output(Pins[NoPWM], GPIO.LOW)





def __del__(self):
        print("Status led is going offline")
        GPIO.cleanup()
