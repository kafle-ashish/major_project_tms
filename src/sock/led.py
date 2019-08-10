from gpiozero import LED
import time


class Led:
    def __init__(self, pin):
        self.pin = pin
        self.led = LED(self.pin)

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()

    def active(self):
        return self.led.is_active
