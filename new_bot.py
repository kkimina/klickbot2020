from time import *
from xbox_controll import XBOX_CONTROL
from computer_vision import imagebot
from telegrams import TGRAMS
import random
import sys
import datetime


from imagesearch import *


class XBOX_BOT():

    def __init__(self):
        self.proof_loop =   {
                                'ok'                 : '2',
                                'ok2'                : '2',
                                'ok3'                : '2',
                                'abgelaufen'         : '2',
                                'gekauft'            : '1',
                            }
        self.status         = 'init'
        self.run            = 'ON'
        self.cards          = 0
        self.transfermarkt  = 0
        self.insgesamt      = 0
        self.verkauf        = 0
        self.price          = 900
        self.new_price      = 900
        self.confirm_price  = 900
        self.buy_price      = 900
        self.card_price     = 900
        self.xbox_cmd       = 0
        self.vision         = 0
        self.tele           = 0
        self.stoerung       = 0
        self.get_out        = 0
        self.full           = 0
        self.last_price     = 0
        self.sum            = 0
        self.gesamt_coins_  = 0
        self.coinselling    = 'OFF'
        self.solver         = 'ON'


    def start(self):
        self.xbox_cmd   = XBOX_CONTROL()
        self.xbox_cmd.run()

        self.vision     = imagebot(self.xbox_cmd)
        self.tele       = TGRAMS()

        self.tele.telegram_bot_sendtextSTATUS('START-BOT')
        self.searchingbegin()




    def preissuche_loop(self):
        sicherheit = 0
        while 1:
            if self.get_out is 1:
                return 'get_out'
            sleep(1)
            if self.vision.regions['transfermarkt_found'][0] != 0:
                self.new_extended()
                return 9
            else:
                ttt = self.vision.suche_pics2(self, 'extended', 'normal')
                if ttt == 1:
                    self.xbox_cmd.preissuche_extend()
                    return 1
                elif ttt == 2:
                    self.xbox_cmd.preissuche()
                    return 2
                else:
                    if sicherheit < 50:
                        sicherheit = sicherheit + 1
                    else:
                        self.stoerung = 1

        return 0

    def getCalibX(self, old_x):
        if self.get_out is 1:
            return 'get_out'
        return self.vision.regions['transfermarkt_found'][1] + old_x

    def getCalibY(self, old_y):
        if self.get_out is 1:
            return 'get_out'
        return self.vision.regions['transfermarkt_found'][0] + old_y


    def read_transfermarket(self):
        objekt_string = self.vision.tess(self, [self.getCalibY(+668), self.getCalibX(-246), 106, 39])
        if objekt_string.__contains__('/100 Objekte'):
            objekt_string = objekt_string.replace('/100 Objekte', '')
            self.transfermarkt = int(self.replace_string(objekt_string))
            if self.transfermarkt > 90:
                self.tele.telegram_bot_sendtext('TRANSFERMARKT FULL: ' + str(self.transfermarkt))

    def set_price(self):
        if self.get_out is 1:
            return 'get_out'
        while 1:
                stringi = self.vision.tess(self, self.gesamt_coins)
                print(stringi)
                print(self.replace_string(stringi))
                get_search_price = int(self.replace_string(stringi))
                if get_search_price < self.buy_price:
                    self.xbox_cmd.press_button('right')
                elif get_search_price > self.buy_price:
                    self.xbox_cmd.press_button('left')
                else:
                    print(1)
                    pass


    def selling_new(self, anfang):
        if self.get_out is 1:
            return 'get_out'
        self.vision.get_pixel_color(self, self.getCalibX(-127), self.getCalibY(534), self.xbox_cmd, 'down', self.vision.pink, 0)
        self.xbox_cmd.press_button('lt')
        self.vision.get_pixel_color(self, self.getCalibX(- 144), self.getCalibY(519), self.xbox_cmd, 'up', self.vision.pink, 0)
        sleep(0.5)
        self.xbox_cmd.make_price(anfang, self.price)
        try:
            self.last_price = int(self.replace_string(self.vision.tess(self, [self.vision.regions['transfermarkt_found'][0] + 611, self.vision.regions['transfermarkt_found'][1] - 84, 34, 15])))
            self.sum = self.sum + self.price * 0.95 - self.last_price
        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass


        self.vision.get_pixel_color(self, self.getCalibX(-9), self.getCalibY(590), self.xbox_cmd, 'up', self.vision.pink, 0)


    def replace_string(self, txt):
        txt = txt.replace('°','')
        txt = txt.replace('.', '')
        txt = txt.replace('@', '')
        txt = txt.replace(' ', '')
        txt = txt.replace('¢', '')
        txt = txt.replace('«', '')
        txt = txt.replace(',', '')
        txt = txt.replace('{', '')
        txt = txt.replace('}', '')
        txt = txt.replace('|', '')
        txt = txt.replace(';', '')
        return txt

    def empty_transfermarket(self):
        self.xbox_cmd.press_button('b')
        sleep(5)
        self.vision.get_pixel_color(self, self.getCalibX(+36), self.getCalibY(+264), self.xbox_cmd, 'down', self.vision.pink)
        sleep(3)
        self.xbox_cmd.press_button('a')
        sleep(5)
        self.xbox_cmd.press_button('lt')
        sleep(5)
        self.xbox_cmd.press_button('rt')
        sleep(5)
        self.xbox_cmd.press_button('up')
        sleep(5)
        self.xbox_cmd.press_button('a')
        sleep(5)
        self.xbox_cmd.press_button('b')
        sleep(5)
        self.vision.get_pixel_color(self, self.getCalibX(-182), self.getCalibY(+745), self.xbox_cmd, 'up', self.vision.pink)
        self.xbox_cmd.press_button('a')
        sleep(5)

    def new_extended(self):
        if self.get_out is 1:
            return 'get_out'
        if self.transfermarkt > 90:
            self.empty_transfermarket()
            self.transfermarkt = 0
        self.make_new_price()
        self.vision.get_pixel_color(self, self.getCalibX(-29), self.getCalibY(135), self.xbox_cmd, 'down', self.vision.pink, 0)

        self.vision.get_pixel_color(self, self.getCalibX(-123), self.getCalibY(88), self.xbox_cmd, 'a', [140, 144, 146], 0)

        self.vision.get_pixel_color(self, self.getCalibX(26), self.getCalibY(74), self.xbox_cmd, 'down', self.vision.blue, 0)
        self.xbox_cmd.press_button('left')
        try:
            stringi = self.vision.tess(self, [self.getCalibY(+63), self.getCalibX(-269), 35, 15])
            self.gesamt_coins_ = int(self.replace_string(stringi))
        except:
            #print("Unexpected error:", sys.exc_info()[0])
            #print(stringi)
            pass
        self.xbox_cmd.press_button('y')

    def make_new_price(self):
        if self.new_price == self.confirm_price:
            return
        else:
            self.confirm_price = self.new_price

        if self.get_out is 1:
            return 'get_out'
        self.vision.get_pixel_color(self, self.getCalibX(-29), self.getCalibY(135), self.xbox_cmd, 'down', self.vision.pink, 0)
        self.vision.get_pixel_color(self, self.getCalibX(-123), self.getCalibY(88), self.xbox_cmd, 'a', [140, 144, 146], 0)
        self.vision.get_pixel_color(self, self.getCalibX(85), self.getCalibY(90), self.xbox_cmd, 'down', self.vision.blue, 0)

        self.xbox_cmd.press_button('lt')
        sleep(1)
        self.xbox_cmd.make_price_search(150, self.new_price)


    def selling(self, anfang):
        if self.get_out is 1:
            return 'get_out'
        self.xbox_cmd.press_button('x')
        self.vision.search_loop(self, 'anbieten1')
        self.selling_new(anfang)
        sleep(1)
        self.xbox_cmd.press_button('a')
        #self.vision.ok_while(self)
        sleep(2)
        self.xbox_cmd.press_button('a')
        sleep(2)
        self.xbox_cmd.press_button('b')


    def transfermarkt_loop(self):
        gotIt = 0
        for s in range(0, 50):
            if self.get_out is 1:
                return 'get_out'

            if self.vision.regions['transfermarkt_found'][0] == 0:
                nix = self.vision.suche_pics2(self, 'transfermarkt_nix', 'transfermarkt_found')
            else:
                nix = self.vision.pixel_compare(self,
                                    [self.getCalibX(-41),self.getCalibY(350)],
                                    [self.getCalibX(14),self.getCalibY(56)], self.vision.pink,
                                                                             self.vision.dark_grey, 10, 10)

            if nix == 2:
                self.vision.waitKaufsignal(self)
                self.xbox_cmd.kaufen2(self, self.vision)
                gotIt = self.proof_kauf()
                break
            elif nix == 1:
                gotIt = -1
                self.xbox_cmd.press_button('a')
                break
            elif nix == -1:
                return 0
        return gotIt

    def proof_kauf(self):
        sicherheit = 0
        while 1:
            if self.get_out is 1:
                return 'get_out'
            #nix = self.vision.suche_pics2(self, 'gekauft', 'abgelaufen')
            nix = self.vision.suche_pics_loop(self, self.proof_loop)
            sleep(1)
            if nix == 1:
                self.xbox_cmd.press_button('a')
                sicherheit = 0

                while 1:
                    if self.get_out is 1:
                        return 'get_out'
                    test = self.vision.suche_pics2(self, 'selling1', 'selling2')
                    if test is 1 or test is 2:
                        self.read_transfermarket()
                        break
                    else:
                        sleep(1)
                        sicherheit = sicherheit + 1
                        if sicherheit > 50:
                            self.stoerung = 1
                test = self.selling(150)
                if test == 0:
                    return 0
                #self.vision.ok_while(self)
                self.xbox_cmd.press_button('a')
                return 1


            elif nix == 2:
                self.xbox_cmd.press_button('a')
                sleep(3)
                self.xbox_cmd.press_button('b')
                sleep(3)
                self.xbox_cmd.press_button('b')
                return 2

            sleep(0.5)
            sicherheit = sicherheit + 1
            if sicherheit > 50:
                self.stoerung = 1
        print('mhm')
        return 0

    def searchingbegin(self):
        while 1:
            for n in range(0, 10):
                starttime = time.clock()
                if self.get_out is 1:
                    self.get_out            = 0
                    self.vision.get_out     = 0
                    self.xbox_cmd.get_out   = 0
                    self.stoerung           = 0
                elif self.run is 'ON':
                    if self.preissuche_loop() == 0:
                        self.tele.telegram_bot_sendtext('seltsam_preissuche_loop')
                        print('seltsam_preissuche_loop')
                        return
                    gotIt = self.transfermarkt_loop()
                    if gotIt == 1:
                        self.cards = self.cards + 1
                        self.insgesamt = self.insgesamt + 1
                        print(str(self.cards) + " von (" + str(self.insgesamt) + ")")

                        self.tele.telegram_bot_sendtextSTATUS(str(self.cards) + " von (" + str(self.insgesamt) + ") " + str(int(self.sum)) + ' Coins (' +str(round(self.sum*self.card_price/10000, 4))  + ' €)  Insgesamt:' + str(int(self.gesamt_coins_)) + '   TM:'+ str(self.transfermarkt))
                    elif gotIt == 2:
                        self.insgesamt = self.insgesamt + 1
                        print(str(self.cards) + " von (" + str(self.insgesamt) + ")")
                        self.tele.telegram_bot_sendtextSTATUS(str(self.cards) + " von (" + str(self.insgesamt) + ") " + str(int(self.sum)) + ' Coins (' +str(round(self.sum*self.card_price/10000, 4))  + ' €)  Insgesamt:' + str(int(self.gesamt_coins_)) + '   TM:'+ str(self.transfermarkt))
                    elif gotIt == -1:
                        sleep(0.05)
            if (time.clock() - starttime) < 40 and self.run is 'ON':
                sleep(random.randint(35, 45))
            else:
                sleep(random.randint(10, 20))
        print('BOT_ENDE')


#XBOX_BOT().start()