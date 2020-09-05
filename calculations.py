def calc_selling(sell_price, rest):
    times = 0

    if sell_price <= 1000:
        sell_price = sell_price - rest
        times = int((sell_price) / 50)
    else:
        sell_price = sell_price - rest

        #first_price = sell_price - 1000
        #times1 = int((1000 - anfang) / 50)
        #times = int(first_price / 100) +times1
        times = int(sell_price / 100)
    return times

