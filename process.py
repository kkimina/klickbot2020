import requests
import hashlib
import time
from imagesearch import *
import json
import pytesseract
from telegram.ext import Updater
from telegram.ext import CommandHandler
#from test import *
#
#def unknown(update, context):
#    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
#
#def printscreen(update, context):
#    image = pyautogui.screenshot()
#    image = np.array(image)
#    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#    cv2.imwrite('printscreen.png', image)
#    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))
#
#
#def up(update, context):
#    image = pyautogui.screenshot()
#    image = np.array(image)
#    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#    cv2.imwrite('printscreen.png', image)
#    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('printscreen.png', 'rb'))
#
#def other_bot():
#    updater = Updater(token='1091873086:AAG3Zas2Tx3egjq0odjx8aydt3fkfsbpHWA', use_context=True)
#    start_handler = CommandHandler('start', unknown)
#    printscreen_handler = CommandHandler('printscreen', printscreen)
#    up_handler = CommandHandler('up', up)
#    dispatcher = updater.dispatcher
#    dispatcher.add_handler(start_handler)
#    dispatcher.add_handler(printscreen_handler)
#    dispatcher.add_handler(up_handler)
#    updater.start_polling()
#    updater.idle()
#

def telegram_bot_sendtext(bot_message):
    bot_token = '1091873086:AAG3Zas2Tx3egjq0odjx8aydt3fkfsbpHWA'
    bot_chatID = '1310706288'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def get_color(coord, ):
    image = pyautogui.screenshot()
    image = np.array(image)
    #coord = [ 362,1121]
    col = [250, 84, 97]
    print( str(image[coord[0], coord[1], 0] - col[0])+',' +
            str(image[coord[0], coord[1], 1] - col[1])+',' +
            str(image[coord[0], coord[1], 2] - col[2]))

    #image[coord[0], coord[1]][0] = 0
    #image[coord[0], coord[1]][1] = 0
    #image[coord[0], coord[1]][2] = 0

    #cv2.imshow('a', image)
    #cv2.waitKey()

def get_color_row():
    count = 0
    image = pyautogui.screenshot()
    image = np.array(image)
    for r in range(1403, 1848):
        coord1 = [320, r]
        coord2 = [320, r - 1]


        #if  #abs(image[coord1[0], coord1[1], 0] -image[coord2[0], coord2[1], 0]) > 200 and \
            #abs(image[coord1[0], coord1[1], 1] - image[coord2[0], coord2[1], 1]) > 200 and \
            #abs(image[coord1[0], coord1[1], 2] - image[coord2[0], coord2[1], 2]) < 200:
        #if 1:
        if image[coord2[0], coord2[1], 0] > 200 and \
           image[coord2[0], coord2[1], 1] > 200 and \
           image[coord2[0], coord2[1], 2] > 100 and image[coord2[0], coord2[1], 2] < 180:
            count = count +1



            #print(
            #    str(image[coord2[0], coord2[1], 0])
            #    + ',' +
            #    str(image[coord2[0], coord2[1], 1])
            #    + ',' +
            #    str(image[coord2[0], coord2[1], 2])
            #)

            #print( str(abs(image[coord1[0], coord1[1], 0] -image[coord2[0], coord2[1], 0]))+',' +
            #   str(abs(image[coord1[0], coord1[1], 1] -image[coord2[0], coord2[1], 1])) +',' +
            #   str(abs(image[coord1[0], coord1[1], 2] - image[coord2[0], coord2[1], 2])))

            #image[coord1[0], coord1[1]][0] = 0
            #image[coord1[0], coord1[1]][1] = 0
            #image[coord1[0], coord1[1]][2] = 0
    print(count)
    #cv2.imshow('a', image)
    #cv2.waitKey()

def tess(reg):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    path = r'C:\Users\Kimi\Desktop'
    template = cv2.imread(path + r'\\' + '100full' + '.PNG')
    image = pyautogui.screenshot(region=(reg[0], reg[1], reg[2], reg[3]))
    image = np.array(image)



    template = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(pytesseract.image_to_string(template))
    cv2.imshow('template', template)
    cv2.waitKey()
    return









#tess([1709, 117, 106, 39])
#get_coin_sell()
#while 1:
#while 1:
#    get_color([207, 1537])
#get_color([820, 280])
##telegram_bot_sendtext('WAZUP')
#while 1:
#    other_bot()