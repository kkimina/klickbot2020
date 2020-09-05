from imagesearch import *
from time import *




#### suchmaske
name           = 'name'
name_confirm   = 'name_confirm'
zuruecksetzen  = 'zuruecksetzen'
qualitaet      = 'quality'
sk             = 'sk'
nk             = 'nk'
suchen         = 'suchen'

#### sell
anbieten       = 'anbieten'
sell_nk        = 'sell_nk'
sell_sk        = 'sell_sk'
sell_player    = 'sell_player'



class AutoClicker():

    def __init__(self):
        self.zurueck = 'zurueck'
        self.not_found = 'nicht_gefunden'
        self.nicht_bekommen = 'nicht_bekommen'
        # found          = 'gefunden'
        self.found  = 'einen_gefunden'
        self.found2 = 'zwei_gefunden'
        self.kaufen = 'kaufen'
        self.kaufen_confirm = 'kaufen_confirm'


    def suche_pics(self,img):
        path = r'C:\Users\Kimi\Desktop'
        img = cv2.imread(path+r'\\'+img+'.png')
        cv2.imshow('asd', img)
        cv2.waitKey()

    def suche_pic(self, img, duration):
        image = '//Users//fusselmania//Desktop//bot//'+ img +'.png'

        for i in range(0,duration):
            pos = imagesearch(image)
            if pos[0] != -1:
                pyautogui.moveTo((pos[0])/2, (pos[1])/2)
                return
            else:
                print('')
            cv2.waitKey(1)

    def suche_pic_two(self, img, img2, img3, duration):
        image  = '//Users//fusselmania//Desktop//bot//'+ img +'.png'
        image2 = '//Users//fusselmania//Desktop//bot//' + img2 + '.png'
        image3 = '//Users//fusselmania//Desktop//bot//' + img3 + '.png'
        for i in range(0,duration):
            pos  = imagesearch(image)
            pos2 = imagesearch(image2)
            pos3 = imagesearch(image3)
            if pos[0] != -1:
                return 1
            elif pos2[0] != -1:
                return 2
            elif pos3[0] != -1:
                return 3
            cv2.waitKey(1)

    def suche_pic_two_prec(self, img, img2, img3, duration):
        image  = '//Users//fusselmania//Desktop//bot//'+  img +'.png'
        image2 = '//Users//fusselmania//Desktop//bot//' + img2 + '.png'
        image3 = '//Users//fusselmania//Desktop//bot//' + img3 + '.png'
        for i in range(0,duration):
            pos  = imagesearch(image, precision=0.95)
            pos2 = imagesearch(image2, precision=0.99)
            pos3 = imagesearch(image3, precision=0.95)
            if pos[0] != -1:
                return 1
            elif pos2[0] != -1:
                return 2
            elif pos3[0] != -1:
                return 3
            cv2.waitKey(1)

    def suche_pic_two_click(self, img, img2, duration):
        image  = '//Users//fusselmania//Desktop//bot//'+ img +'.png'
        image2 = '//Users//fusselmania//Desktop//bot//' + img2 + '.png'
        iml = cv2.imread(image)
        width = iml.shape[0]
        height = iml.shape[1]
        for i in range(0,duration):
            pos  = imagesearch(image)
            pos2 = imagesearch(image2)
            if pos[0] != -1:
                pyautogui.click(x = (pos[0]  + height/2)/2, y=(pos[1]  + width/2)/2)
                return 1
            elif pos2[0] != -1:
                pyautogui.moveTo((pos2[0]  + width/2)/2, (pos2[1]  + height/2)/2)
                return 2

            cv2.waitKey(1)

    def suche_pic_click(self, img, duration):
        image = '//Users//fusselmania//Desktop//bot//' + img + '.png'

        img = cv2.imread(image)
        width = img.shape[0]
        height = img.shape[1]

        for i in range(0,duration):
            pos = imagesearch(image)
            if pos[0] != -1:
                pyautogui.click(x = (pos[0]  + height/2)/2, y=(pos[1]  + width/2)/2)
                return
            else:
                print("")
            cv2.waitKey(1)

    def fill_in_field(self, button, text):
        self.button_click(button)
        pyautogui.typewrite(text)


    def push_zurueck(self):
        self.suche_pic_click(self.zurueck, 500)



    def part_suchen(self):
        self.button_click(suchen)
        proof = self.suche_pic_two_prec(self.not_found, self.found2, self.found, 10)
        if proof == 2 or proof == 3:
            print('found')
            self.suche_pic_click(self.kaufen, 500)
            self.suche_pic_click(self.kaufen_confirm, 500)
            sleep(5)
            proof2 = self.suche_pic_two(self.nicht_bekommen, self.nicht_bekommen, anbieten, 10)
            if proof2 == 2 or proof2 == 1:
                return'nicht bekommen'
            elif proof2 == 3:
                return 'gekauft'
            else:
                return 'nix'
        elif proof == 1:
            self.button_click(self.zurueck)
            return 'nicht gefunden'

        self.button_click(self.zurueck)

    def part_verkaufen(self, sell_price):


        self.suche_pic_click(anbieten, 500)
        sleep(2)
        self.fill_in_field(sell_nk, str(1000000))
        sleep(2)
        self.fill_in_field(sell_sk, str(sell_price))
        sleep(2)
        self.suche_pic_click(sell_player, 500)
        sleep(2)

    def fill_suchmaske(self, player_name, player_quality, player_sk, player_nk):
        self.button_click(zuruecksetzen)

        #### NAME
        self.fill_in_field(name, player_name)
        self.suche_pic_click(name_confirm, 500)
        pyautogui.moveTo(100,100)

        #### QUALITY
        self.suche_pic_click(qualitaet, 500)
        self.suche_pic_click(player_quality, 500)

        #### SK
        self.fill_in_field(sk, str(player_sk))

        #### NK
        #self.fill_in_field(nk, str(player_nk))
