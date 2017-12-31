import requests, json


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


def getKrakenPairs():
    url = "https://api.kraken.com/0/public/AssetPairs"
    r = requests.get(url)

    print(r.text)



#getKrakenPairs()


conversion = input("Exchange: ")
getKraken(conversion)
