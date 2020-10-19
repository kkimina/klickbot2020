import socket
from enum import IntEnum
from time import sleep
import struct
import sys
from imagesearch import *
import time
import random
import requests
import csv
import winsound
from process import *
from telegram.ext import Updater
from telegram.ext import CommandHandler
from xbox_controll import *


DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 51914
regions = {
    'normal'                :[0,0,0,0,0],
    'abgelaufen'            :[0,0,0,0,0],
    'kaufen_yes'            :[0,0,0,0,0],
    'transfermarkt_found'   :[0,0,0,0,0],
    'transfermarkt_nix'     :[0,0,0,0,0],
    'gekauft'               :[0,0,0,0,0],
    'selling1'              :[0,0,0,0,0],
    'selling2'              :[0,0,0,0,0],
    'transfers'             :[0,0,0,0,0],
    'verbrauch'             :[0,0,0,0,0],
    'anbieten1'             :[0,0,0,0,0],
    'extended'              :[0,0,0,0,0],
    'extended_safe'         :[0,0,0,0,0],
}

blue     = [62 ,225, 237]
pink     = [250, 84,  97]
black_ok = [0, 0, 0]

lucas = {
    'normal'                :[0,0],
    'abgelaufen'            :[0,0],
    'kaufen_yes'            :[0,0],
    'transfermarkt_found'   :[0,0],
    'transfermarkt_nix'     :[0,0],
    'gekauft'               :[0,0],
    'selling1'              :[0,0],
    'selling2'              :[0,0],
    'transfers'             :[0,0],
    'verbrauch'             :[0,0],
    'anbieten1'             :[0,0],
    'extended'              :[0,0],
    'extended_safe'         :[0,0],
}


######## kann weg:
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

def send_message(ip, port, changes):
    packet = bytearray([0x01, len(changes)])  # type + axis count

    for axis, value in changes.items():
        # axis + value (network byte order)
        packet.extend(
            [axis, (value & 0xff000000) >> 24, (value & 0xff0000) >> 16, (value & 0xff00) >> 8, (value & 0xff)])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (ip, port))

def check_status(ip, port):
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


def press_button(button):
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
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    sleep(0.1)
    changes[button_default] = ButtonState.RELEASED
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    sleep(0.1)

def preissuche():
        press_button('left')
        press_button('y')

def preissuche_extend():
        sleep(2)
        press_button('down')
        sleep(1)
        press_button('a')
        press_button('down')
        press_button('left')
        press_button('y')

def calc_selling(anfang, sell_price):
    times = 0
    if sell_price <= 1100:
        times = int((sell_price - anfang) / 50)
    #print(times)
    return times

def make_price(anfang, sell_price):
    times = int(calc_selling(anfang, sell_price)) - 1
    for s in range(0, times):
        press_button('right')
        sleep(0.5)

def get_pixel_pink(x,y, command): #### -> get_pixel_color
    sicherheit = 0
    while 1:
        image = pyautogui.screenshot()
        image = np.array(image)

        coord2 = [x,y]
        color = pink
        if get_pixel_diff(image, coord2, color, 5):
            return
        else:
            if sicherheit < 10:
                if command != 'nix':
                    press_button(command)
                    sleep(1)
                sicherheit = sicherheit + 1
            else:
                print('pink ' + str(image[coord2[0], coord2[1], 0] - color[0]) + ',' +
                                str(image[coord2[0], coord2[1], 1] - color[0]) + ',' +
                                str(image[coord2[0], coord2[1], 2] - color[0]))



def preissuche_loop():
    for r in range(0, 50):
        sleep(1)
        if regions['transfermarkt_found'][0] != 0:
            new_extended()
            return 9
        else:
            ttt = suche_pics2('extended', 'normal')
            if ttt == 1:
                preissuche_extend()
                return 1
            elif ttt == 2:
                preissuche()
                return 2
    return 0


