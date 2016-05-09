# coding=utf-8

from ScoreContainer import ScoreContainer
import Constants
from datetime import timedelta

import lxml.etree
# from lxml.html import parse
# from lxml.etree import XMLParser

from google.appengine.api import urlfetch

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
        
        result = urlfetch.fetch(URL + "/memberslistxml/?xml=1")
        page = lxml.etree.fromstring(result.content, self.parser)
        
        totalPages = int(page.find("totalPages").text)
        
        self.totalUsers = page.find("memberCount").text
        
        for i in range(totalPages):
            # 1000 users per page, index starting at 0
            
            for userId in page.find("members"):
                self.getStatsFromUserProfile(userId.text)

            result = urlfetch.fetch((URL + "/memberslistxml/?xml=1&p=%d") % i)
            page = lxml.etree.fromstring(result.content, self.parser)
        
#        self.printScore()
        
        return self.filledStats

        
    def getStatsFromUserProfileList(self, URLList):
        for url in URLList:
            self.getStatFromUserProfile(url)

    
    def getStatsFromUserProfile(self, Id):
        statsURL = ("http://steamcommunity.com/profiles/%s/stats/tf2/?xml=1") % Id
        
        try:
            result = urlfetch.fetch(statsURL)
            page = lxml.etree.fromstring(result.content, self.parser)
            
            privacyState = page.find("privacyState")
        
            if privacyState == None or privacyState.text == "private":
            # User doesn't have TF2 or profile is private
                return
        
            self.totalUsersTF2 += 1 
        
            allClassesData = page.findall("stats/classData")
        
            for classData in allClassesData:
                className = classData.find("className").text
                classIcon = classData.find("classIcon").text
                if not self.onlySelectedClasses.has_key(className): 
                # class must not be parsed
                    continue
            
                for stat in self.selectedStats:
                    try:
                        statData = int(classData.find(stat).text)
                        if self.filledStats.scoreByStat[stat][className].statValue < statData:
                            self.filledStats.scoreByStat[stat][className].statValue = statData
                        
                            self.filledStats.scoreByStat[stat][className].iconURL = classIcon
                            self.filledStats.scoreByStat[stat][className].statText = Constants.availableStatsText[stat]
                        
                            result = urlfetch.fetch(("http://steamcommunity.com/profiles/%s/?xml=1") % Id)
                            profile = lxml.etree.fromstring(result.content, self.parser)
                        
                            name = profile.find("steamID").text
                            self.filledStats.scoreByStat[stat][className].userName = name
                            self.filledStats.scoreByStat[stat][className].profileURL = ("http://steamcommunity.com/profiles/%s") % Id
                    except AttributeError:
                        pass
                        
        except lxml.etree.XMLSyntaxError:
            print statsURL


    def printScore(self):
        print "Summary of stats for the group: " + self.URL
        print "Total users: %s" % self.totalUsers
        print "Total users who play TF2: %s" % self.totalUsersTF2
        print "\n"
        
        for stat in self.filledStats.scoreByStat:
            print stat
            print self.filledStats.scoreByStat[stat]
        
            
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
