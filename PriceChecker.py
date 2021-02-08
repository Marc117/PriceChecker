import sys

sys.path.append('')
import requests
from os import path
import datetime
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

URL = 'http://produkte.exclusive-networks.de/cgi/listen.cgi?ZXEU1734'

page = requests.get(URL, auth=HTTPBasicAuth('gast', ''))

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table', {'class': "drja"})


def getPriceFromWebsite(page_table):
    price = page_table.find_all_next('td')
    return float(price[13].text.strip().replace(".", "").replace(",",
                                                                 "."))  # first price is in the 13th td tag, then strip the "<td>" tags out, replace the "," to transform it into a float to make it comparable


def saveToFile(price):
    with open("logs.txt", 'w') as f:
        f.write(str(price) + " " + str(datetime.datetime.now()))


def getPriceFromFile():
    with open("logs.txt", 'r') as f:
        data = f.read().split(" ", 1)
    return data


if __name__ == '__main__':
    priceWebsite = getPriceFromWebsite(table)
    priceFile = -1
    if path.exists("logs.txt"):
        log_price_date = getPriceFromFile()
        priceFile = str(log_price_date[0])
        dateFile = datetime.datetime.strptime(log_price_date[1], '%Y-%m-%d %H:%M:%S.%f')

        if priceWebsite != float(priceFile):
            print("Preis hat sich geändert:")
        else:
            print("Preis hat sich nicht geändert:")

        print('Preis aus Log-Datei: ', priceFile)
        print('Zeitangabe aus Log-Datei: ', dateFile)
        print('Preis von der Website', priceWebsite)

        saveToFile(priceWebsite)

        input("Enter drücken um Programm zu beenden")
    else:
        print("Keine Log-Datei vorhanden. Neue Log-Datei mit aktuellem Preis erstellt.")
        print("Aktueller Preis: ", priceWebsite);
        saveToFile(priceWebsite)
        input("Enter drücken um Programm zu beenden")
