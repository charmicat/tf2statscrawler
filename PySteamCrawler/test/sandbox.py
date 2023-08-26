# coding=utf-8

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import SoupStrainer 
from ScoreContainer import ScoreContainer
import urllib.request, urllib.parse, urllib.error
import re
import copy

def main():
#    URL = "http://steamcommunity.com/id/viniciusfs"
    URL = "http://steamcommunity.com/id/charmicat"
    statsURL = URL + "/stats/TF2"
    selectedStats = ["maxPoints", "maxDamage", "maxKills"]
    
    statsProfile = urllib.request.urlopen(statsURL).read()
           
    filledStats = {}
        
    for stat in selectedStats:
        filledStats[stat] = ScoreContainer()
        
    ss = SoupStrainer(['div', 'h2', 'h1'])
    statsBS = BeautifulSoup(statsProfile, parseOnlyThese=ss)
            
    userName = ""
    
    try:
        userName = statsBS.find(text='Team Fortress 2 Stats').findNext('h1').contents[0]
    except AttributeError:
        #usuario nao tem TF2!
        pass

    print(userName)
    divClasses = copy.copy(selectedStats) #copy pra divClasses nao referenciar o mesmo objeto -_-
    divClasses.append("className")
    
    foundStats = dict()
    for statVal in statsBS.findAll("div", {"class":divClasses}):
        print(statVal.attrs)
        if statVal.attrs[0][1] == 'className':
            className = statVal.decodeContents().strip()
            if len(foundStats) != len(selectedStats):
                break
            else:
                for st in foundStats:
                    if filledStats[st].statByClass[className].statValue < foundStats[st]:
                        filledStats[st].statByClass[className].statValue = foundStats[st]
            
            # verificar se ja pegou os outros stats
            # comparar com o ScoreContainer
        else:
            rawValue = statVal.findAllNext(text=True, limit=1)[0]
            valuePoints = int(rawValue.strip().replace(",", ""))
            foundStats[statVal.attrs[0][1]] = valuePoints
            
            
    print("Summary of stats for the group: " + URL)
    print("\n")
    
    for stat in filledStats:
        print("*** Stat: " + stat)
        print("")

        for classStats in filledStats[stat].statByClass:
            currentClass = filledStats[stat].statByClass[classStats]
            
            print("Class: " + classStats)
            print("User: " + currentClass.userName)
            print("Points: %s" % currentClass.statValue)
            print("URL: " + currentClass.profileURL)
            print("")
            
        print("-----------------------------")                        
    

if __name__ == '__main__':
    main()
    