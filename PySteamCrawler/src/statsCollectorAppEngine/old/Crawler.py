# coding=utf-8

from ScoreContainer import ScoreContainer
from lxml.html import parse
from lxml.etree import HTMLParser
from datetime import timedelta
from lxml.cssselect import CSSSelector

class Crawler:
    
    def __init__(self, selectedStats, selectedClasses):

        self.filledStats = {}
        self.selectedClasses = selectedClasses
        self.quantitySelectedStats = len(selectedStats)
                
        self.divClasses = ",div.".join(selectedStats)
        
        self.totalUsers = 0
        self.totalUsersTF2 = 0
        
        for stat in selectedStats:
            self.filledStats[stat] = ScoreContainer()
            
        self.URL = ""
        
    
    def getStatsFromGroupProfile(self, URL):
        parser = HTMLParser(encoding='utf-8')
        self.URL = URL
        page = parse(URL + "/members", parser).getroot()
        
        cssselector = CSSSelector('a.linkFriend_offline,a.linkFriend_online,a.linkFriend_in-game')
        userLinks = cssselector.evaluate(page)

        for link in userLinks:
            self.getStatsFromUserProfile(link.get('href'), list(link.itertext())[0])
            
        visited = dict()
        
        cssselector = CSSSelector("div.pageLinks a")
        multiplePages = cssselector.evaluate(page)
        
        
        # Problema: links nao estao todos aparentes <<  Page: 1 ... 3  4  5  6  7 ... 13 >>
        # possivel solucao: dividir numero de jogadores por 51 = numero de paginas, isso é bom pra otimizacao

        for pages in multiplePages:
            pageNumber = pages.get('href')
            if not pageNumber in visited:
                visited[pageNumber] = True
                subpage = parse(URL + "/members" + pageNumber, parser).getroot()
                
                cssselector = CSSSelector('a.linkFriend_offline,a.linkFriend_online,a.linkFriend_in-game')
                userLinks = cssselector.evaluate(subpage)
                
                for link in userLinks:
                    self.getStatsFromUserProfile(link.get('href'), list(link.itertext())[0])
                    
        return self.filledStats
            
        
    def getStatsFromUserProfileList(self, URLList):
        for url in URLlist:
            self.getStatFromUserProfile(url)

    
    def getStatsFromUserProfile(self, URL, userName):
        
        self.totalUsers += 1
        statsURL = URL + "/stats/TF2"
        
        try:
            statsProfile = parse(statsURL).getroot()
        except IOError:
            # Usuario nao tem TF2!
            return
        
        self.totalUsersTF2 += 1
        
        foundStats = dict()
        cssselector = CSSSelector('div.className,div.' + self.divClasses)
        matching = cssselector.evaluate(statsProfile)

        for div in matching:
            currentDivClass = div.get("class")

            if currentDivClass == 'className':
                className = div.text_content()

                if not self.selectedClasses[className]: # otimizar isso (?), so recuperar as classes necessarias 
                    continue
                if len(foundStats) != self.quantitySelectedStats:
                    print("Erro de parsing")
                    break
                else:
                    for st in foundStats:
                        currentClass = self.filledStats[st].statByClass[className]
                        
                        if type(foundStats[st]).__name__ == "timedelta" and currentClass.statValue == - 1:
                            currentClass.statValue = timedelta()
                                
                        if currentClass.statValue < foundStats[st]:
                            currentClass.statValue = foundStats[st]
                            currentClass.userName = userName
                            currentClass.profileURL = URL
                            currentClass.className = className
                            
            else:
                rawValue = div.text_content()
                
                cleanValue = rawValue.strip().replace(",", "")
                if cleanValue.find(":") == - 1:
                    valuePoints = int(cleanValue)
                else:
                    valuePoints = self.parseTime(cleanValue)

                foundStats[currentDivClass] = valuePoints

    def printScore(self):
        print("Summary of stats for the group: " + self.URL)
        print("Total users: %s" % self.totalUsers)
        print("Total users who play TF2: %s" % self.totalUsersTF2)
        print("\n")
        
        for stat in self.filledStats:
            print("*** Stat: " + stat)
            print("")

            for classStats in self.filledStats[stat].statByClass:
                currentClass = self.filledStats[stat].statByClass[classStats]

                if currentClass.statValue != - 1:
                    print("Class: " + classStats)
                    print("User: " + currentClass.userName)
                    print("Points: %s" % currentClass.statValue)
                    print("URL: " + currentClass.profileURL)
                    print("")
                
            print("-----------------------------")
            
    def parseTime(self, timeString):
        time = timedelta()
        
        toks = timeString.split(":")
        
        if len(toks) == 3:
            time = timedelta(hours=int(toks[0]), minutes=int(toks[1]), seconds=int(toks[2]))
        else:
            time = timedelta(minutes=int(toks[0]), seconds=int(toks[1]))
            
        return time

