import requests, json, itertools, bisect

#Class builds lists of rates, next build nonce checker and chron job, automatic trade executor and transaction calculator around below class

class Arbitrage:

    rates = None

    def getCoinbase(self, conversion):
        url = "https://api.coinbase.com/v2/prices/"
        r = requests.get(url + conversion + "/buy")  #Coinbase BTC-USD

        if (r.status_code != requests.codes.ok):
            return ("---", "---", "Coinbase")
        
        r = r.json()
    
        buy_price = r['data']['amount']
    
        r = requests.get(url + conversion + "/sell")

        if (r.status_code != requests.codes.ok):
            return ("---", "---", "Coinbase")

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
            return ("---", "---", "Kraken")

        r = r.json()

        if len(r["error"]) != 0:
            return ("---", "---", "Kraken")

        pairname = list(r["result"])[0]
        buy_price = r["result"][pairname]['a'][0]
        sell_price = r["result"][pairname]['b'][0]

        return (buy_price, sell_price, "Kraken")

    
    def getBitfinex(self, conversion):
        url = "https://api.bitfinex.com/v1/ticker/"

        convformat = conversion.replace('-', '')

        r = requests.get(url + convformat)
        
        if (r.status_code != requests.codes.ok):
            return ("---", "---", "Bitfinex")

        r = r.json()
        
        buy_price = r["ask"]
        sell_price = r["bid"]

        return (buy_price, sell_price, "Bitfinex")


    def getExmo(self, conversion):
        url = "https://api.exmo.com/v1/order_book/?pair="

        convformat = conversion.replace('-', '_')
        r = requests.get(url + convformat)

        
        if (r.status_code != requests.codes.ok or len(r.json()) == 0):
            return ("---", "---", "Exmo")

        r = r.json()
        
        buy_price = r[convformat]["ask_top"]
        sell_price = r[convformat]["bid_top"]

        if buy_price == 0 or sell_price == 0:
            return ("---", "---", "Exmo")

        return (buy_price, sell_price, "Exmo")

    
    def getCoinroom(self, conversion):
        url = "https://coinroom.com/api/ticker/"

        convformat = conversion.replace('-', '/')

        r = requests.get(url + convformat)

        if (r.status_code != requests.codes.ok or len(r.json()) == 0):
            return ("---", "---", "Coinroom")


        r = r.json()

        buy_price = r["ask"]
        sell_price = r["bid"]

        if buy_price == 0 or sell_price == 0:
            return ("---", "---", "Coinroom")

        return (buy_price, sell_price, "Coinroom")

    def getHitBTC(self, conversion):
        url = "https://api.hitbtc.com/api/2/public/ticker/"
        
        convformat = conversion.replace('-', '')

        r = requests.get(url + convformat)

        if (r.status_code != requests.codes.ok):
            return ("---", "---", "HitBTC")

        r = r.json()

        buy_price = r["ask"]
        sell_price = r["bid"]

        return (buy_price, sell_price, "HitBTC")

    
    def bestRate(self, rates):
       
        gains = list()

        for i in range(len(rates)):
            if rates[i][0] != "---":

                for j in range(len(rates)):
                    
                    if i != j and rates[j][0] != "---":
                        
                        gains_tup = (100 * (float(rates[j][1]) - float(rates[i][0])) / float(rates[i][0]), rates[i][2], rates[j][2])    #Tup:(percentage gain, exchange to buy at, exchange to sell at)
                        bisect.insort(gains, gains_tup)
        
        gains.reverse()     #Better table format
       
        return (gains)

    
    def printRates(self, rates, gains):
        #Potential Check
        if len(gains) < 2:
            print("Arbitrage not possible; try another currency pair.")
            return

        #Rates Table
        print("{0:^20s}|{1:^20s}|{2:^20s}".format("Exchange:", "Lowest Ask (Buy):", "Highest Bid (Sell):"))

        for i in range(len(rates)):
            if rates[i][0] != "---":
                print("{0:^20s}|{1:^20.6f}|{2:^20.6f}".format(rates[i][2], float(rates[i][0]), float(rates[i][1])))


        #Gains Table
        print("\n{0:^20s}|{1:^20s}|{2:^20s}".format("Buy At:", "Sell At:", "% Gain:"))
        
        for i in range(len(gains)):
            print("{1:^20s}|{2:^20s}|{0:^20.4f}".format(gains[i][0], gains[i][1], gains[i][2]))

        #Best Viable Trade
        gain = gains[0][0]
        buyAt = gains[0][1]
        sellAt = gains[0][2]

        print('\n', gain, "% gain | Buy: ", buyAt, " | Sell: ", sellAt)

    def trade_path(self, com):
        #Parses input as space separated values, last input is an optional trading value
        
        if not any(char.isdigit() for char in com):
            com += " 1"

        com_dup = com.split()
        records = []

        for i in range(len(com_dup) - 1):
            print(i, "/", len(com_dup ))
            if i == len(com_dup) - 2:
                print(com_dup[0], com_dup[i])
                records.append(self.getHitBTC(com_dup[0] + com_dup[i]))
            
            else:
                print(com_dup[i], com_dup[i + 1])
                records.append(self.getHitBTC(com_dup[i] + com_dup[i + 1]))

        change = float(com_dup[-1])

        for i in records:
            if i != records[-1]:
                change *= float(i[1])

            else:
                change /= float(i[0])

        print("Ending amount: ", change)


    def __init__(self):
        rates = list()
        
        conversion = input("Enter currencies to exchange (ex. BTC-USD): ")
        self.trade_path(conversion)
        return
        #Build list of exchange rates
        rates.append(self.getCoinbase(conversion))
        rates.append(self.getKraken(conversion))
        rates.append(self.getExmo(conversion))
        rates.append(self.getBitfinex(conversion))
        rates.append(self.getCoinroom(conversion))
        rates.append(self.getHitBTC(conversion))


        #Compute
        print(rates)
        gains = self.bestRate(rates)

        self.printRates(rates, gains)

while(True):
    Arbitrage()
