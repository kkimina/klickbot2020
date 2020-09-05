from telegram.ext import Updater
from telegram.ext import CommandHandler
from imagesearch import *
from test import *
import telegram
import request

class TGRAMS():
    def __init__(self):
        self.status         = 'init'
        self.updater        = 0
        self.status         = 0
        self.kauf           = 0
        self.verkauf        = 0
        self.webapp_price   = 0
        self.screen_search  = 0

    def printscreen(self, update, context):
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))

    def new(self, update, context):
        prices = update.message.text.replace('/new ', '')
        try:
            self.kauf = int(prices[:prices.find('/')])
            self.verkauf = int(prices[(prices.find('/')+1):])
            #print(self.kauf)
            #print(self.verkauf)
            self.telegram_bot_sendtext('CONFIRM NEWPRICES:' + str(self.kauf) + ' '+ str(self.verkauf) + ' with /bot or /webapp')
        except:
            self.kauf    = 0
            self.verkauf = 0
            self.telegram_bot_sendtext('FEHLER NEWPRICE')

    def pause(self, update, context):
            self.telegram_bot_sendtext('CONFIRM PAUSE:' ' for /sellingpause or /botpause or /webapppause')




    def wprice(self, update, context):
        prices = update.message.text.replace('/wprice ', '')
        self.webapp_price = int(prices)
        self.status = 'wprice'


    def screen(self, update, context):
        if self.screen_search == 1:
            image = pyautogui.screenshot()
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imwrite('printscreen.png', image)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))
            self.screen_search = 0
            self.status = 'screen'

    def webapp(self, update, context):
        self.status = 'webapp'

    def webapppause(self, update, context):
        self.status = 'webapppause'

    def botpause(self, update, context):
        self.status = 'botpause'

    def sellingpause(self, update, context):
        self.status = 'sellingpause'

    def bot(self, update, context):
        self.status = 'bot'

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

    def rb(self, update, context):
        press_button('rb')
        image = pyautogui.screenshot()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('printscreen.png', image)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))


    def lb(self, update, context):
        press_button('lb')
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
        self.updater = Updater(token='1091873086:AAG3Zas2Tx3egjq0odjx8aydt3fkfsbpHWA', use_context=True)
        printscreen_handler = CommandHandler('printscreen', self.printscreen)
        wprice_handler = CommandHandler('wprice', self.wprice)
        screen_handler = CommandHandler('screen', self.screen)
        up_handler = CommandHandler('up', self.up)
        down_handler = CommandHandler('down', self.down)
        newprice_handler = CommandHandler('new', self.new)
        right_handler = CommandHandler('right', self.right)
        left_handler = CommandHandler('left', self.left)
        rt_handler = CommandHandler('rt', self.rt)
        lt_handler = CommandHandler('lt', self.lt)
        rb_handler = CommandHandler('rb', self.rb)
        lb_handler = CommandHandler('lb', self.lb)
        a_handler = CommandHandler('a', self.a)
        b_handler = CommandHandler('b', self.b)
        x_handler = CommandHandler('x', self.x)
        y_handler = CommandHandler('y', self.y)
        pause_handler = CommandHandler('pause', self.pause)
        webapp_handler = CommandHandler('webapp', self.webapp)
        bot_handler    = CommandHandler('bot', self.bot)
        webapppause_handler = CommandHandler('webapppause', self.webapppause)
        botpause_handler = CommandHandler('botpause', self.botpause)
        sellingpause_handler = CommandHandler('sellingpause', self.sellingpause)

        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(screen_handler)
        dispatcher.add_handler(wprice_handler)
        dispatcher.add_handler(webapp_handler)
        dispatcher.add_handler(pause_handler)
        dispatcher.add_handler(bot_handler)
        dispatcher.add_handler(webapppause_handler)
        dispatcher.add_handler(botpause_handler)
        dispatcher.add_handler(sellingpause_handler)
        dispatcher.add_handler(printscreen_handler)
        dispatcher.add_handler(up_handler)
        dispatcher.add_handler(newprice_handler)
        dispatcher.add_handler(down_handler)
        dispatcher.add_handler(right_handler)
        dispatcher.add_handler(left_handler)
        dispatcher.add_handler(rt_handler)
        dispatcher.add_handler(lt_handler)
        dispatcher.add_handler(rb_handler)
        dispatcher.add_handler(lb_handler)
        dispatcher.add_handler(a_handler)
        dispatcher.add_handler(b_handler)
        dispatcher.add_handler(y_handler)
        dispatcher.add_handler(x_handler)
        self.updater.start_polling()
        self.updater.idle()

    #################### other way
    def telegram_bot_sendtext(self, bot_message):
        bot_token = '1091873086:AAG3Zas2Tx3egjq0odjx8aydt3fkfsbpHWA'
        bot_chatID = '1310706288'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)

        return response.json()


    def telegram_bot_sendtextSTATUS(self,bot_message):
        bot_token = '1127221085:AAFvvkHoXa6eCtI3HtEmJN0Sxcx4IWOkrRc'
        bot_chatID = '1310706288'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)

        return response.json()

    #def bot2(self):
    #    image = pyautogui.screenshot()
    #    image = np.array(image)
    #    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #    cv2.imwrite('printscreen.png', image)
#
#
#        bot = telegram.Bot(token='1127221085:AAFvvkHoXa6eCtI3HtEmJN0Sxcx4IWOkrRc')
#        update = telegram.Update.de_json(request.get_json(force=True), bot)
#        chat_id = update.message.chat.id
##        msg_id = update.message.message_id
#        bot.sendPhoto(chat_id=chat_id, photo=image, reply_to_message_id=msg_id)