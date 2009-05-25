# coding=utf-8

class User:
    def __init__(self, userName="", profileURL="", className="", statValue=0):
        self.userName = userName
        self.profileURL = profileURL
        self.className = className
        
        self.statValue = statValue
        
    def __repr__(self):
        return "User "+self.userName+ " | statValue: %s " % self.statValue
