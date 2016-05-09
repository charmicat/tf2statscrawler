# coding=utf-8

class User:
    def __init__(self, userName="", profileURL="", statValue=-1):
        self.userName = userName
        self.profileURL = profileURL
        
        self.statValue = statValue
        
    def __repr__(self):
        return "User "+self.userName+ " | profile: " + self.profileURL + " | statValue: %d" % self.statValue