def get_pixel_diff(image, coord2, color, filter):
    if abs(int(image[coord2[0], coord2[1], 0]) - color[0]) < filter and abs(int(image[coord2[0], coord2[1], 1]) - color[1]) < filter and abs(int(image[coord2[0], coord2[1], 2]) - color[2]) < filter:
        return 1
    else:
        return 0


def suche_pics(find_img):
    start_time = time.time()
    precision = 0.9
    template = prepare_template(find_img)

    image = prepare_screenshot(find_img)
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1,-1]
    else:
        regions[find_img][0] = max_loc[0]
        regions[find_img][1] = max_loc[1]
        regions[find_img][2] = template.shape[1]
        regions[find_img][3] = template.shape[0]
        regions[find_img][4] = template
        cv2.imwrite('wrong_' + find_img + '.png', image)
    return max_loc


def prepare_template(find_img):
    if regions[find_img][4] is 0:
        #print('prepare ' + find_img)
        path = r'C:\Users\Kimi\Desktop'
        template = cv2.imread(path + r'\\' + find_img + '.png')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        #template = cv2.Canny(template, 50, 200)
        regions[find_img][4] = template
        return template#cv2.Canny(template, 50, 200)
    else:
        return regions[find_img][4]


def prepare_screenshot(find_img):
    if regions[find_img][0] == 0:
        image = pyautogui.screenshot()
    else:
        image = pyautogui.screenshot(region=(regions[find_img][0], regions[find_img][1], regions[find_img][2], regions[find_img][3]))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image#cv2.Canny(image, 50, 200)



def search_loop(pic):
    for r in range(0, 50):
        sleep(1)
        ttt = suche_pics(pic)
        if ttt[0] != -1:
            return 1
    return 0

def selling_new(anfang, sell_price):
    get_pixel_pink(regions['transfermarkt_found'][1] - 127, regions['transfermarkt_found'][0] + 534, 'down')
    press_button('lt')
    get_pixel_pink(regions['transfermarkt_found'][1] - 144, regions['transfermarkt_found'][0] + 519, 'up')
    sleep(0.5)
    make_price(anfang, sell_price)
    get_pixel_pink(regions['transfermarkt_found'][1] - 9, regions['transfermarkt_found'][0] + 590, 'up')


def new_extended():
    get_pixel_pink(regions['transfermarkt_found'][1]-29, regions['transfermarkt_found'][0]+135, 'down')
    get_pixel_grey(regions['transfermarkt_found'][1]-123, regions['transfermarkt_found'][0]+88,  'a', [140, 144, 146])
    get_pixel_blue(regions['transfermarkt_found'][1]+26, regions['transfermarkt_found'][0]+74, 'down')
    press_button('left')
    press_button('y')

def selling(anfang, sell_price):
    print(sell_price)
    press_button('x')
    test = search_loop('anbieten1')
    if test == 0:
        return 0
    selling_new(anfang, sell_price)
    sleep(1)
    press_button('a')
    sleep(2)
    press_button('a')
    sleep(2)
    press_button('b')

def kaufen2():
    press_button('a')
    get_pixel_pink(regions['transfermarkt_found'][1]-145, regions['transfermarkt_found'][0]+477, 'nix')
    sleep(0.1)
    changes = {XboxOneControls.DOWN: ButtonState.PRESSED}
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    sleep(0.1)
    changes = {XboxOneControls.A: ButtonState.PRESSED}
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    changes[XboxOneControls.DOWN] = ButtonState.RELEASED
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    sleep(0.05)
    changes[XboxOneControls.A] = ButtonState.RELEASED
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    sleep(0.1)

    changes = {XboxOneControls.UP: ButtonState.PRESSED}
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    sleep(0.05)
    changes = {XboxOneControls.A: ButtonState.PRESSED}
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    changes[XboxOneControls.UP] = ButtonState.RELEASED
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    sleep(0.05)
    changes[XboxOneControls.A] = ButtonState.RELEASED
    send_message(DEFAULT_IP, DEFAULT_PORT, changes)
    sleep(0.05)





