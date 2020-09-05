import os

def myCmd():
    os.system('cmd /c "cd../../../../Program Files/GIMX & gimx --src 127.0.0.1:51914 -p COM3 --status  --subpos -c XOnePadUsb.xml --nograb"')

myCmd()