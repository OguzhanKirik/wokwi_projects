from machine import Pin, I2C,SoftI2C
from time import sleep
from buzzer import *
from stepper import *
from hcsr04 import *
from oled import I2C
from mpu6050 import accel

print("Hello, ESP32 is Ready!")
oled_width = 128
oled_height = 64
# --- Constants ---
STEPS_PER_REV = 200
WHEEL_CIRCUMFERENCE_CM = 18.84
STEPS_PER_CM = STEPS_PER_REV / WHEEL_CIRCUMFERENCE_CM  # ~10.62



# --- I2C setup ---
i2c = SoftI2C(scl = Pin(22), sda = Pin(21))
# --- Button, Buzzer, LED ---
led = Pin(12, Pin.OUT)
button = Pin(27, Pin.IN, Pin.PULL_UP)
buzzer = Buzzer(15)

## Stepper Setup
stepper1 = Stepper(13)
stepper2 = Stepper(19)

# --- OLED, Ultrasonic, Accelrometer setup ---
ultrasonic = HCSR04(trigger_pin=5, echo_pin=18)

oled = I2C(oled_width, oled_height, i2c)

#oled = oled.ssd1306.SSD1306_I2C(128, 64, i2c)
mpu = accel(i2c)



# Function to calculate number of steps for given distance
def get_steps_from_distance(distance_cm):
    return int(distance_cm * STEPS_PER_CM)


def beep(count=1, duration=0.1, pause=0.1):
    for _ in range(count):
        buzzer.beep_once()
        sleep(duration)


def wait_button_press():
    while button.value() == 1:  # Wait until button is pressed
        sleep(0.1)
    return

# --- Main Loop ---
while True:
    led.off()

    # Show idle message
    oled.fill(0)
    oled.text("Press button", 0, 0)
    oled.text("to start", 0, 10)
    oled.show()

    # Wait for button press
    wait_button_press()

    # Beep once to confirm start
    beep(1)

    # Read distance
    try:
        distance = ultrasonic.distance_cm()
    except Exception:
        distance = 0

    # Calculate steps
    steps = get_steps_from_distance(distance)

    # Display info
    oled.fill(0)
    oled.text("Distance: {:.1f}cm".format(distance), 0, 0)
    oled.text("Steps: {}".format(steps), 0, 10)
    oled.show()

    reached = True

    # Set motor direction forward
    #stepper1.value(1)
    #stepper2.value(1)

    for _ in range(steps):
        stepper1.move_one_step()
        stepper2.move_one_step()
        
        # Read accelerometer Y axis
        values = mpu.get_values()
        acy = values["AcY"]

        if acy > 12000 or acy < -12000:
            reached = False
            break

    oled.fill(0)

    if reached:
        oled.text("REACHED", 0, 0)
        oled.show()
        beep(1)
    else:
        warning_led.on()
        oled.text("TILTED", 0, 0)
        oled.show()
        beep(3, 0.1, 0.2)

    sleep(3)