def proof_kauf(price):
    for s in range(0, 50):
        nix = suche_pics2('gekauft', 'abgelaufen')
        if nix == 1:
            press_button('a')

            test = search_loop('selling1')
            sleep(3)
            if test is 0:
                test = search_loop('selling2')
                if test is 0:
                    return 0

            test = selling(150, price)
            if test == 0:
                return 0

            press_button('a')
            return 1

        elif nix == 2:
            press_button('a')
            sleep(3)
            press_button('b')
            sleep(3)
            press_button('b')
            return 2
        sleep(1)
    print('mhm')
    return 0





def suche_pixel():
    for r in range(0, 5000):
        sleep(1)
        ttt = suche_pics('transfermarkt_found')
        if ttt[0] != -1:
            pyautogui.moveTo((ttt[0]+1), (ttt[1]+1))
            pyautogui.moveTo((ttt[0] + 100), (ttt[1] - 50))
            pyautogui.moveTo((ttt[0]), (ttt[1] + 10))
            print(str(ttt[0] + 300) + ',' + str(ttt[1] - 50))
            print(str(ttt[0] + 300) + ',' + str(ttt[1] - 180))
            print('found')
            break
        else:
            print('nix')





def get_pixel_blue(x,y, command):
    sicherheit = 0
    while 1:
        image = pyautogui.screenshot()
        image = np.array(image)

        coord2 = [x,y]
        color = blue
        if get_pixel_diff(image, coord2, color, 5):
            return
        else:
            if sicherheit < 10:
                sleep(1)
                press_button(command)
                sicherheit = sicherheit + 1
            else:
                print('blue ' + str(image[coord2[0], coord2[1], 0] - color[0]) + ',' +
                             str(image[coord2[0], coord2[1], 1] - color[0]) + ',' +
                             str(image[coord2[0], coord2[1], 2] - color[0]))
                return 0



def get_pixel_grey(x,y, command, color):
    sicherheit = 0
    while 1:
        image = pyautogui.screenshot()
        image = np.array(image)

        coord2 = [x,y]
        if get_pixel_diff(image, coord2, color, 10):
            return
        else:
            if sicherheit < 10:
                sleep(1)
            if sicherheit == 0:
                press_button(command)
                sicherheit = sicherheit + 1
            else:
                print('grey ' + str(image[coord2[0], coord2[1], 0] - color[0]) + ',' +
                        str(image[coord2[0], coord2[1], 1] - color[0]) + ',' +
                        str(image[coord2[0], coord2[1], 2] - color[0]))


def region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2]-x1
    height = region[3]-y1
    return pyautogui.screenshot(region=(x1,y1,width,height))







def find_one_pic(find_img):
    precision = 0.9
    template = prepare_template(find_img)
    image    = prepare_screenshot(find_img)
    res1 = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)
    if max_val > precision:
        if regions[find_img][0] is 0:
            regions[find_img][0] = max_loc[0]
            regions[find_img][1] = max_loc[1]
            regions[find_img][4] = template
            regions[find_img][2] = template.shape[1]
            regions[find_img][3] = template.shape[0]

        cv2.imwrite('wrong_'+find_img +'.png', image)
        return 1

    else:
        #cv2.imshow(find_img, template)
        #cv2.imshow('image '+find_img, image)
        #cv2.waitKey()
        return -1

def suche_pics2_neu(find_img1, find_img2):
    if find_one_pic(find_img1) == 1:
        return 1
    elif find_one_pic(find_img2) == 1:
        return 2
    else:
        return 0

