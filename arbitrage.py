import requests, json, itertools

#Class builds lists of rates, next build nonce checker and chron job, automatic trade executor and transaction calculator around below class

class Arbitrage:

    def __init__(self):
        self.rates = list()
        
        conversion = input("Enter currencies to exchange (ex. BTC-USD): ")
        #Build list of exchange rates
        rates.append(getCoinbase(conversion))
        rates.append(getKraken(conversion))
        rates.append(getBitfinex(conversion))

        #Compute
        bestRate()



    def getCoinbase(conversion):
        url = "https://api.coinbase.com/v2/prices/"
        r = requests.get(url + conversion + "/buy")  #Coinbase BTC-USD
        
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



    def getKraken(conversion):
        
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

    
    def getBitfinex(conversion):




    def bestRate():

        lowestBuy, highestSell = 0

        for i in range(len(rates)):
            if (rates[i][0] < rates[lowestBuy][0]):
                    lowestBuy = i

            if (rates[i][1] > rates[highestSell[1]):
                    highestSell = i

        gain = (float(rates[highestSell][1]) - float(rates[lowestBuy][0])) / float(rates[lowestBuy][0])

        buyAt = rates[lowestBuy][3]
        sellAt = rates[highestSell][3]

        print(gain, "% gain | Buy: ", buyAt, " | Sell: ", sellAt)

