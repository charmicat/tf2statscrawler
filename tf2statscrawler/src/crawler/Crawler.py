# coding=utf-8

from ScoreContainer import ScoreContainer
from lxml.html import parse
from lxml.etree import HTMLParser
from time import strftime
from datetime import timedelta
from lxml.cssselect import CSSSelector

class Crawler:
    
    def __init__(self, selectedStats, selectedClasses):

        self.filledStats = {}
        self.selectedStats = selectedStats
        self.selectedClasses = selectedClasses
        
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
        divClasses = ",div.".join(self.selectedStats)
        
        statsURL = URL + "/stats/TF2"
        
        try:
            statsProfile = parse(statsURL).getroot()
        except IOError:
            # Usuario nao tem TF2!
            return
        
        foundStats = dict()
        cssselector = CSSSelector('div.className,div.' + divClasses)
        matching = cssselector.evaluate(statsProfile)

        for div in matching:

            if div.get("class") == 'className':
                className = div.text_content()

                if not self.selectedClasses[className]: # otimizar isso (?), so recuperar as classes necessarias 
                    continue
                if len(foundStats) != len(self.selectedStats):
                    print "Erro de parsing"
                    break
                else:
                    for st in foundStats:
                        currentClass = self.filledStats[st].statByClass[className]
                        
                        try:
                            if currentClass.statValue < foundStats[st]:
                                currentClass.statValue = foundStats[st]
                                currentClass.userName = userName
                                currentClass.profileURL = URL
                                currentClass.className = className
                            
                        except TypeError:
                            #comparando um inteiro com o LongestLife - gambiarra -_-
                            pass
            else:
                rawValue = div.text_content()
                
                cleanValue = rawValue.strip().replace(",", "")
                if cleanValue.find(":") == - 1:
                    valuePoints = int(cleanValue)
                else:
                    valuePoints = self.parseTime(cleanValue)
                
                foundStats[div.get("class")] = valuePoints

                    
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
            return strftime("%H:%M:%S", value)
        else:
            return value                   
    
    def parseTime(self, timeString):
        # TODO http://steamcommunity.com/id/ollithemagicbum/stats/TF2 LongestLife 3630:24 =(
        # usar timedelta!
#        parsedTimeString = timeString
#        format = "%M:%S"

        time = timedelta()
        
        toks = timeString.split(":")
        
        if len(toks) == 3:
            time = timedelta(hours=int(toks[0]), minutes=int(toks[1]), seconds=int(toks[2]))
        else:
            time = timedelta(minutes=int(toks[0]), seconds=int(toks[1]))
            
            
        return time
            
#        minutes = int(toks[0])
#        
#        if minutes >= 59:
#            hours = minutes / 60
#            minutes = minutes % 60
#            parsedTimeString = "%d:%d:%s" % (hours, minutes, toks[1])
#            format = "%H:%M:%S"
#            
#            
#        return strptime(parsedTimeString, format)
