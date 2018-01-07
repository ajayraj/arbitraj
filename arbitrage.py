import requests, json, itertools

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

    
    #def getBitfinex(conversion):

    def getExmo(self, conversion):
        url = "https://api.exmo.com/v1/order_book/?pair="

        convformat = conversion.replace('-', '_')
        r = requests.get(url + convformat)
        r = r.json()

        buy_price = r[convformat]["ask_top"]
        sell_price = r[convformat]["bid_top"]

        return(buy_price, sell_price, "Exmo")



    def bestRate(self):
       
        lowestBuy = 0
        highestSell = 0

        for i in range(len(self.rates)):
            if (rates[i][0] < rates[lowestBuy][0]):
                    lowestBuy = i

            if (rates[i][1] > rates[highestSell][1]):
                    highestSell = i

        gain = (float(rates[highestSell][1]) - float(rates[lowestBuy][0])) / float(rates[lowestBuy][0])

        buyAt = rates[lowestBuy][3]
        sellAt = rates[highestSell][3]

        print(gain, "% gain | Buy: ", buyAt, " | Sell: ", sellAt)



    def __init__(self):
        rates = list()
        
        conversion = input("Enter currencies to exchange (ex. BTC-USD): ")
        #Build list of exchange rates
        rates.append(self.getCoinbase(conversion))
        rates.append(self.getKraken(conversion))
        rates.append(self.getExmo(conversion))
        print(rates)
        #rates.append(self.getBitfinex(conversion))

        #Compute
        #self.bestRate()



Arbitrage()
