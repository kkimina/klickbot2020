from enum import IntEnum
import socket
from time import sleep
import struct
import sys
from calculations import *


DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 51914

class XboxOneControls(IntEnum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3
    VIEW = 128
    MENU = 129
    GUIDE = 130
    UP = 131
    RIGHT = 132
    DOWN = 133
    LEFT = 134
    Y = 135
    B = 136
    A = 137
    X = 138
    LB = 139
    RB = 140
    LT = 141
    RT = 142
    LS = 143
    RS = 144


class ButtonState(IntEnum):
    RELEASED = 0
    PRESSED = 255


class XBOX_CONTROL():
    def __init__(self):
        self.status = 'init'
        self.ip = DEFAULT_IP
        self.port = DEFAULT_PORT
        self.get_out = 0

    def run(self):
        if self.check_status(self.ip, self.port):
            sys.exit(-1)

    def send_message(self, ip, port, changes):
        if self.get_out is 1:
            return 'get_out'
        packet = bytearray([0x01, len(changes)])  # type + axis count

        for axis, value in changes.items():
            packet.extend(
                [axis, (value & 0xff000000) >> 24, (value & 0xff0000) >> 16, (value & 0xff00) >> 8, (value & 0xff)])

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(packet, (ip, port))

    def check_status(self, ip, port):
        packet = bytearray([0x00, 0x00])
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((ip, port))
        sock.send(packet)
        timeval = struct.pack('ll', 1, 0)  # seconds and microseconds
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
        try:
            data, (address, port) = sock.recvfrom(2)
            response = bytearray(data)
            if (response[0] != 0x00):
                print("Invalid reply code: {0}".format(response[0]))
                return 1
        except socket.error as err:
            print(err)

        return 0

    def press_button(self, button):
        if self.get_out is 1:
            return 'get_out'
        button_default = XboxOneControls.GUIDE

        if button == 'a':
            button_default = XboxOneControls.A
        elif button == 'y':
            button_default = XboxOneControls.Y
        elif button == 'down':
            button_default = XboxOneControls.DOWN
        elif button == 'up':
            button_default = XboxOneControls.UP
        elif button == 'left':
            button_default = XboxOneControls.LEFT
        elif button == 'right':
            button_default = XboxOneControls.RIGHT
        elif button == 'b':
            button_default = XboxOneControls.B
        elif button == 'x':
            button_default = XboxOneControls.X
        elif button == 'lt':
            button_default = XboxOneControls.LT
        elif button == 'rt':
            button_default = XboxOneControls.RT
        elif button == 'rb':
            button_default = XboxOneControls.RB
        elif button == 'lb':
            button_default = XboxOneControls.LB

        changes = {button_default: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.1)
        changes[button_default] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.1)

    def preissuche(self):
        if self.get_out is 1:
            return 'get_out'
        self.press_button('left')
        self.press_button('y')

    def take_old_prices(self):
        path = r'C:\Users\Kimi\Desktop\klickbot'
        f = open(path+'\price.txt', 'w')


    def preissuche_extend(self):
        if self.get_out is 1:
            return 'get_out'
        sleep(2)
        self.press_button('down')
        sleep(1)
        self.press_button('a')
        sleep(1)
        self.press_button('down')
        self.press_button('left')
        self.press_button('y')

    def make_price(self,anfang, sell_price):
        if self.get_out is 1:
            return 'get_out'
        rest = 0
        if sell_price > 650:
            self.press_button('rb')
            sleep(1)
            rest = 650
        if sell_price > 1300:
            self.press_button('rb')
            sleep(1)
            rest = 1300
        if sell_price > 2300:
            self.press_button('rb')
            sleep(1)
            rest = 2300
        if sell_price > 3300:
            self.press_button('rb')
            sleep(1)
            rest = 3300
        if sell_price > 4300:
            self.press_button('rb')
            sleep(1)
            rest = 4300

        times = int(calc_selling(sell_price, rest)) - 1
        for s in range(0, times):
            self.press_button('right')
            sleep(1)

    def make_price_search(self, anfang, sell_price):
        if self.get_out is 1:
            return 'get_out'
        rest = 0
        if sell_price > 650:
            self.press_button('rb')
            sleep(1)
            rest = 650
        if sell_price > 1300:
            self.press_button('rb')
            sleep(1)
            rest = 1300
        if sell_price > 2300:
            self.press_button('rb')
            sleep(1)
            rest = 2300
        if sell_price > 3300:
            self.press_button('rb')
            sleep(1)
            rest = 3300
        if sell_price > 4300:
            self.press_button('rb')
            sleep(1)
            rest = 4300


        times = int(calc_selling(sell_price, rest))
        for s in range(0, times):
            self.press_button('right')
            sleep(1)

    def kaufen2(self, bot,  imagebot):
        if self.get_out is 1:
            return 'get_out'


        changes = {XboxOneControls.A: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes[XboxOneControls.A] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes = {XboxOneControls.DOWN: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes = {XboxOneControls.A: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes[XboxOneControls.DOWN] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes[XboxOneControls.A] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.1)

        changes = {XboxOneControls.UP: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes = {XboxOneControls.A: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        changes[XboxOneControls.UP] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes[XboxOneControls.A] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)

    def kaufen3(self):
        if self.get_out is 1:
            return 'get_out'
        changes = {XboxOneControls.A: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        changes[XboxOneControls.DOWN] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes[XboxOneControls.A] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.1)

        changes = {XboxOneControls.UP: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes = {XboxOneControls.A: ButtonState.PRESSED}
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        changes[XboxOneControls.UP] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)
        changes[XboxOneControls.A] = ButtonState.RELEASED
        self.send_message(DEFAULT_IP, DEFAULT_PORT, changes)
        sleep(0.05)




