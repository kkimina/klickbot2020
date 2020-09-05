import requests
import time


class fifacoins():
    def __init__(self):
        self.status = 'keine Angabe'

    def getdata(self):
        while 1:
            try:
                output = requests.get('https://www.fifacoin.com/sell?platform=xboxone&dt=cash/').text
                if output.__contains__(
                        'There are not any players available now, please click Reload a few minutes later') is False:
                    self.status = 'verkauf moeglich'
                else:
                    self.status = 'verkauf nicht moeglich'
                time.sleep(10)
            except:
                print('error by ')