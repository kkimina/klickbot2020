from imagesearch import *
import pyautogui
import cv2
import time
import random
import pytesseract

class webapp():
    def __init__(self):
        self.pink       = [252, 69, 84]
        self.red        = [244, 68, 68]
        self.calib      = [0 ,0]
        self.back       = [-426, -612, 0]
        self.make_bid   = [1, -279 , 0]
        self.red_frame  = [-402,1, 0]
        self.buy        = [-29, -237, 0]
        self.ok_buy     = [-131, -279, 0]
        self.prices     = [150,200,250,300,350,400,500,550,600]
        self.run        = 'OFF'
        self.buy_price  = 0
        self.sell_price = 0
        self.suchpreis  = 1800
        self.send_screen = 0
        self.status_screen = '0'
        self.transferlist = 60


    def prepare_template_webapp(self, find_img):
        path = r'C:\Users\Kimi\Desktop\webapp'
        template = cv2.imread(path + r'\\' + find_img + '.png')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        return template

    def prepare_screenshot(self):
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def klick_button(self, find_img):
        template = self.prepare_template_webapp(find_img)
        screen = self.prepare_screenshot()

        precision = 0.9
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            pass
        else:
            if self.calib[0] is 0:
                self.calib = [max_loc[0], max_loc[1]]
            pyautogui.click(max_loc[0], max_loc[1])

    def klick_button_loop(self, find_img, find_img2, filter=10):
        while 1:
            template = self.prepare_template_webapp(find_img)
            template2 = self.prepare_template_webapp(find_img2)
            screen = self.prepare_screenshot()

            precision = 0.9
            res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            coord2 = self.calibration(self.red_frame[0], self.red_frame[1])
            image = pyautogui.screenshot()
            image = np.array(image)
            # red button
            if abs(int(image[coord2[1], coord2[0], 0]) - self.red[0]) < filter and \
                    abs(int(image[coord2[1], coord2[0], 1]) - self.red[1]) < filter and \
                    abs(int(image[coord2[1], coord2[0], 2]) - self.red[2]) < filter:
                return 2

            if max_val < precision:
                pass
            else:
                if self.calib[0] is 0:
                    self.calib = [max_loc[0], max_loc[1]]
                pyautogui.click(max_loc[0], max_loc[1])
                return 1

            res = cv2.matchTemplate(screen, template2, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val < precision:
                pass
            else:
                if self.calib[0] is 0:
                    self.calib = [max_loc[0], max_loc[1]]
                return 2

            self.calibration(self.red_frame[0], self.red_frame[1]), self.red

    def klick_loop(self, find_img):
        while 1:
            template = self.prepare_template_webapp(find_img)
            screen = self.prepare_screenshot()

            precision = 0.9
            res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val < precision:
                pass
            else:
                pyautogui.click(max_loc[0], max_loc[1])
                return 1

    def clear_list(self):
        self.klick_loop('transfers')
        self.klick_loop('transferlist')
        time.sleep(5)
        self.klick_button_loop('clear_list', 'transferlist_not_full')
        self.klick_loop('transfers')
        self.klick_loop('search_transfer')
        time.sleep(5)

    def status_img_pix(self, find_img, coord, color, coord2, color2, filter = 10):
        while 1:
            coord
            template = self.prepare_template_webapp(find_img)
            screen = self.prepare_screenshot()

            precision = 0.9
            res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            image = pyautogui.screenshot()
            image = np.array(image)

            if abs(int(image[coord[1], coord[0], 0]) - color[0]) < filter and abs(
                   int(image[coord[1], coord[0], 1]) - color[1]) < filter and abs(
                   int(image[coord[1], coord[0], 2]) - color[2]) < filter:
                return 2

            if abs(int(image[coord2[1], coord2[0], 0]) - color2[0]) < filter and abs(
                   int(image[coord2[1], coord2[0], 1]) - color2[1]) < filter and abs(
                   int(image[coord2[1], coord2[0], 2]) - color2[2]) < filter:
                return 1

            if max_val < precision:
                pass
            else:
                return 1

    def calibration(self, x, y):
        if self.calib[0] is not 0:
            return self.calib[0]+x, self.calib[1]+y

    def button_calib(self, button):
        if self.calib[0] is not 0:
            return [self.calib[0]+button[0], self.calib[1]+button[1]]

    def click_calib(self, button):
        calib_coord = self.calibration(button[0],button[1])
        pyautogui.click(calib_coord[0], calib_coord[1])

    def double_click_calib(self, x,y):
        calib_coord = self.calibration(x,y)
        pyautogui.doubleClick(calib_coord[0], calib_coord[1])


    def buy_card(self):
        self.click_calib(self.buy)
        time.sleep(0.2)
        self.click_calib(self.ok_buy)

    def sell(self):
        time.sleep(2)
        result = self.klick_button_loop('button_list', 'status_abgelaufen')
        if result is 2:
            return 'getout'
        self.transferlist = self.transferlist+1
        time.sleep(2)
        self.double_click_calib(33, -246)
        time.sleep(0.1)
        pyautogui.write(str(15000000))
        self.read_buyed_price()
        time.sleep(0.1)
        self.double_click_calib(42, -187)
        pyautogui.write(str(self.sell_price))
        self.klick_button('button_einstellen')
        time.sleep(5)

    def tess(self, reg):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        try:
            image = np.array(pyautogui.screenshot(region=(reg[0], reg[1], reg[2], reg[3])))
        except:
            print('wrong')
            image = np.array(pyautogui.screenshot(region=(reg[0], reg[1], reg[2], reg[3])))
        template = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #print(pytesseract.image_to_string(template))
        #cv2.imshow('template', template)
        #cv2.waitKey()
        return pytesseract.image_to_string(template)


    def read_buyed_price(self):
        x, y = self.calibration(+140, -304)
        objekt_string = self.tess([x, y, 60, 20])
        #print(objekt_string)
        if objekt_string.__contains__('@'):
            objekt_string = objekt_string.replace(' @', '')
            objekt_string = objekt_string.replace(',', '')
            objekt_string = objekt_string.replace('.', '')
            try:
                self.status_screen = int(self.status_screen) + int(self.sell_price*0.95) - int(objekt_string)
            except:
                self.status_screen = int(self.status_screen) + int(self.sell_price*0.95) - int(self.buy_price)

    def fill_prices(self, price):
        self.double_click_calib(-315, -353)
        time.sleep(0.1)
        pyautogui.write(str(self.prices[random.randint(0,8)]))
        time.sleep(0.1)
        self.double_click_calib(-8, -272)
        time.sleep(0.1)
        pyautogui.write(str(price))
        time.sleep(0.1)


    def main_bot(self):
        timercount = 0
        buyed = 0
        starttime = time.clock()
        while 1:
            if self.run == 'ON':
                self.klick_button('search_button')
                found = self.status_img_pix('status_not_found', self.button_calib(self.make_bid), self.pink, self.calibration(self.red_frame[0], self.red_frame[1]), self.red)
                if found is 1:
                    self.click_calib(self.back)
                elif found is 2:
                    self.buy_card()
                    sell_status = self.sell()
                    #if sell_status != 'getout':
                        #buyed = buyed + 1
                        #print(str(buyed*self.sell_price*0.95-buyed*self.buy_price))
                        #self.status_screen = str(int(buyed*self.sell_price*0.95-buyed*self.buy_price))
                    self.click_calib(self.back)
                time.sleep(random.randint(20, 80) / 10)
                timercount = timercount+1
                self.fill_prices(self.buy_price)

                if timercount > 10:
                    timercount = 0
                    if (time.clock() - starttime) < 40:
                        time.sleep(random.randint(35, 45))
                    else:
                        time.sleep(random.randint(10, 20))
                    starttime = time.clock()

                if self.transferlist > 50:
                    self.clear_list()
                    self.transferlist = 30


            elif self.run == 'SUCHE':
                self.klick_button('search_button')
                time.sleep(2)
                self.click_calib(self.back)
                time.sleep(2)
                self.fill_prices(self.suchpreis)
                self.klick_button('search_button')
                time.sleep(2)
                self.send_screen = 1
                self.run = 'SUCHE_WEITER'
            elif self.run == 'SUCHE_WEITER' and self.send_screen == 0:
                self.click_calib(self.back)
                time.sleep(3)
                self.fill_prices(self.buy_price)
                self.run = 'SUCHE_END'
