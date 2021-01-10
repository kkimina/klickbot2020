import tkinter as tk
import tkinter.ttk as ttk
from new_bot import *
from webap_klick import *

from subprocess import Popen
import threading
import requests
import hashlib

from new_bot import XBOX_BOT

process = ''
import json

class BotiWidget(ttk.Frame):
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.bot    = XBOX_BOT()
        self.webapp = webapp()
        self.temp           = 0
        self.webapp_coins   = 0
        self.stoerfeuer     = 0

        frame_2 = ttk.Frame(self)
        xbox_verkauf = ttk.Entry(frame_2)
        self.xbox_verkauf_val = tk.StringVar('')
        self.xbox_verkauf_val.set('4700')
        xbox_verkauf.config(textvariable=self.xbox_verkauf_val)
        xbox_verkauf.grid(column='1', row='2')

        self.xbox_kauf_val = tk.StringVar('')
        self.xbox_kauf_val.set('4300')
        xbox_kauf = ttk.Entry(frame_2)
        xbox_kauf.config(textvariable=self.xbox_kauf_val)
        xbox_kauf.grid(column='1', row='3')

        self.xbox_statistics = tk.StringVar('')
        self.xbox_statistics.set('XBOX')
        label_3 = ttk.Label(frame_2)
        label_3.config(textvariable=self.xbox_statistics)
        label_3.grid(column='1', pady='10', row='0', sticky='w')
        label_3.grid_propagate(0)

        xbox_start = ttk.Button(frame_2)
        self.xbox_start_field = tk.StringVar('')
        self.xbox_start_field.set('START BOT')
        xbox_start.config(takefocus=False, text='START BOT', textvariable=self.xbox_start_field, command=self.starting)
        xbox_start.grid(column='0', row='4', sticky='e')
        xbox_start.columnconfigure('0', minsize='0', pad='60')


        xbox_run = ttk.Button(frame_2)
        self.start_bot_field = tk.StringVar('')
        self.start_bot_field.set('PAUSE')
        xbox_run.config(takefocus=False,  text='PAUSE',  textvariable=self.start_bot_field, command=self.bot_on_off)
        #xbox_run.grid(column='0', row='5', sticky='e')
        xbox_run.grid(column='1', row='4', sticky='w')
        xbox_run.columnconfigure('0', minsize='0', pad='60')
        label_5 = ttk.Label(frame_2)
        label_5.config(compound='top', text='Verkauf:')
        label_5.grid(column='0', row='2')
        label_5.columnconfigure('0', minsize='0', pad='60')
        label_7 = ttk.Label(frame_2)
        label_7.config(text='Kauf:')
        label_7.grid(column='0', row='3')
        label_7.columnconfigure('0', minsize='0', pad='60')
        #xbox_telegram = ttk.Button(frame_2)
        #xbox_telegram.config(state='normal', text='telegram')
        #xbox_telegram.grid(column='1', row='4', sticky='w')
        frame_2.config(borderwidth='0', height='0', takefocus=True, width='200')
        frame_2.grid(column='1', row='0', sticky='w')
        frame_2.columnconfigure('1', pad='30')
        frame_4 = ttk.Frame(self)
        selling_min = ttk.Entry(frame_4)

        self.selling_min_val = tk.StringVar('')
        self.selling_min_val.set('55000')
        selling_min.config(textvariable=self.selling_min_val)
        selling_min.grid(column='1', row='2')
        selling_min.rowconfigure('2', minsize='0')
        selling_min.columnconfigure('1', minsize='0', pad='0')
        selling_max = ttk.Entry(frame_4)
        self.selling_max_val = tk.StringVar('')
        selling_max.config(textvariable=self.selling_max_val)
        self.selling_max_val.set('225000')
        selling_max.grid(column='1', row='3')
        selling_max.columnconfigure('1', minsize='0', pad='0')
        label_2 = ttk.Label(frame_4)
        label_2.config(text='Selling')
        label_2.grid(column='1', pady='10', row='0', sticky='w')
        label_2.columnconfigure('1', minsize='0', pad='0')
        label_8 = ttk.Label(frame_4)
        label_8.config(text='min price:')
        label_8.grid(column='0', padx='0', row='2')
        label_8.rowconfigure('2', minsize='0')
        label_8.columnconfigure('0', minsize='0', pad='60')
        label_9 = ttk.Label(frame_4)
        label_9.config(text='max price:')
        label_9.grid(column='0', row='3')
        label_9.columnconfigure('0', minsize='0', pad='60')
        selling_run = ttk.Button(frame_4)
        self.sell_field = tk.StringVar('')
        self.sell_field.set('SELLING - OFF')
        selling_run.config(textvariable=self.sell_field, command=self.selling_on_off)
        selling_run.grid(column='1', ipadx='20', row='4')
        selling_run.grid_propagate(0)
        selling_run.rowconfigure('4', minsize='0')
        selling_run.columnconfigure('1', minsize='0', pad='0')
        frame_4.config(height='200', width='200')
        frame_4.grid(column='3', row='0', sticky='e')
        frame_5 = ttk.Frame(self)
        webapp_run = ttk.Button(frame_5)
        self.webapp_run_field = tk.StringVar('')
        self.webapp_run_field.set('PAUSE')
        webapp_run.config(textvariable=self.webapp_run_field, command=self.webapp_on_off)
        webapp_run.grid(column='1', row='4')
        webapp_kauf = ttk.Entry(frame_5)
        self.webapp_kauf_val = tk.StringVar('')
        self.webapp_kauf_val.set('1800')
        webapp_kauf.config(textvariable=self.webapp_kauf_val)
        webapp_kauf.grid(column='1', row='3')
        webapp_verkauf = ttk.Entry(frame_5)
        self.webapp_verkauf_val = tk.StringVar('')
        self.webapp_verkauf_val.set('2100')
        webapp_verkauf.config(textvariable=self.webapp_verkauf_val)
        webapp_verkauf.grid(column='1', row='2')
        self.webapp_status_screen = tk.StringVar('')
        self.webapp_status_screen.set('WEBAPP')
        label_12 = ttk.Label(frame_5)
        label_12.config(textvariable=self.webapp_status_screen)
        label_12.grid(column='1', ipadx='0', ipady='0', pady='10', row='0', sticky='w')
        label_12.grid_propagate(0)
        label_12.rowconfigure('0', minsize='0', pad='0', weight='0')
        label_13 = ttk.Label(frame_5)
        label_13.config(font='TkDefaultFont', text='Verkauf:')
        label_13.grid(column='0', row='2')
        label_13.columnconfigure('0', minsize='0', pad='60')
        label_14 = ttk.Label(frame_5)
        label_14.config(text='Kauf:')
        label_14.grid(column='0', row='3')
        label_14.columnconfigure('0', minsize='0', pad='60')
        frame_5.config(height='200', width='200')
        frame_5.grid(column='1', ipadx='0', row='1')
        frame_5.columnconfigure('1', pad='30')

    def starting(self):
        threading.Thread(target=self.automatic_update).start()
        threading.Thread(target=self.bot.start).start()
        time.sleep(3)
        self.bot_on_off()
        threading.Thread(target=self.get_coin_sell).start()
        threading.Thread(target=self.webapp.main_bot).start()
        threading.Thread(target=self.bot.tele.other_bot).start()
        threading.Thread(target=self.timerstatistic).start()
        self.bot.tele.updater.start_polling()
        #self.bot.tele.updater.idle()


    def telegram(self):
        threading.Thread(target=self.bot.tele.other_bot).start()

    def pause(self):
            if self.bot.tele.status == 'botpause':
                self.bot.tele.status = ''
                self.bot_on_off()

            if self.bot.tele.status == 'webapppause':
                self.bot.tele.status = ''
                self.webapp_on_off()

            if self.bot.tele.status == 'sellingpause':
                self.bot.tele.status = ''
                self.selling_on_off()

    def timerstatistic(self):
        while 1:
            last_time       = time.time()
            last_requests   = self.bot.server_request
            time.sleep(60)
            time_diff    = time.time() - last_time
            request_diff = self.bot.server_request - last_requests
            print(request_diff/time_diff)
            if request_diff/time_diff > 0.1:
                self.bot.sleep = self.bot.sleep + 1
            else:
                self.bot.sleep = max(self.bot.sleep - 1,0)

    def change_prices(self):
            if self.bot.tele.status == 'bot':
                self.xbox_verkauf_val.set(str(self.bot.tele.verkauf))
                self.xbox_kauf_val.set(str(self.bot.tele.kauf))
                self.bot.tele.telegram_bot_sendtext('NEWPRICES BOT:' + str(self.bot.tele.kauf) + ' ' + str(self.bot.tele.verkauf))
                self.bot.tele.status = ''
            if self.bot.tele.status == 'webapp':
                self.webapp_verkauf_val.set(str(self.bot.tele.verkauf))
                self.webapp_kauf_val.set(str(self.bot.tele.kauf))
                self.bot.tele.telegram_bot_sendtext(
                    'NEWPRICES webapp:' + str(self.bot.tele.kauf) + ' ' + str(self.bot.tele.verkauf))
                self.bot.tele.status = ''
            if self.bot.tele.status =='wprice':
                self.temp       = self.webapp.run
                self.webapp.run = 'SUCHE'
                self.webapp.suchpreis = self.bot.tele.webapp_price
                self.bot.tele.status = 'wprice_next'
            if self.bot.tele.status =='screen':
                self.webapp.run = 'SUCHE_WEITER'
                self.webapp.send_screen = 0
                self.bot.tele.status = ''
            if self.webapp.run == 'SUCHE_END':
                self.webapp.run = self.temp
            if self.webapp.send_screen == 1 and self.bot.tele.status =='wprice_next':
                self.bot.tele.screen_search = 1
                self.bot.tele.telegram_bot_sendtext(
                    'CONFIRM with: /screen')
                self.bot.tele.status == ''


    def automatic_update(self):
        self.stoerfeuer = 0
        while 1:
            self.xbox_statistics.set(str(self.bot.cards) + " von (" + str(self.bot.insgesamt) + ")")
            self.change_prices()
            self.pause()
            self.send_statistic()
            self.webapp.sell_price    = int(self.webapp_verkauf_val.get())
            self.webapp.buy_price     = int(self.webapp_kauf_val.get())
            self.bot.buy_price        = int(self.xbox_verkauf_val.get())
            self.bot.price            = int(self.xbox_verkauf_val.get())
            self.bot.new_price        = int(self.xbox_kauf_val.get())
            self.bot.card_price       = float(0.67)
            self.webapp_status_screen.set(self.webapp.status_screen)
            sleep(5)
            if self.bot.stoerung is 1 and self.bot.solver is 'ON':
                image = pyautogui.screenshot()
                image = np.array(image)
                cv2.imwrite('stoerung.png', image)
                if self.bot.vision.suche_pics('extended')[0] != -1:
                    self.bot.stoerung           = 0
                    self.bot.get_out            = 1
                    self.bot.vision.get_out     = 1
                    self.bot.xbox_cmd.get_out   = 1
                    self.stoerfeuer             = 0
                    self.bot.vision.regions['transfermarkt_found'][0] = 0
                    self.bot.tele.telegram_bot_sendtext('getout')

                elif self.bot.vision.get_pixel_diff(image, [self.bot.getCalibX(-45),self.bot.getCalibY(-48)], [151,  70, 244], 10):
                    self.bot.xbox_cmd.press_button('up')
                    self.bot.tele.telegram_bot_sendtext('geklappt')
                    print('geklappt')

                elif self.bot.vision.suche_pics('erneut_versuchen')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('erneut_versuchen')
                    print('erneut_versuchen')

                elif self.bot.vision.suche_pics('abgeschlossen')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    time.sleep(3)
                    self.bot.xbox_cmd.press_button('b')
                    time.sleep(3)
                    self.bot.xbox_cmd.press_button('left')
                    time.sleep(3)
                    self.bot.tele.telegram_bot_sendtext('transferliste_out')
                    print('transferliste_out')

                elif self.bot.vision.suche_pics('kandidatenliste')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('kandidatenliste')
                    print('kandidatenliste')

                elif self.bot.vision.suche_pics('transfermarkt1')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('transfermarkt1')
                    print('transfermarkt1')

                elif self.bot.vision.suche_pics('transfermarkt2')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('transfermarkt2')
                    print('transfermarkt2')

                elif self.bot.vision.suche_pics('verschieben')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('verschieben')
                    print('verschieben')

                elif self.bot.vision.suche_pics('abgelaufen')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('abgelaufen_pressed_a')
                    print('abgelaufen_pressed_a')

                elif self.bot.vision.suche_pics('abgelaufen2')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('abgelaufen2_pressed_a')

                elif self.bot.vision.suche_pics('ok2')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('ok2_pressed_a')
                    print('ok2_pressed_a')

                elif self.bot.vision.suche_pics('ok3')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('ok3_pressed_a')
                    print('ok3_pressed_a')

                elif self.bot.vision.suche_pics('ok4')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('ok4_pressed_a')
                    print('ok4_pressed_a')

                elif self.bot.vision.suche_pics('ok5')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('ok5_pressed_a')
                    print('ok5_pressed_a')

                elif self.bot.vision.suche_pics('sicher_nein')[0] != -1:
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('sicher_a')
                    print('sicher_a')

                elif self.bot.vision.suche_pics('sicher_ja')[0] != -1:
                    self.bot.xbox_cmd.press_button('down')
                    self.bot.tele.telegram_bot_sendtext('sicher_runter')
                    print('sicher_runter')

                elif self.bot.vision.suche_pics('transfermarkt_found')[0] != -1:
                    self.bot.xbox_cmd.press_button('b')
                    self.bot.tele.telegram_bot_sendtext('transfermarkt_found_pressed_b')

                elif self.bot.vision.get_pixel_diff(image, [self.bot.getCalibX(17),self.bot.getCalibY(274)], [120,  68, 233], 10):
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('get_back')
                    print('transfermarkt_found_pressed_b')

                elif self.bot.vision.get_pixel_diff(image, [self.bot.getCalibX(-97),self.bot.getCalibY(276)], [135,  81, 251], 10):
                    self.bot.vision.get_pixel_color(self, self.bot.getCalibX(17), self.bot.getCalibY(274), self.bot.xbox_cmd, 'right',[120, 68, 233], 0)
                    self.bot.tele.telegram_bot_sendtext('go_to_transfermarkt')
                    print('go_to_transfermarkt')

                elif self.bot.vision.suche_pics('kuemmern')[0] != -1:
                    self.bot.xbox_cmd.press_button('up')
                    time.sleep(3)
                    self.bot.xbox_cmd.press_button('a')
                    self.bot.tele.telegram_bot_sendtext('kuemmern')
                    print('kuemmern')

                elif self.bot.vision.suche_pics('fehler1')[0] != -1:
                    self.bot.xbox_cmd.press_button('b')
                    time.sleep(3)
                    self.bot.tele.telegram_bot_sendtext('fehler1')
                    print('fehler1')


                else:
                    self.stoerfeuer = self.stoerfeuer + 1
                    if self.stoerfeuer > 5:
                        self.bot.tele.telegram_bot_sendtext('STÖÖÖÖHRUNG no solution')
                        print('STÖÖÖÖHRUNG no solution')
                        self.bot.solver = 'OFF'

    def send_statistic(self):
        if self.webapp_status_screen.get() != 'WEBAPP':
            if self.webapp_coins != int(self.webapp_status_screen.get()):
                self.bot.tele.telegram_bot_sendtextSTATUS('WEBAPP: '+ str(int(self.webapp_status_screen.get()) - self.webapp_coins) + ' insgesamt: '+str(int(self.webapp_status_screen.get())))
                self.webapp_coins = int(self.webapp_status_screen.get())

    def get_coin_sell(self):
        print('Start Coin-Selling')
        partnerid = '12158'
        secretkey = 'fdbc4d17393168e074d8cf98865651ff'
        requestspeed = 0.75

        while 1:

            timestamp = str(int(time.time()))
            hash = hashlib.md5((str(partnerid) + str(secretkey) + str(timestamp)).encode())
            minbuy = str(self.selling_min_val.get())
            maxbuy = str(self.selling_max_val.get())
            dsfut_path = r'https://dsfut.net/api/21/xb/' + partnerid + r'/' + timestamp + r'/' + str(
                hash.hexdigest() + r'?min_buy=' + minbuy + r'&max_buy=')# + maxbuy+ r'&take_after=10')
            if self.bot.coinselling is 'ON':
                output = requests.get(dsfut_path).text
                if output.__contains__(r'Queue is empty'):
                    pass
                elif output.__contains__(r'Parameters Error'):
                    self.bot.tele.telegram_bot_sendtext('Kein Spieler im Preissegment')
                elif output.__contains__(r'Timestamp Error'):
                    print('Timestamp Error')
                    #self.bot.tele.telegram_bot_sendtext('Timestamp Error')
                    #time.sleep(5)
                elif output.__contains__(r'Please try again in'):
                    print(output)
                    #sleep(int(str(output)[str(output).find('in') + 6:str(output).find('minutes') - 1]) * 60)
                elif output.__contains__(r'Request Limit Error'):
                    print(output)
                    sleep(5)
                    requestspeed = requestspeed+0.1
                else:
                    print(output)
                    self.bot.tele.telegram_bot_sendtext(output)
                    json_output = json.loads(output)
                    player = json_output['player']
                    self.bot.tele.telegram_bot_sendtext(
                        'Name:     ' + str(player['name']) + "\n" +

                        'Rating:    ' + str(player['rating']) + "\n" +

                        'Position:  ' + str(player['position']) + "\n" +

                        'Start:       ' + str(player['startPrice']) + "\n" +

                        'BuyNow:  ' + str(player['buyNowPrice']) + "\n")
                    self.sell_field.set('SELLING - OFF')
                    self.bot.coinselling = 'OFF'
            time.sleep(requestspeed)

    #def find_img(self):
    #    i = 0
    #    while 1:
    #        i=i+1
    #        coo = self.bot.vision.suche_pics('test')[0]
    #        if coo == -1:
    #            print('not found')
    #        elif coo == 670 or coo == 0:
    #            print('found')
    #        else:
    #            print('error')
    #        print(i)
    #        sleep(0.1)

    def selling_on_off(self):
        if self.bot.coinselling is 'OFF':
            self.sell_field.set('SELLING - Running...')
            self.bot.coinselling = 'ON'
            self.bot.solver      = 'ON'
            self.stoerfeuer      = 0

        elif self.bot.coinselling is 'ON':
            self.sell_field.set('SELLING - OFF')
            self.bot.coinselling = 'OFF'
            self.bot.solver      = 'ON'
            self.stoerfeuer      = 0

    def bot_on_off(self):
        if self.bot.run is 'OFF':
            self.start_bot_field.set('RUN')
            self.bot.run = 'ON'
        elif self.bot.run is 'ON':
            self.start_bot_field.set('PAUSE')
            self.bot.run = 'OFF'
            self.bot.get_out            = 1
            self.bot.vision.get_out     = 1
            self.bot.xbox_cmd.get_out   = 1
        self.xbox_statistics.set(str(self.bot.cards) + " von (" + str(self.bot.insgesamt) + ")")
        self.bot.price = int(self.xbox_verkauf_val.get())

    def webapp_on_off(self):
        if self.webapp.run is 'OFF':
            self.webapp_run_field.set('RUN')
            self.webapp.run = 'ON'
        elif self.webapp.run is 'ON':
            self.webapp_run_field.set('PAUSE')
            self.webapp.run = 'OFF'


    def key(self, event):
        if event.char == event.keysym:
            msg = 'Normal Key %r' % event.char
        elif event.keysym == 'F12':
            self.selling_on_off()
        elif event.keysym == 'Escape':
            self.bot_on_off()
        elif event.keysym == 'w':
            self.webapp_on_off()
        #elif len(event.char) == 1:
        #    msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
        else:
            msg = 'Special Key %r' % event.keysym
        #print(msg)



if __name__ == '__main__':
    root = tk.Tk()
    widget = BotiWidget(root)
    widget.pack(expand=True, fill='both')
    root.bind_all('<Key>', widget.key)
    root.mainloop()

