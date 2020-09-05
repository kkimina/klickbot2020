from subprocess import Popen
import threading, queue
import time
import cv2
from imagesearch import *
import os, re
from transfermarkt import *
from other_pages import *


blue = [62, 225, 237]
pink = [250, 84, 97]
black_ok = [0, 0, 0]





bot     = transfer_result()
selling = fifacoins()


t1 = threading.Thread(target=bot.transfersearch_thread, args=[1])
t2 = threading.Thread(target=bot.searchsearch, args=[1])
t3 = threading.Thread(target=selling.getdata)
t4 = threading.Thread(target=bot.rundlauf, args=[1000])
t5 = threading.Thread(target=bot.proof_kauf)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

while 1:
    if bot.kaufen_mode is 1 or bot.kaufen_mode is 1 or bot.search_mode is 1:
        pass
    else:
        if bot.status_transfer == 2:
            bot.kaufen_mode = 1
        elif bot.status_transfer == 1:
            bot.ok_mode = 1

        if bot.gekauft == 1:
            bot.ok_mode = 1


    #else:
        #print(bot.status_transfer)
        #print(bot.status_search)
    #print(selling.status)





#if bot.status_search == 2:
#    mini.search_mode = 1

#if gekauft ==:
#    mini.selling_mode = 1


#if transfer_gefunden == 1:
#    mini.selling_mode = 1

# if ok_mode












