# coding=utf-8

from lxml.html import parse
from lxml.etree import HTMLParser
from lxml.cssselect import CSSSelector
from lxml import etree

import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, http.cookiejar

from io import StringIO

class GameInfo:
    def __init__(self):
        self.price = 0
        self.url = ""

class PriceDataStructure:
    def __init__(self):
        self.userID = ""
        self.game_priceList = dict()
        self.totalPrice = 0
        
    def __repr__(self):
        str += self.userID + "\n\n"
        for k, v in self.game_priceList.items():
            str += k + ": " + v + "\n"
            
        str += "\nTotal: $%.2f" % self.totalPrice
        
        return str

class ValueCalculator:
    def __init__(self, profileURL):
        self.profileURL = profileURL
        
    def calculate(self):
        priceDS = PriceDataStructure()
        titles = dict()
        
        priceDS.userID = self.profileURL.rsplit("/", 1)[1]
        
        allGamesURL = self.profileURL + "/games?tab=all"
        
        ageDay = '10'
        ageMonth = 'January'
        ageYear = '1980'
    
        parser = HTMLParser(encoding='utf-8')
        page = parse(allGamesURL, parser).getroot()
        
        cssselector = CSSSelector('div.gameLogo a')
        userLinks = cssselector.evaluate(page)
        
        totalPrice = 0.0
    
        for link in userLinks:
            gameUrl = link.get("href")
            
            try:
                gamePage = parse(gameUrl, parser).getroot()
            except IOError: #page not found for some reason
                continue
            
            if gamePage.base.find("agecheck") != -1:
                cj = http.cookiejar.CookieJar()
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
                login_data = urllib.parse.urlencode({'ageDay' : ageDay, 'ageMonth' : ageMonth, 'ageYear' : ageYear})
                resp1 = opener.open(gamePage.base, login_data)
                resp = opener.open(gameUrl).read()
                
                htmlParser = etree.HTMLParser()
                gamePage = etree.parse(StringIO(resp), htmlParser)
            elif gamePage.base.find("app") == -1:
                continue
                 
            
            cssselector = CSSSelector('div#game_area_purchase h2:nth-child(0n+1)')
            excludeGame = cssselector.evaluate(gamePage)
            
            if len(excludeGame) > 0: #exclude games that only come in packages, can't be bought alone
                continue
            
            cssselector = CSSSelector('div.game_name')
            titleDiv = cssselector.evaluate(gamePage)
            
            repeat = 0
            
            title = titleDiv[0]
            for x in title.itertext():
                if len(x.strip()) > 0:
                    title = x.strip()
                    if title not in titles:
                        priceDS.game_priceList[title] = GameInfo()
                    else:
                        repeat = 1
                    
            if repeat == 1: #skip if the game is not unique
                continue
            
            # gotta find a way to capture the first price available, be it discounted or not
            cssselector = CSSSelector('div.game_purchase_price')
            priceDiv = cssselector.evaluate(gamePage)
    
            if len(priceDiv) == 0: #discounted game
                cssselector = CSSSelector('div.discount_original_price')
                priceDiv = cssselector.evaluate(gamePage)

            if len(priceDiv) == 0: #demos
                continue
            
            found = 0
            for div in priceDiv:
                found = found + 1
                
                if found == 1: #don't want the other prices, only the first one
                    priceDS.game_priceList[title].price = div.text.strip()
                    priceDS.game_priceList[title].url = gameUrl
                    
                    print(title + " - " + priceDS.game_priceList[title].price)
                        
                    price = div.text.strip().strip("$").strip(" USD")
                    try:
                        totalPrice = totalPrice + float(price)
                    except ValueError: #Free games have a "Free" price
                        priceDS.game_priceList.pop(title)
                        pass
                else:
                    break
        
        priceDS.totalPrice = totalPrice
        
        return priceDS
    
