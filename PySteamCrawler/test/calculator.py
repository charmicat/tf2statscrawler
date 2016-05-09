# coding=utf-8

from lxml.html import parse
from lxml.etree import HTMLParser
from lxml.cssselect import CSSSelector
from lxml import etree

import urllib, urllib2, cookielib

import string
from StringIO import StringIO

def main():
    URL = "http://steamcommunity.com/id/viniciusfs"
    allGamesURL = URL + "/games?tab=all"
    
    ageDay = '10'
    ageMonth = 'January'
    ageYear = '1980'

    parser = HTMLParser(encoding='utf-8')
    page = parse(allGamesURL, parser).getroot()
    
    cssselector = CSSSelector('div.gameLogo a')
    userLinks = cssselector.evaluate(page)
    
    titles = dict()
    
    totalPrice = 0.0

    for link in userLinks:
        gameUrl = link.get("href")
        
        gamePage = parse(gameUrl, parser).getroot()
        
        if gamePage.base.find("agecheck") != -1:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            login_data = urllib.urlencode({'ageDay' : ageDay, 'ageMonth' : ageMonth, 'ageYear' : ageYear})
            resp1 = opener.open(gamePage.base, login_data)
            resp = opener.open(gameUrl).read()
            
            htmlParser = etree.HTMLParser()
            gamePage = etree.parse(StringIO(resp), htmlParser)
            
        cssselector = CSSSelector('title')
        title = cssselector.evaluate(gamePage)
        
        repeat = 0
        for a in title:
            title = a.text.replace(" on Steam", "")
            if not titles.has_key(title):
                print title
                titles[title] = 1;
            else:
                repeat = 1
                
        if repeat == 1: #skip if the game is not unique
            continue

        cssselector = CSSSelector('div.game_purchase_price')
        priceDiv = cssselector.evaluate(gamePage)
        
        found = 0
        for div in priceDiv:
            found = found + 1
            
            if found == 1: #don't want the other prices, only the first one
                price = div.text.strip().strip("$").strip(" USD")
                print price
                try:
                    totalPrice = totalPrice + float(price)
                except ValueError: #Free games have a "Free" price
                    pass
            else:
                break
        
    print "Total value %f2" % totalPrice
            
if __name__ == '__main__':
    main()
    
