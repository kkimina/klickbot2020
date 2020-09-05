from computer_vision import *
import threading
from test import *

class transfer_result():
    def __init__(self):
        self.result  = 0
        self.gekauft = 0
        self.blue = [62, 225, 237]
        self.pink = [250, 84, 97]
        self.black_ok = [0, 0, 0]
        self.search_mode = 0
        self.selling_mode = 0
        self.kaufen_mode = 0
        self.ok_mode = 0
        self.regions = {
            'normal': [0, 0, 0, 0, 0],
            'abgelaufen': [0, 0, 0, 0, 0],
            'kaufen_yes': [0, 0, 0, 0, 0],
            'transfermarkt_found': [0, 0, 0, 0, 0],
            'transfermarkt_nix': [0, 0, 0, 0, 0],
            'gekauft': [0, 0, 0, 0, 0],
            'selling1': [0, 0, 0, 0, 0],
            'transfers': [0, 0, 0, 0, 0],
            'verbrauch': [0, 0, 0, 0, 0],
            'anbieten1': [0, 0, 0, 0, 0],
            'extended': [0, 0, 0, 0, 0],
            'extended_safe': [0, 0, 0, 0, 0],
        }

        self.status_transfer = 0
        self.status_search = 0
        self.computer_vision = imagefun(self.regions)



        self.lucas = {
            'normal': [0, 0],
            'abgelaufen': [0, 0],
            'kaufen_yes': [0, 0],
            'transfermarkt_found': [0, 0],
            'transfermarkt_nix': [0, 0],
            'gekauft': [0, 0],
            'selling1': [0, 0],
            'transfers': [0, 0],
            'verbrauch': [0, 0],
            'anbieten1': [0, 0],
            'extended': [0, 0],
            'extended_safe': [0, 0],
        }


    def rundlauf(self, price):
        while 1:
            self.fillsearchfields()
            self.selling(price)
            self.kaufen()
            self.press_ok()

    def fillsearchfields(self):
        if self.search_mode is 1:
            self.get_pixel_command(regions['transfermarkt_found'][1] - 29, regions['transfermarkt_found'][0] + 135, 'down', self.pink)
            self.get_pixel_command(regions['transfermarkt_found'][1] - 123, regions['transfermarkt_found'][0] + 88, 'a',
                   [140, 144, 146])
            self.get_pixel_command(regions['transfermarkt_found'][1] + 26, regions['transfermarkt_found'][0] + 74, 'down', self.blue)
            press_button('left')
            press_button('y')
            self.search_mode = 0


    def selling(self, sell_price):
        if self.selling_mode is 1:
            self.get_pixel_command(regions['transfermarkt_found'][1] - 127, regions['transfermarkt_found'][0] + 534, 'down', self.pink)
            press_button('lt')
            self.get_pixel_command(regions['transfermarkt_found'][1] - 144, regions['transfermarkt_found'][0] + 519, 'up', self.pink)
            sleep(0.5)
            make_price(150, sell_price)
            self.get_pixel_command(regions['transfermarkt_found'][1] - 9, regions['transfermarkt_found'][0] + 590, 'up', self.pink)
            self.selling_mode = 0

    def kaufen(self):
        if self.kaufen_mode is 1 and self.regions['transfermarkt_found'][0] != 0:
            press_button('a')
            get_pixel_pink(self.regions['transfermarkt_found'][1] - 145, self.regions['transfermarkt_found'][0] + 477, 'nix')
            sleep(0.1)
            changes = {XboxOneControls.DOWN: ButtonState.PRESSED}
            send_message(DEFAULT_IP, DEFAULT_PORT, changes)
            sleep(0.1)
            changes = {XboxOneControls.A: ButtonState.PRESSED}
            send_message(DEFAULT_IP, DEFAULT_PORT, changes)
            changes[XboxOneControls.DOWN] = ButtonState.RELEASED
            send_message(DEFAULT_IP, DEFAULT_PORT, changes)
            sleep(0.05)
            changes[XboxOneControls.A] = ButtonState.RELEASED
            send_message(DEFAULT_IP, DEFAULT_PORT, changes)
            sleep(0.1)

            changes = {XboxOneControls.UP: ButtonState.PRESSED}
            send_message(DEFAULT_IP, DEFAULT_PORT, changes)
            sleep(0.05)
            changes = {XboxOneControls.A: ButtonState.PRESSED}
            send_message(DEFAULT_IP, DEFAULT_PORT, changes)
            changes[XboxOneControls.UP] = ButtonState.RELEASED
            send_message(DEFAULT_IP, DEFAULT_PORT, changes)
            sleep(0.05)
            changes[XboxOneControls.A] = ButtonState.RELEASED
            send_message(DEFAULT_IP, DEFAULT_PORT, changes)
            sleep(0.05)
            self.kaufen_mode = 0

    def proof_kauf(self):
        while 1:
            self.gekauft = self.computer_vision.suche_pics2('gekauft', 'abgelaufen')


    def press_ok(self):
        if self.ok_mode is 1:
            press_button('a')
            self.ok_mode = 0

    def lucas_search(self, input, savi1, savi2):
        safeInt = 0
        low_threshold = 6
        # params for ShiTomasi corner detection
        feature_params = dict(maxCorners=5000,
                              qualityLevel=0.01,
                              minDistance=1,
                              blockSize=10)

        # Parameters for lucas kanade optical flow
        lk_params = dict(winSize=(10, 10),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        save_string = ''
        if input is 2:
            save_string = savi2
        elif input is 1:
            save_string = savi1
        elif input is 0:
            return

        if (self.lucas[savi1][0] == 0 or self.lucas[savi2][0] == 0):
            if self.lucas[save_string][0] != 0:
                return
            # time.sleep(5)
            im = region_grabber(region=(1030, 0, 1843, 510))
            im = np.array(im)
            gray_frame_old = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            gray_frame_old = cv2.Canny(gray_frame_old, low_threshold, low_threshold * 3)
            self.lucas[save_string][1] = gray_frame_old
            self.lucas[save_string][0] = 1
            return
        else:
            gray_frame_old1 = self.lucas[savi1][1]
            gray_frame_old2 = self.lucas[savi2][1]

        p0_1 = cv2.goodFeaturesToTrack(gray_frame_old1, mask=None, **feature_params)
        p0_2 = cv2.goodFeaturesToTrack(gray_frame_old2, mask=None, **feature_params)

        for n in range(0, 500000):
            mask1 = np.zeros_like(gray_frame_old1)
            mask2 = np.zeros_like(gray_frame_old2)

            im2 = region_grabber(region=(1030, 0, 1843, 510))
            im2 = np.array(im2)
            frame_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.Canny(frame_gray, low_threshold, low_threshold * 3)

            # calculate optical flow
            p1_1, st_1, err = cv2.calcOpticalFlowPyrLK(gray_frame_old1, frame_gray, p0_1, None, **lk_params)
            p1_2, st_2, err = cv2.calcOpticalFlowPyrLK(gray_frame_old2, frame_gray, p0_2, None, **lk_params)
            # Select good points
            good_new1 = p1_1  # [st==1]
            good_old1 = p0_1  # [st==1]

            good_new2 = p1_2  # [st==1]
            good_old2 = p0_2

            # draw the tracks
            for i, (new, old) in enumerate(zip(good_new1, good_old1)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask1 = cv2.line(mask1, (a, b), (c, d), (255, 255, 255), 2)
            # img = cv2.add(frame, mask)

            for i, (new, old) in enumerate(zip(good_new2, good_old2)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask2 = cv2.line(mask2, (a, b), (c, d), (255, 255, 255), 2)
            # img = cv2.add(frame, mask)

            cv2.imshow('frame', mask1)
            cv2.imshow('frame2', mask2)

            diff1 = (good_new1 - good_old1) / 2
            diff2 = (good_new2 - good_old2) / 2
            feature1 = np.sum(np.absolute(diff1)) / diff1.shape[0]
            feature2 = np.sum(np.absolute(diff2)) / diff2.shape[0]

            if feature2 < 3:
                # print(feature2)
                return 2

            if feature1 < 5:
                # print(feature1)
                return 1
            safeInt = safeInt + 1
            if safeInt > 10000:
                print(savi1 + ' ' + feature1)
                print(savi2 + ' ' + feature2)
                return 0
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break

    def twoSearchLucas(self, first, second):
        if self.lucas[second][0] != 0 and self.lucas[first][0] != 0:
            test = self.lucas_search(3, first, second)
            if test is 2:
                nix = 2
            elif test is 1:
                nix = 1
            elif test is 0:
                return -1
        else:
            nix = self.computer_vision.suche_pics2(first, second)
            self.regions = self.computer_vision.get_regions()
            if self.lucas[second][0] == 0 or self.lucas[first][0] == 0:
                self.lucas_search(nix, first, second)
        return nix

    def searchsearch(self, c):
        while 1:
            #if regions['transfermarkt_found'][0] != 0:
                self.status_search = self.computer_vision.suche_pics2('extended', 'normal')
                self.regions = self.computer_vision.get_regions()
            #else:



    def transfersearch(self, c):
        while 1:
            if self.regions['transfermarkt_found'][0] == 0:

                self.status_transfer = self.twoSearchLucas('transfermarkt_nix', 'transfermarkt_found')

            else:

                self.status_transfer = self.computer_vision.pixel_compare(
                    [self.regions['transfermarkt_found'][1] - 41,
                     self.regions['transfermarkt_found'][0] + 350],
                    [self.regions['transfermarkt_found'][1] + 122,
                     self.regions['transfermarkt_found'][0] + 242], self.pink, self.black_ok, 5, 10)
            self.regions = self.computer_vision.get_regions()


    def write_result(self):
        while 1:
            self.status_transfer = self.computer_vision.pixel_compare(
                    [self.regions['transfermarkt_found'][1] - 41,
                     self.regions['transfermarkt_found'][0] + 350],
                    [self.regions['transfermarkt_found'][1] + 122,
                     self.regions['transfermarkt_found'][0] + 242], self.pink, self.black_ok, 5, 10)

    def transfersearch_thread(self, c):
        while 1:
            if self.regions['transfermarkt_found'][0] == 0:
                self.status_transfer = self.twoSearchLucas('transfermarkt_nix', 'transfermarkt_found')
                self.regions = self.computer_vision.get_regions()
            else:
                break
        t1 = threading.Thread(target=self.write_result())
        t1.start()


