from imagesearch import *
import pyautogui
import cv2
from time import *
import time
import pytesseract

class imagebot():
    def __init__(self, xbox_control):
        self.init = 0
        self.xbox_control = xbox_control
        self.get_out = 0
        self.blue = [62, 225, 237]
        self.pink = [250, 84, 97]
        self.black_ok = [0, 0, 0]
        self.dark_grey = [221, 223, 223]

        self.regions = {
            'normal': [0, 0, 0, 0, 0],
            'abgelaufen': [0, 0, 0, 0, 0],
            'kaufen_yes': [0, 0, 0, 0, 0],
            'transfermarkt_found': [0, 0, 0, 0, 0],
            'transfermarkt_nix': [0, 0, 0, 0, 0],
            'gekauft': [0, 0, 0, 0, 0],
            'selling1': [0, 0, 0, 0, 0],
            'selling2': [0, 0, 0, 0, 0],
            'transfers': [0, 0, 0, 0, 0],
            'verbrauch': [0, 0, 0, 0, 0],
            'anbieten1': [0, 0, 0, 0, 0],
            'extended': [0, 0, 0, 0, 0],
            'extended_safe': [0, 0, 0, 0, 0],
            'ok': [0, 0, 0, 0, 0],
            'ok2': [0, 0, 0, 0, 0],
            'ok3': [0, 0, 0, 0, 0],
            'ok4': [0, 0, 0, 0, 0],
            '100full': [0, 0, 0, 0, 0],
            'bietoption': [0, 0, 0, 0, 0],
            'transfermarkt': [0, 0, 0, 0, 0]
        }




    def get_pixel_diff(self, image, coord2, color, filter):
        if self.get_out is 1:
            return 'get_out'
        if abs(int(image[coord2[0], coord2[1], 0]) - color[0]) < filter and abs(
                int(image[coord2[0], coord2[1], 1]) - color[1]) < filter and abs(
                int(image[coord2[0], coord2[1], 2]) - color[2]) < filter:
            return 1
        else:
            return 0


    def get_pixel_color(self, bot, x, y, xbox_cmd, command, color, schnell = 1):
        sicherheit = 0
        bot.status = 'get_pixel_color'+command#+str(x)+str(y)
        while 1:
            if self.get_out is 1:
                return 'get_out'

            try:
                image = pyautogui.screenshot()
                image = np.array(image)
                thresh = 10
            except:
                sicherheit = sicherheit + 1

            if self.get_pixel_diff(image, [x, y], color, thresh):
                bot.stoerung = 0
                return
            else:
                if sicherheit < 50:
                    if command != 'nix':
                        xbox_cmd.press_button(command)
                        time.sleep(0.01)
                        if schnell is 0:
                            sleep(1)
                    sicherheit = sicherheit + 1
                else:
                    bot.stoerung = 1
                    print('pink ' + str(image[[x, y][0], [x, y][1], 0] - color[0]) + ',' +
                                    str(image[[x, y][0], [x, y][1], 1] - color[0]) + ',' +
                                    str(image[[x, y][0], [x, y][1], 2] - color[0]))


    def search_loop(self, bot,  pic):
        bot.status = 'search_loop'+str(pic)
        sicherheit = 0
        #TODO: for in loop und return 0 fehlerananlyse
        while 1:
            if self.get_out is 1:
                return 'get_out'
            sleep(0.5)
            ttt = self.suche_pics(pic)
            if ttt[0] != -1:
                bot.stoerung = 0
                return 1
            else:
                sicherheit = sicherheit + 1
                if sicherheit > 50:
                    bot.stoerung = 1


    def get_color_row(self, bot):
        count = 0
        try:
            image = pyautogui.screenshot()
        except:
            print('wrong')
        image = np.array(image)
        for r in range(bot.getCalibY(355), bot.getCalibY(800)):
            coord2 = [bot.getCalibX(-42), r - 1]

            if image[coord2[0], coord2[1], 0] > 200 and \
                    image[coord2[0], coord2[1], 1] > 200 and \
                    image[coord2[0], coord2[1], 2] > 100 and image[coord2[0], coord2[1], 2] < 180:
                count = count + 1
        return count

    def waitKaufsignal(self, bot):
        while 1:
            if self.get_out is 1:
                return 'get_out'

            if self.get_color_row(bot) > 20:
                return 1

    def suche_pics(self, find_img):
        if self.get_out is 1:
            return 'get_out'
        precision = 0.9
        template = self.prepare_template(find_img)

        image = self.prepare_screenshot(find_img)
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return [-1, -1]
        else:
            self.regions[find_img][0] = max_loc[0]
            self.regions[find_img][1] = max_loc[1]
            self.regions[find_img][2] = template.shape[1]
            self.regions[find_img][3] = template.shape[0]
            self.regions[find_img][4] = template
            cv2.imwrite('wrong_' + find_img + '.png', image)
        return max_loc

    def prepare_template(self, find_img):
        if self.get_out is 1:
            return 'get_out'
        if self.regions[find_img][4] is 0:
            path = r'C:\Users\Kimi\Desktop'
            template = cv2.imread(path + r'\\' + find_img + '.png')
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            self.regions[find_img][4] = template
            return template
        else:
            return self.regions[find_img][4]

    def prepare_screenshot(self, find_img):
        if self.get_out is 1:
            return 'get_out'

        try:
            if self.regions[find_img][0] == 0:
                image = pyautogui.screenshot()
            else:
                image = pyautogui.screenshot(
                region=(self.regions[find_img][0], self.regions[find_img][1], self.regions[find_img][2], self.regions[find_img][3]))
        except:
            print('wrong')
            image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def pixel_compare(self, bot, coord1, coord2, color1, color2, filter1, filter2):
        bot.status = 'pixel_compare'#+str(coord1)+str(coord2)+str(color1)+str(color2)
        sicherheit = 0
        while 1:
            if self.get_out is 1:
                return 'get_out'
            try:
                image = pyautogui.screenshot()
            except:
                print('wrong')
                image = pyautogui.screenshot()
            image = np.array(image)

            if self.get_pixel_diff(image, coord1, color1, filter1):
                bot.stoerung = 0
                return 1
            elif self.get_pixel_diff(image, coord2, color2, filter2):
                bot.stoerung = 0
                return 2
            else:
                if sicherheit < 500:
                    sicherheit = sicherheit + 1
                else:
                    bot.stoerung = 1
                    sleep(0.05)
                    print(color2)
                    print(str(image[coord2[0], coord2[1], 0]) + ',' +
                          str(image[coord2[0], coord2[1], 1]) + ',' +
                          str(image[coord2[0], coord2[1], 2]))

    def suche_pics2(self, bot, find_img1, find_img2):
        if self.get_out is 1:
            return 'get_out'
        bot.status = 'suche_pics2'+find_img1+find_img2
        precision = 0.9
        template1 = self.prepare_template(find_img1)
        template2 = self.prepare_template(find_img2)

        image1 = self.prepare_screenshot(find_img1)
        image2 = self.prepare_screenshot(find_img2)

        res2 = cv2.matchTemplate(image2, template2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
        if max_val > precision:
            if self.regions[find_img2][0] is 0:
                self.regions[find_img2][0] = max_loc[0]
                self.regions[find_img2][1] = max_loc[1]
                self.regions[find_img2][4] = template2
                self.regions[find_img2][2] = template2.shape[1]
                self.regions[find_img2][3] = template2.shape[0]
            cv2.imwrite('wrong_' + find_img2 + '.png', image2)
            # print("--- %s seconds ---" % (time.time() - start_time))
            return 2

        res1 = cv2.matchTemplate(image1, template1, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)
        if max_val > precision:
            # print('found2')
            if self.regions[find_img1][0] is 0:
                self.regions[find_img1][0] = max_loc[0]
                self.regions[find_img1][1] = max_loc[1]
                self.regions[find_img1][4] = template1
                self.regions[find_img1][2] = template1.shape[1]
                self.regions[find_img1][3] = template1.shape[0]
                cv2.imwrite('wrong_' + find_img1 + '.png', image1)
            # print("--- %s seconds ---" % (time.time() - start_time))
            return 1
        return 0

    def suche_pics_part(self,find_img1, precision=0.9):
        if self.get_out is 1:
            return 'get_out'
        template1 = self.prepare_template(find_img1)
        image1 = self.prepare_screenshot(find_img1)
        try:
            res1 = cv2.matchTemplate(image1, template1, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)
        except:
            print(find_img1)
            print(template1)
            print(image1)
            self.regions[find_img1][0] = 0
            image1 = self.prepare_screenshot(find_img1)
            res1 = cv2.matchTemplate(image1, template1, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)


        if max_val > precision:
            #print(find_img1 + ': '+str(max_loc[0])+','+str(max_loc[1]))
            if self.regions[find_img1][0] is 0:
                self.regions[find_img1][0] = max_loc[0]
                self.regions[find_img1][1] = max_loc[1]
                self.regions[find_img1][4] = template1
                self.regions[find_img1][2] = template1.shape[1]
                self.regions[find_img1][3] = template1.shape[0]
                cv2.imwrite('wrong_' + find_img1 + '.png', image1)
            # print("--- %s seconds ---" % (time.time() - start_time))
            return 1
        return 0


    def suche_pics_loop(self, bot, pics):
        bot.status = 'suche_pics_loop'

        for s in pics:
            if self.get_out is 1:
                return 'get_out'
            if self.suche_pics_part(s) is 1:
                return int(pics[s])
        return 0

    def tess(self,bot, reg):
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

    def ok_while(self, bot):
        while 1:
            if self.get_out is 1:
                return 'get_out'

            stringi = self.tess(bot, [1156, 220, 700, 240])
            if stringi.__contains__('OK') or stringi.__contains__('Transferpreises'):
                bot.xbox_cmd.press_button('a')
                break