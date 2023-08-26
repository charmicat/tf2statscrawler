# coding=utf-8

#TODO: Longest Life esta com problemas por causa do formato de hora

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import SoupStrainer 
from ScoreContainer import ScoreContainer
import Constants
import urllib
import re
import copy
import time


class Crawler:
    
    def __init__(self, selectedStats, selectedClasses):

        self.filledStats = {}
        self.selectedStats = selectedStats
        self.selectedClasses = selectedClasses
        
        for stat in selectedStats:
            self.filledStats[stat] = ScoreContainer()
            
        self.URL = ""
        
    
    def getStatsFromGroupProfile(self, URL):
        self.URL = URL
        page = urllib.urlopen(URL).read()
        
        ss = SoupStrainer('a')
        bs = BeautifulSoup(page, parseOnlyThese=ss)
        
        userLinks = bs.findAll("a", {"class":"groupMemberLink"})
        
        for link in userLinks:
            self.getStatsFromUserProfile(link.attrs[2][1])
#            self.getStatsFromUserProfileOlde(link.attrs[2][1])
            
        return self.filledStats
            
        
    def getStatsFromUserProfileList(self, URLList):
        for url in URLlist:
            self.getStatFromUserProfile(url)

    
    def getStatsFromUserProfile(self, URL):
        divClasses = copy.copy(self.selectedStats) #copy pra divClasses nao referenciar o mesmo objeto -_-
        divClasses += ["className", "returnLink"]
        
        statsURL = URL + "/stats/TF2"
        statsProfile = urllib.urlopen(statsURL).read()
            
        ss = SoupStrainer('div', {"class":divClasses})
        statsBS = BeautifulSoup(statsProfile, parseOnlyThese=ss)
        
        userName = ""
        
        divs = statsBS.findAll("div", {"class":divClasses})
        
        foundStats = dict()
        for statVal in divs:
            if statVal.attrs[0][1] == 'className':
                className = statVal.decodeContents().strip()
                if not self.selectedClasses[className]:
                    continue
                if len(foundStats) != len(self.selectedStats):
                    print "Erro no parsing"
                    break
                else:
                    for st in foundStats:
                        currentClass = self.filledStats[st].statByClass[className]
                        if currentClass.statValue < foundStats[st]:
                            currentClass.statValue = foundStats[st]
                            currentClass.userName = userName
                            currentClass.profileURL = URL
                            currentClass.className = className
            elif statVal.attrs[0][1] == 'returnLink':
                rawName = statVal.a.contents[0]
                userName = rawName.replace("Return to ", "")
                userName = userName.replace("'s profile", "")
                statVal.a.extract()
            else:
                rawValue = statVal.findAllNext(text=True, limit=1)[0]
                
                cleanValue = rawValue.strip().replace(",", "")
                if cleanValue.find(":") == - 1:
                    valuePoints = int(cleanValue)
                else:
                    valuePoints = self.parseTime(cleanValue)
                    
                foundStats[statVal.attrs[0][1]] = valuePoints
        

                    
    def getStatsFromUserProfileOlde(self, URL):
        divClasses = copy.copy(self.selectedStats) #copy pra divClasses nao referenciar o mesmo objeto -_-
        divClasses += ["className", "returnLink"]
        
        statsURL = URL + "/stats/TF2"
        statsProfile = urllib.urlopen(statsURL).read()
            
        ss = SoupStrainer(['div', 'h2', 'h1'])
        statsBS = BeautifulSoup(statsProfile, parseOnlyThese=ss)
        
        userName = ""
        try:
            userName = statsBS.find(text='Team Fortress 2 Stats').findNext('h1').contents[0]
        except AttributeError:
            #usuario nao tem TF2!
            pass
        
        # checando se userName é o melhor em cada stat
        # TODO: melhorar isso, seria melhor pegar todos os stats de uma vez, nao fazer uma busca
        # diferente pra cada stat
        for currentStat in self.filledStats.keys():
            className = ""
            valuePoints = 0
            
            for statVal in statsBS.findAll("div", {"class":[currentStat, "className"]}):
            
                if statVal.attrs[0][1] == currentStat:
                    rawValue = statVal.findAllNext(text=True, limit=1)[0]
                    cleanValue = rawValue.strip().replace(",", "")
                    
                    if cleanValue.find(":") == - 1:
                        valuePoints = int(cleanValue)
                    else:
                        valuePoints = self.parseTime(cleanValue)
                                
                elif statVal.attrs[0][1] == 'className' and valuePoints > 0:
                    className = statVal.decodeContents().strip()
                    
                    if not self.selectedClasses[className]:
                        continue
                
                    classStat = self.filledStats[currentStat].statByClass[className]
                                    
                    if valuePoints > classStat.statValue:
                        classStat.statValue = valuePoints
                        classStat.userName = userName
                        classStat.profileURL = statsURL
                        
                        valuePoints = 0

    def printScore(self):
        print "Summary of stats for the group: " + self.URL
        print "\n"
        
        for stat in self.filledStats:
            print "*** Stat: " + stat
            print ""

            for classStats in self.filledStats[stat].statByClass:
                currentClass = self.filledStats[stat].statByClass[classStats]
                
                if currentClass.statValue != 0:
                    print "Class: " + classStats
                    print "User: " + currentClass.userName
                    print "Points: %s" % self.formatStatValue(currentClass.statValue)
                    print "URL: " + currentClass.profileURL
                    print ""
                
            print "-----------------------------"     
            
    def formatStatValue(self, value):
        if type(value).__name__ != "int":
            return time.strftime("%H:%M:%S", value)
        else:
            return value                   
    
    def parseTime(self, timeString):
        parsedTimeString = timeString
        format = "%M:%S"
        
        toks = timeString.split(":")
        minutes = int(toks[0])
        
        if minutes > 60:
            hours = minutes / 60
            minutes = minutes % 60
            parsedTimeString = "%d:%d:%s" % (hours, minutes, toks[1])
            format = "%H:%M:%S"
            
            
        return time.strptime(parsedTimeString, format)
        
        