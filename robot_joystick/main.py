print("Hello, ESP32!")
import machine
import time
from joystick import *
from servo import *

slide_switch = Pin(15, Pin.IN)

led1 = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)


joystick = Joystick(34, 35, 21, mode="polling")
button = Pin(21, Pin.IN, Pin.PULL_UP)


# Servo initialization
cam1_pan = Servo(13)
cam1_tilt = Servo(12)
cam2_pan = Servo(14)
cam2_tilt = Servo(27)


# Initial gain
gain = 1
button_last = 1  # for edge detection

def request_gain():
    global gain
    while True:
        try:
            user_input = input("Enter gain (1-10): ")
            value = int(user_input)
            if 1 <= value <= 10:
                gain = value
                print("Gain set to", gain)
                break
            else:
                print("Invalid gain. Please enter a number between 1 and 10.")
        except:
            print("Invalid input. Please enter a number between 1 and 10.")


while True:

    cam_selected = slide_switch.value()
    direction = joystick.read()

    if cam_selected == 1:
        led1.on()
        led2.off()
    else:
        led1.off()
        led2.on()
    time.sleep(0.01)
    
    button_now = Pin(21, Pin.IN, Pin.PULL_UP).value()
    if button_last == 1 and button_now == 0:  # falling edge
        request_gain()
    button_last = button_now

    # Move correct servos based on direction and camera
    if cam_selected:  # Camera 1
        if direction == "L":
            cam1_pan.left()
        elif direction == "R":
            cam1_pan.right()
        elif direction == "U":
            cam1_tilt.left()
        elif direction == "D":
            cam1_tilt.right()
    else:  # Camera 2
        if direction == "L":
            cam2_pan.left()
        elif direction == "R":
            cam2_pan.right()
        elif direction == "U":
            cam2_tilt.left()
        elif direction == "D":
            cam2_tilt.right()
#while True:
#    direction = joystick.read()
#    print("Joystick:", direction, "Button:", "Pressed" if button.value() == 0 else "Released")
#    time.sleep(0.2) 




