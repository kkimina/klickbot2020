from imagesearch import *
import pyautogui
import cv2
from time import *
import time
import pytesseract
from setting import *

class imagebot():
    def __init__(self, xbox_control):
        self.init = 0
        self.xbox_control = xbox_control
        self.get_out = 0
        self.blue = [62, 225, 237]
        self.pink = [250, 84, 97]
        self.black_ok = [0, 0, 0]
        self.dark_grey = [221, 223, 223]
        self.dunkel_blau = [20,18,71]
        self.cyan        = [42, 254, 201]
        self.lila        = [126,  66, 244]

        self.regions = {
            'normal': [0, 0, 0, 0, 0],
            'abgelaufen': [0, 0, 0, 0, 0],
            'abgelaufen2': [0, 0, 0, 0, 0],
            'kaufen_yes': [0, 0, 0, 0, 0],
            'transfermarkt_found': [0, 0, 0, 0, 0],
            'transfermarkt_nix': [0, 0, 0, 0, 0],
            'gekauft': [0, 0, 0, 0, 0],
            'gekauft2': [0, 0, 0, 0, 0],
            'selling1': [0, 0, 0, 0, 0],
            'selling2': [0, 0, 0, 0, 0],
            'transfers': [0, 0, 0, 0, 0],
            'transfermarkt1': [0, 0, 0, 0, 0],
            'transfermarkt2': [0, 0, 0, 0, 0],
            'verbrauch': [0, 0, 0, 0, 0],
            'anbieten1': [0, 0, 0, 0, 0],
            'extended': [0, 0, 0, 0, 0],
            'extended_safe': [0, 0, 0, 0, 0],
            'ok': [0, 0, 0, 0, 0],
            'ok2': [0, 0, 0, 0, 0],
            'ok3': [0, 0, 0, 0, 0],
            'ok4': [0, 0, 0, 0, 0],
            'ok5': [0, 0, 0, 0, 0],
            'test': [0, 0, 0, 0, 0],
            '100full': [0, 0, 0, 0, 0],
            'bietoption': [0, 0, 0, 0, 0],
            'transfermarkt': [0, 0, 0, 0, 0],
            'erneut_versuchen': [0, 0, 0, 0, 0],
            'jaein': [0, 0, 0, 0, 0],
            'sicher_ja': [0, 0, 0, 0, 0],
            'sicher_nein': [0, 0, 0, 0, 0],
            'abgeschlossen': [0, 0, 0, 0, 0],
            'verschieben': [0, 0, 0, 0, 0],
            'kuemmern': [0, 0, 0, 0, 0],
            'kandidatenliste': [0, 0, 0, 0, 0]
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


    def get_pixel_color(self, bot, x, y, xbox_cmd, command, color, schnell = 1,thresh = 40):
        sicherheit = 0
        bot.status = 'get_pixel_color'+command#+str(x)+str(y)
        while 1:
            if self.get_out is 1:
                return 'get_out'

            try:
                image = pyautogui.screenshot()
                image = np.array(image)

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
                            sicherheit = sicherheit + 2
                    sicherheit = sicherheit + 1
                else:
                    bot.stoerung = 1
                    print('get_pixel_color ' + str(image[[x, y][0], [x, y][1], 0] - color[0]) + ',' +
                                    str(image[[x, y][0], [x, y][1], 1] - color[1]) + ',' +
                                    str(image[[x, y][0], [x, y][1], 2] - color[2]))


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
        for r in range(bot.getCalibY(355-200), bot.getCalibY(800-300),4):
            coord2 = [bot.getCalibX(-42), r]

            if image[coord2[0], coord2[1], 0] > 100 and \
                    image[coord2[0], coord2[1], 1] > 120 and \
                    image[coord2[0], coord2[1], 2] > 65 and \
                    image[coord2[0], coord2[1], 2] < 150:
                count = count + 1
        return count

    def waitKaufsignal(self, bot):
        tried = 0
        while 1:
            if self.get_out is 1:
                return 'get_out'
            counti = self.get_color_row(bot)
            #print(counti)
            if counti > 10 or tried > 3:
                return 1
            else:
                tried = tried + 1
                print(counti)

    def waitKaufsignal2(self, bot, x, y):
        while 1:
            if self.get_out is 1:
                return 'get_out'
            image = pyautogui.screenshot()
            image = np.array(image)

            coord2 = [x, y]
            if self.get_pixel_diff(image, coord2, [112,162,50], 10):
                #print('gruen')
                return 1
                # return
                pass
            elif self.get_pixel_diff(image, coord2, [112-66,162+88,50-20], 10):
                sleep(0.1)
                #print('gruen2')
                return 1
            elif self.get_pixel_diff(image, coord2, [134, 24, 28], 10):
                sleep(0.1)
                #print('rot')
                return 1
            elif self.get_pixel_diff(image, coord2, [134-64, 24+89, 28-20], 10):
                sleep(0.1)
                #print('rot2')
                return 1
            else:
                pass
                # print(str(image[coord2[0], coord2[1], 0] - color[0]) + ',' +
                #                 str(image[coord2[0], coord2[1], 1] - color[0]) + ',' +
                #                 str(image[coord2[0], coord2[1], 2] - color[0]))

                #print('pink ' + str(image[coord2[0], coord2[1], 0]) + ',' +
                #    str(image[coord2[0], coord2[1], 1]) + ',' +
                #  str(image[coord2[0], coord2[1], 2]))



    def suche_pics(self, find_img):
        if self.get_out is 1:
            return 'get_out'
        precision = 0.7
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
            #cv2.imwrite('wrong_' + find_img + '.png', image)
        return max_loc

    def prepare_template(self, find_img):
        if self.get_out is 1:
            return 'get_out'
        if self.regions[find_img][4] is 0:
            path = r'xbox'
            template = cv2.imread(path + r'\\' + find_img + '.png')
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            self.regions[find_img][4] = template
            return template
        else:
            return self.regions[find_img][4]

    def prepare_screenshot(self, find_img):
        if self.get_out is 1:
            return 'get_out'
        while 1:
            try:
                if self.regions[find_img][0] == 0:
                    image = pyautogui.screenshot()
                else:
                    image = pyautogui.screenshot(
                    region=(self.regions[find_img][0], self.regions[find_img][1], self.regions[find_img][2], self.regions[find_img][3]))
                break
            except:
                print('wrong')
                sleep(1)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def pixel_compare(self, bot, coord1, coord4, color1, color4):
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

            if self.get_pixel_diff(image, coord1, color1, 20):
                bot.stoerung = 0
                return 1
            elif self.get_pixel_diff(image, [coord4[0], coord4[1]-153], color4, 15):
                bot.stoerung = 0
                #print('grau')
                return 2
            elif self.get_pixel_diff(image, [bot.getCalibX(123),bot.getCalibY(-245)], [134, 24, 28], 10):
                bot.stoerung = 0
                #print('prerot')
                return 3
            else:
                if sicherheit < 500:
                    sicherheit = sicherheit + 1
                else:
                    bot.stoerung = 1
                    sleep(0.05)
                    #print(color2)
                    #print(str(image[coord2[0], coord2[1], 0]) + ',' +
                    #      str(image[coord2[0], coord2[1], 1]) + ',' +
                    #      str(image[coord2[0], coord2[1], 2]))

    def suche_pics2(self, bot, find_img1, find_img2):
        if self.get_out is 1:
            return 'get_out'
        bot.status = 'suche_pics2'+find_img1+find_img2
        precision = 0.7
        template1 = self.prepare_template(find_img1)
        template2 = self.prepare_template(find_img2)

        image1 = self.prepare_screenshot(find_img1)
        image2 = self.prepare_screenshot(find_img2)
        try:
            res2 = cv2.matchTemplate(image2, template2, cv2.TM_CCOEFF_NORMED)
        except:
            pass
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
        if max_val > precision:
            if self.regions[find_img2][0] is 0:
                self.regions[find_img2][0] = max_loc[0]
                self.regions[find_img2][1] = max_loc[1]
                self.regions[find_img2][4] = template2
                self.regions[find_img2][2] = template2.shape[1]
                self.regions[find_img2][3] = template2.shape[0]
            #cv2.imwrite('wrong_' + find_img2 + '.png', image2)
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
                #cv2.imwrite('wrong_' + find_img1 + '.png', image1)
            # print("--- %s seconds ---" % (time.time() - start_time))
            return 1
        return 0

    def suche_pics_part(self,find_img1, precision=0.75):
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
                #cv2.imwrite('wrong_' + find_img1 + '.png', image1)
            # print("--- %s seconds ---" % (time.time() - start_time))
            return 1
        return 0


    def suche_pics_loop(self, bot, pics):
        bot.status = 'suche_pics_loop'
        sleep(5)
        for s in pics:
            if self.get_out is 1:
                return 'get_out'
            if self.suche_pics_part(s) is 1:
                return int(pics[s])
        return 0




    def tess(self,bot, reg):
        pytesseract.pytesseract.tesseract_cmd = tesseract
        try:
            image = np.array(pyautogui.screenshot(region=(reg[0], reg[1], reg[2], reg[3])))
        except:
            print('wrong')
            image = np.array(pyautogui.screenshot(region=(reg[0], reg[1], reg[2], reg[3])))
        template = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template = cv2.bitwise_not(template)
        template[template > 200] = 255
        #print(pytesseract.image_to_string(template))
        #cv2.imshow('template', template)
        #cv2.waitKey()
        # resize image
        return pytesseract.image_to_string(template)

#vision = imagebot('')
#vision.tess([1399, 130, 106, 39])

#vision.get_pixel_color(self, 683, 467, self.xbox_cmd, 'down', , 0)
