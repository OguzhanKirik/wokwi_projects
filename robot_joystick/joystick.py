from machine import ADC, Pin
import time


class Joystick:
    def __init__(self, xAxis: int, yAxis: int, button_pin: int, mode: str):
        # Write your code here
        self.h_axis = ADC(Pin(xAxis))
        self.v_axis = ADC(Pin(yAxis))
        self.button = Pin(button_pin, Pin.IN, Pin.PULL_UP)

        self.mode = mode
        self.last_state = "M"

        self.h_axis.atten(ADC.ATTN_11DB)
        self.v_axis.atten(ADC.ATTN_11DB)
        
        if self.mode == "interrupt":
            self.timer = Timer(-1)
            self.timer.init(period=100, mode=Timer.PERIODIC, callback=self._update_state)


    # This function reads the joystick and returns the joystick state:
    # L: left    R: Right    U: Up    D: Down    M: Middle
    def read(self):
        # Write your code here
        x_val = self.h_axis.read()
        y_val = self.v_axis.read()
        btn_val = self.button.value()

        if btn_val == 0:
            self.last_state = "M"
        elif x_val < 1000:
            self.last_state = "L"
        elif x_val > 3000:
            self.last_state = "R"
        elif y_val < 1000:
            self.last_state = "U"
        elif y_val > 3000:
            self.last_state = "D"
        else:
            self.last_state = "M"

        return self.last_state