from test import *

class bundle():
    def __init__(self, pink, blue, black_ok):
        self.pink               = pink
        self.blue               = blue
        self.black_ok           = black_ok
        self.search_mode        = 0
        self.selling_mode       = 0
        self.kaufen_mode        = 0
        self.ok_mode            = 0


    def get_pixel_command(self, x, y, command, color):
        sicherheit = 0
        while 1:
            image = pyautogui.screenshot()
            image = np.array(image)

            coord2 = [x, y]
            if get_pixel_diff(image, coord2, color, 5):
                return
            else:
                if sicherheit < 10:
                    if command != 'nix':
                        press_button(command)
                        sleep(1)
                    sicherheit = sicherheit + 1
                else:
                    print('pink ' + str(image[coord2[0], coord2[1], 0] - color[0]) + ',' +
                          str(image[coord2[0], coord2[1], 1] - color[0]) + ',' +
                          str(image[coord2[0], coord2[1], 2] - color[0]))





