from time import *
from xbox_controll import XBOX_CONTROL
from computer_vision import imagebot
from telegrams import TGRAMS
from imagesearch import *
import pyautogui
import sys

class XBOX_BOT():

    def __init__(self):
        self.proof_loop =   {
                                'ok'                 : '2',
                                'ok2'                : '2',
                                'ok3'                : '2',
                                'abgelaufen'         : '2',
                                'gekauft'            : '1',
                                'gekauft2'           : '1',
                            }
        self.status         = 'init'
        self.run            = 'OFF'
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
        self.fast           = 0
        self.debug          = 0
        self.sicherheit     = 0


    def start(self):
        self.xbox_cmd   = XBOX_CONTROL()
        self.xbox_cmd.run()

        self.vision     = imagebot(self.xbox_cmd)
        self.tele       = TGRAMS()

        self.tele.telegram_bot_sendtextSTATUS('START-BOT')
        self.searchingbegin()

    def init_sicherheit(self):
        self.sicherheit = 0
        self.stoerung   = 0


    def preissuche_loop(self):
        sicherheit = 0
        while 1:
            if self.debug is 1:
                print('preissuche_loop')
            if self.get_out is 1:
                return 'get_out'
            if self.fast is 1:
                sleep(0.7)
            else:
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
        try:
            obje_string = self.vision.tess(self, [self.getCalibY(470), self.getCalibX(-263), 102, 39])
            if obje_string.__contains__('/100 Items'):
                objekt_string = obje_string.replace('/100 Items', '')
                self.transfermarkt = int(self.replace_string(objekt_string))
                if self.transfermarkt > 90:
                    self.tele.telegram_bot_sendtext('TRANSFERMARKT FULL: ' + str(self.transfermarkt))
                    self.tele.telegram_bot_sendtext('TRANSFERMARKT FULL: ' + str(obje_string))
                    pass
        except:
            pass
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
        self.vision.get_pixel_color(self, self.getCalibX(-134), self.getCalibY(287), self.xbox_cmd, 'down', self.vision.lila, 0)
        self.xbox_cmd.press_button('lt')
        self.vision.get_pixel_color(self, self.getCalibX(-158), self.getCalibY(298), self.xbox_cmd, 'up', self.vision.lila, 0)
        sleep(0.5)
        self.xbox_cmd.make_price(anfang, self.price)
        try:
            self.last_price = int(self.replace_string(self.vision.tess(self, [self.getCalibY(397), self.getCalibX(-98), 44, 20])))
            self.sum = self.sum + self.price * 0.95 - self.last_price
        except:
            self.sum = self.sum + self.price * 0.95 - self.buy_price
            #print("Unexpected error:", sys.exc_info()[0])
            pass


        self.vision.get_pixel_color(self, self.getCalibX(-19), self.getCalibY(338), self.xbox_cmd, 'up', self.vision.lila,  0)


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
        if self.transfermarkt > 95:
            sleep(120)
        self.xbox_cmd.press_button('b')
        sleep(5)
        self.vision.get_pixel_color(self, self.getCalibX(-97),self.getCalibY(276), self.xbox_cmd, 'right', 	[135,  81, 251], 0)
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
        self.vision.get_pixel_color(self, self.getCalibX(17),self.getCalibY(274), self.xbox_cmd, 'right', [120,  68, 233], 0)
        self.xbox_cmd.press_button('a')
        sleep(5)

    def whilebreak(self):
        if self.sicherheit > 50:
            self.stoerung = 1
        self.sicherheit = self.sicherheit + 1

    def safetyTest(self):
        if self.get_out is 1:
            return 'get_out'
        self.init_sicherheit()
        while 1:
            image = pyautogui.screenshot()
            image = np.array(image)
            if self.vision.get_pixel_diff(image, [self.getCalibX(-148),self.getCalibY(+287)], [29, 107, 43], 10):
                self.init_sicherheit()
                return 1
            else:
                self.whilebreak()

    def new_extended(self):
        if self.get_out is 1:
            return 'get_out'
        if self.transfermarkt > 90:
            self.empty_transfermarket()
            self.transfermarkt = 0

        self.make_new_price()
        self.safetyTest()

        self.vision.get_pixel_color(self, self.getCalibX(25), self.getCalibY(-170), self.xbox_cmd, 'down', self.vision.cyan, 0)
        self.xbox_cmd.press_button('left')
        try:
            stringi = self.vision.tess(self, [self.getCalibY(-183),self.getCalibX(-291), 50, 15])
            self.gesamt_coins_ = int(self.replace_string(stringi))
        except:
            pass
        self.xbox_cmd.press_button('y')

    def make_new_price(self):
        self.vision.get_pixel_color(self, self.getCalibX(-36), self.getCalibY(-241), self.xbox_cmd, 'down',
                                    [78,244,228], 0, thresh = 30)
        self.vision.get_pixel_color(self, self.getCalibX(123), self.getCalibY(-156), self.xbox_cmd, 'a', [62, 156, 191],
                                    0)
        if self.new_price == self.confirm_price:
            return
        else:
            self.confirm_price = self.new_price
        if self.fast is 1:
            return
        if self.get_out is 1:
            return 'get_out'
        self.vision.get_pixel_color(self, self.getCalibX(87), self.getCalibY(-167), self.xbox_cmd, 'down', self.vision.cyan, 0)

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
        sleep(2)
        self.xbox_cmd.press_button('a')
        sleep(2)
        self.xbox_cmd.press_button('b')


    def transfermarkt_loop(self):
        gotIt = 0
        for s in range(0, 50):
            if self.debug is 1:
                print('transfermarkt_loop')
            if self.get_out is 1:
                return 'get_out'

            if self.vision.regions['transfermarkt_found'][0] == 0:
                nix = self.vision.suche_pics2(self, 'transfermarkt_nix', 'transfermarkt_found')
            else:
                nix = self.vision.pixel_compare(self,
                                    [self.getCalibX(-50),self.getCalibY(44)],
                                    [self.getCalibX(-235), self.getCalibY(+96)],
                                                self.vision.lila,
                                               [45, 45, 63],
                                                 10, 10)

            if nix == 2:
                self.vision.waitKaufsignal2(self, self.getCalibX(123),self.getCalibY(-245))
                self.xbox_cmd.kaufen2(self, self.vision)
                gotIt = self.proof_kauf()
                break
            if nix == 3:
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
            if sicherheit > 10:
                self.stoerung = 1
        print('mhm')
        return 0

    def searchingbegin(self):
        while 1:
            for n in range(0, random.randint(10,16)):
                starttime = time.clock()
                if self.get_out is 1:
                    self.get_out            = 0
                    self.vision.get_out     = 0
                    self.xbox_cmd.get_out   = 0
                    self.stoerung           = 0
                    self.solver             = 'ON'
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
                        #self.tele.telegram_bot_sendtextSTATUS(str(self.cards) + " von (" + str(self.insgesamt) + ") " + str(int(self.sum)) + ' Coins (' +str(round(self.sum*self.card_price/10000, 4))  + ' €)  Insgesamt:' + str(int(self.gesamt_coins_)) + '   TM:'+ str(self.transfermarkt))
            if self.run is 'ON':
                if (time.clock() - starttime) < 40:
                    sleep(random.randint(35, 45))
                else:
                    sleep(random.randint(10, 20))
        print('BOT_ENDE')


#XBOX_BOT().start()