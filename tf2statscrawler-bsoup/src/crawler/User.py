# coding=utf-8

class User:
    def __init__(self, userName="", profileURL="", className="", statValue=-1):
        self.userName = userName
        self.profileURL = profileURL
        self.className = className

        self.statValue = statValue

    def __repr__(self):
        return "User " + self.userName + " | profile: " + self.profileURL + " | statValue: %d" % self.statValue
