from machine import Pin, PWM

class Servo:
    def __init__(self, pwm_pin: int, min_us=500, max_us=2500):
        self.pwm = PWM(Pin(pwm_pin), freq=50)
        self.min_us = min_us
        self.max_us = max_us
        self.angle = 90  # start at center
        self.goto(self.angle)


    def _angle_to_duty(self, angle):
        us = self.min_us + (self.max_us - self.min_us) * angle // 180
        duty = int(us * 1023 // 20000)  # convert microseconds to duty cycle
        return duty

    def goto(self, angle):
        angle = max(0, min(180, angle))  # limit angle to valid range
        self.angle = angle
        duty = self._angle_to_duty(angle)
        self.pwm.duty(duty)

    def left(self, delta=1):
        self.goto(self.angle - delta)

    def right(self, delta=1):
        self.goto(self.angle + delta)
