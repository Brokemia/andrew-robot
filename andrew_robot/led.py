import serial

class LedController:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)

    def turn_on(self, led_number, power=255):
        self.set_power(led_number, power)

    def turn_off(self, led_number):
        self.set_power(led_number, 0)

    def set_power(self, led_number, power):
        self.ser.write(f'{led_number}{power:03}'.encode('ascii'))