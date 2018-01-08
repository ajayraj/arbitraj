import requests, json, itertools, bisect

#Class builds lists of rates, next build nonce checker and chron job, automatic trade executor and transaction calculator around below class

class Arbitrage:

    rates = None

    def getCoinbase(self, conversion):
        url = "https://api.coinbase.com/v2/prices/"
        r = requests.get(url + conversion + "/buy")  #Coinbase BTC-USD
        print(conversion)
        if (r.status_code != requests.codes.ok):
            print("Requests error: ", r.status_code)
            exit()
        
        r = r.json()
    
        buy_price = r['data']['amount']
    
        r = requests.get(url + conversion + "/sell")

        if (r.status_code != requests.codes.ok):
            print("Requests error: ". r.status_code)
            exit()

        r = r.json()

        sell_price = r['data']['amount']

        return (buy_price, sell_price, "Coinbase")



    def getKraken(self, conversion):
        
        url = "https://api.kraken.com/0/public/Ticker"
        
        convformat = conversion.replace('BTC', 'XBT')   #Uses XBT, Kraken's own code for BTC
        convformat = convformat.replace('-', '')
        params = {'pair':convformat}
        r = requests.get(url, params)

        if (r.status_code != requests.codes.ok):
            print("Requests error: ", r.status_code)
            exit()


        r = r.json()

        pairname = list(r["result"])[0]
        buy_price = r["result"][pairname]['a'][0]
        sell_price = r["result"][pairname]['b'][0]

        return (buy_price, sell_price, "Kraken")

    
    def getBitfinex(self, conversion):
        url = "https://api.bitfinex.com/v1/ticker/"

        convformat = conversion.replace('-', '')

        r = requests.get(url + convformat).json()
        
        buy_price = r["ask"]
        sell_price = r["bid"]

        return (buy_price, sell_price, "Bitfinex")


    def getExmo(self, conversion):
        url = "https://api.exmo.com/v1/order_book/?pair="

        convformat = conversion.replace('-', '_')
        r = requests.get(url + convformat).json()

        buy_price = r[convformat]["ask_top"]
        sell_price = r[convformat]["bid_top"]

        return (buy_price, sell_price, "Exmo")

    
    def getCoinroom(self, conversion):
        url = "https://coinroom.com/api/ticker/"

        convformat = conversion.replace('-', '/')

        r = requests.get(url + convformat).json()

        buy_price = r["ask"]
        sell_price = r["bid"]

        print(buy_price)
        print(sell_price)

        return (buy_price, sell_price, "Coinroom")


    def bestRate(self, rates):
       
        gains = list()


        print("{0:^20s}|{1:^20s}|{2:^20s}".format("Exchange:", "Lowest Ask (Buy):", "Highest Bid (Sell):"))


        for i in range(len(rates)):

            for j in range(len(rates)):

                if i != j:

                    gains_tup = (100 * (float(rates[j][1]) - float(rates[i][0])) / float(rates[i][0]), rates[i][2], rates[j][2])    #Tup:(percentage gain, exchange to buy at, exchange to sell at)
                    bisect.insort(gains, gains_tup)


            print("{0:^20s}|{1:^20.6f}|{2:^20.6f}".format(rates[i][2], float(rates[i][0]), float(rates[i][1])))

        
        gains.reverse()     #Better table format
        gain = gains[0][0]

        print("\n{0:^20s}|{1:^20s}|{2:^20s}".format("Buy At:", "Sell At:", "% Gain:"))

        for i in range(len(gains)):
            print("{1:^20s}|{2:^20s}|{0:^20.4f}".format(gains[i][0], gains[i][1], gains[i][2]))

        buyAt = gains[0][1]
        sellAt = gains[0][2]

        print('\n', gain, "% gain | Buy: ", buyAt, " | Sell: ", sellAt)



    def __init__(self):
        rates = list()
        
        conversion = input("Enter currencies to exchange (ex. BTC-USD): ")
        #Build list of exchange rates
        rates.append(self.getCoinbase(conversion))
        rates.append(self.getKraken(conversion))
        rates.append(self.getExmo(conversion))
        rates.append(self.getBitfinex(conversion))
        rates.append(self.getCoinroom(conversion))
        #self.getCoinroom(conversion)


        #Compute
        print(rates)
        self.bestRate(rates)

while(True):
    Arbitrage()
