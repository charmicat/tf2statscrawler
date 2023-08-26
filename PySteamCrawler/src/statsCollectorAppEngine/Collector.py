# coding=utf-8

from ScoreContainer import ScoreContainer
from datetime import timedelta

import lxml
import lxml.etree
#from lxml.html import parse
#from lxml.etree import XMLParser

class Collector:
    
    def __init__(self, selectedStats, selectedClasses):
        self.quantitySelectedStats = len(selectedStats)
                
        self.totalUsers = 0
        self.totalUsersTF2 = 0
        
        self.onlySelectedClasses = dict()
        
        for i in selectedClasses:
            self.onlySelectedClasses[i] = ""
                
        self.selectedStats = selectedStats
                
        self.filledStats = ScoreContainer(self.selectedStats, self.onlySelectedClasses)

        self.URL = ""
        self.parser = lxml.etree.XMLParser(encoding='utf-8')
        
    
    def getStatsFromGroupProfile(self, URL):
        self.URL = URL
        page = lxml.etree.parse(URL + "/memberslistxml/?xml=1", self.parser).getroot()
        
        totalPages = int(page.find("totalPages").text)
        
        self.totalUsers = page.find("memberCount").text
        
        for i in range(totalPages):
            #1000 users per page, index starting at 0
            
            for userId in page.find("members"):
                self.getStatsFromUserProfile(userId.text)

            page = lxml.etree.parse((URL + "/memberslistxml/?xml=1&p=%d") % i, self.parser).getroot()
        
#        self.printScore()
        
        return self.filledStats

        
    def getStatsFromUserProfileList(self, URLList):
        for url in URLList:
            self.getStatFromUserProfile(url)

    
    def getStatsFromUserProfile(self, Id):
        statsURL = ("http://steamcommunity.com/profiles/%s/stats/tf2/?xml=1") % Id
        
        page = lxml.etree.parse(statsURL, self.parser).getroot()
        
        privacyState = page.find("privacyState")
        
        if privacyState == None or privacyState.text == "private":
            # User doesn't have TF2 or profile is private
            return
        
        self.totalUsersTF2 += 1 
        
        allClassesData = page.findall("stats/classData")
        
        for classData in allClassesData:
            className = classData.find("className").text
            classIcon = classData.find("classIcon").text
            if className not in self.onlySelectedClasses: 
                # class must not be parsed
                continue
            
            for stat in self.selectedStats:
                statData = int(classData.find(stat).text)
                if self.filledStats.scoreByStat[stat][className].statValue < statData:
                    self.filledStats.scoreByStat[stat][className].statValue = statData
                    
                    self.filledStats.scoreByStat[stat][className].iconURL = classIcon
                    
                    profileURL = ("http://steamcommunity.com/profiles/%s/?xml=1") % Id
                    profile = lxml.etree.parse(profileURL, self.parser).getroot()
                    
                    name = profile.find("steamID").text
                    self.filledStats.scoreByStat[stat][className].userName = name
                    self.filledStats.scoreByStat[stat][className].profileURL = ("http://steamcommunity.com/profiles/%s") % Id
        

    def printScore(self):
        print("Summary of stats for the group: " + self.URL)
        print("Total users: %s" % self.totalUsers)
        print("Total users who play TF2: %s" % self.totalUsersTF2)
        print("\n")
        
        for stat in self.filledStats.scoreByStat:
            print(stat)
            print(self.filledStats.scoreByStat[stat])
        
            
    def parseTime(self, timeString):
        time = timedelta()
        
        toks = timeString.split(":")
        
        if len(toks) == 3:
            time = timedelta(hours=int(toks[0]), minutes=int(toks[1]), seconds=int(toks[2]))
        else:
            time = timedelta(minutes=int(toks[0]), seconds=int(toks[1]))
            
        return time
    
if __name__ == '__main__':
    a = Collector(["iplaytime", "playtimeSeconds"], dict({"Soldier":True, "Spy":False, "Scout":False,
                   "Medic":False, "Engineer":True, "Demoman":False,
                   "Heavy":False, "Pyro":False, "Sniper":False}))
    a.getStatsFromGroupProfile("http://steamcommunity.com/groups/sdstf2")