def suche_pics2(find_img1, find_img2):
    precision = 0.9
    template1 = prepare_template(find_img1)
    template2 = prepare_template(find_img2)

    image1 = prepare_screenshot(find_img1)
    image2 = prepare_screenshot(find_img2)

    res2 = cv2.matchTemplate(image2, template2, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
    if max_val > precision:
        if regions[find_img2][0] is 0:
            regions[find_img2][0] = max_loc[0]
            regions[find_img2][1] = max_loc[1]
            regions[find_img2][4] = template2
            regions[find_img2][2] = template2.shape[1]
            regions[find_img2][3] = template2.shape[0]
        cv2.imwrite('wrong_' + find_img2 + '.png', image2)
        #print("--- %s seconds ---" % (time.time() - start_time))
        return 2

    res1 = cv2.matchTemplate(image1, template1, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)
    if max_val > precision:
        #print('found2')
        if regions[find_img1][0] is 0:
            regions[find_img1][0] = max_loc[0]
            regions[find_img1][1] = max_loc[1]
            regions[find_img1][4] = template1
            regions[find_img1][2] = template1.shape[1]
            regions[find_img1][3] = template1.shape[0]
            cv2.imwrite('wrong_' + find_img1 + '.png', image1)
        #print("--- %s seconds ---" % (time.time() - start_time))
        return 1
    return 0



##### bleibt





def lucas_kanade(low_threshold):
    # params for ShiTomasi corner detection
    feature_params = dict(maxCorners=5000,
                          qualityLevel=0.01,
                          minDistance=1,
                          blockSize=10)

    # Parameters for lucas kanade optical flow
    lk_params = dict(winSize=(10, 10),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    im = region_grabber(region=(1030, 0, 1843, 510))
    im = np.array(im)
    gray_frame_old = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray_frame_old = cv2.Canny(gray_frame_old, low_threshold, low_threshold*3)
    p0 = cv2.goodFeaturesToTrack(gray_frame_old, mask=None, **feature_params)

    for n in range(0,500000):
        mask = np.zeros_like(gray_frame_old)
        im2 = region_grabber(region=(1030, 0, 1843, 510))
        im2 = np.array(im2)
        frame_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        frame_gray =cv2.Canny(frame_gray, low_threshold, low_threshold*3)

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(gray_frame_old, frame_gray, p0, None, **lk_params)

        # Select good points
        good_new = p1#[st==1]
        good_old = p0#[st==1]
        diff = (good_new-good_old)/2
        print(np.sum(np.absolute(diff))/diff.shape[0])
        # draw the tracks
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv2.line(mask, (a, b), (c, d), (255,255,255), 2)

        cv2.imshow('frame', mask)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points
        #gray_frame_old = frame_gray.copy()
        #p0 = good_new.reshape(-1, 1, 2)


class status():
    def __init__(self):
        self.cards     = 0
        self.insgesamt = 0
        self.verkauf   = 0
        self.price     = 900
        self.run       = 'OFF'

    def getdata(self):
        try:
            with open('persons.csv', 'w') as csvfile:
                output = requests.get('https://www.fifacoin.com/sell?platform=xboxone&dt=cash/').text

                if output.__contains__(
                        'There are not any players available now, please click Reload a few minutes later') is False:
                    self.verkauf = 'Verkauf möglich'
                else:
                    self.verkauf = 'Verkauf unmoeglich'
                print(self.verkauf)
        except:
            print('error by ')

    def searchingbegin(self, price):
        for s in range(0, 500):
            for n in range(0, 10):
                if self.run is 'ON':
                    if preissuche_loop() == 0:
                        telegram_bot_sendtext('seltsam_preissuche_loop')
                        print('seltsam_preissuche_loop')
                        return
                    gotIt = transfermarkt_loop(price)
                    if gotIt == 1:
                        self.cards = self.cards + 1
                        self.insgesamt = self.insgesamt + 1
                        print(str(self.cards) + " von (" + str(self.insgesamt) + ")")
                        telegram_bot_sendtext(str(self.cards) + " von (" + str(self.insgesamt) + ") = " + str(0.00378*int(self.cards)) + '€')
                    elif gotIt == 2:
                        self.insgesamt = self.insgesamt + 1
                        print(str(self.cards) + " von (" + str(self.insgesamt) + ")")
                        telegram_bot_sendtext(str(self.cards) + " von (" + str(self.insgesamt) + ") = " + str(0.00378*int(self.cards)) + '€')
                    elif gotIt == -1:
                        # print('nothing found')
                        sleep(0.05)
                    elif gotIt == 0:
                        print('seltsam')
                        telegram_bot_sendtext('seltsam')
                        return
            self.getdata()
            sleep(random.randint(10, 20))
        telegram_bot_sendtext('BOT ENDE')
        print('BOT_ENDE')


    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

    def printscreen(self,update, context):
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def left(self, update, context):
        press_button('left')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def up(self, update, context):
        press_button('up')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def right(self, update, context):
        press_button('right')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def down(self, update, context):
        press_button('down')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def rt(self, update, context):
        press_button('rt')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def lt(self, update, context):
        press_button('lt')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def a(self, update, context):
        press_button('a')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def y(self, update, context):
        press_button('y')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def x(self, update, context):
        press_button('x')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def b(self, update, context):
        press_button('b')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def other_bot(self):
        updater = Updater(token='1091873086:AAG3Zas2Tx3egjq0odjx8aydt3fkfsbpHWA', use_context=True)
        start_handler = CommandHandler('start', self.unknown)
        printscreen_handler = CommandHandler('printscreen', self.printscreen)
        up_handler      = CommandHandler('up', self.up)
        down_handler    = CommandHandler('down', self.down)
        right_handler   = CommandHandler('right', self.right)
        left_handler    = CommandHandler('left', self.left)
        rt_handler      = CommandHandler('rt', self.rt)
        lt_handler      = CommandHandler('lt', self.lt)
        a_handler = CommandHandler('a', self.a)
        b_handler = CommandHandler('b', self.b)
        y_handler = CommandHandler('y', self.y)
        x_handler = CommandHandler('x', self.x)

        dispatcher = updater.dispatcher
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(printscreen_handler)
        dispatcher.add_handler(up_handler)
        dispatcher.add_handler(down_handler)
        dispatcher.add_handler(right_handler)
        dispatcher.add_handler(left_handler)
        dispatcher.add_handler(rt_handler)
        dispatcher.add_handler(lt_handler)
        dispatcher.add_handler(a_handler)
        dispatcher.add_handler(b_handler)
        dispatcher.add_handler(y_handler)
        dispatcher.add_handler(x_handler)
        updater.start_polling()
        updater.idle()


    def main2(self):
        ip = DEFAULT_IP
        port = DEFAULT_PORT

        if check_status(ip, port):
            sys.exit(-1)
        self.getdata()
        #new_extended()
        telegram_bot_sendtext('START BOT')
        #self.other_bot()
        print('START BOT')
        #pixel_compare([352, 1371], [515, 1263], pink, black_ok)
        self.searchingbegin(self.price)


def get_pixel_color(x,y):
    while 1:
        image = pyautogui.screenshot()
        image = np.array(image)

        coord2 = [x,y]
        color = [72,104,33]
        if get_pixel_diff(image, coord2, color, 5):
            print('gruen')
            return
        elif get_pixel_diff(image, coord2, [128,31,36], 5):
            print('rot')
        else:
            #print(str(image[coord2[0], coord2[1], 0] - color[0]) + ',' +
            #                 str(image[coord2[0], coord2[1], 1] - color[0]) + ',' +
            #                 str(image[coord2[0], coord2[1], 2] - color[0]))

            print('pink ' + str(image[coord2[0], coord2[1], 0]) + ',' +
                  str(image[coord2[0], coord2[1], 1]) + ',' +
                  str(image[coord2[0], coord2[1], 2]))

#get_pixel_color(512,690)