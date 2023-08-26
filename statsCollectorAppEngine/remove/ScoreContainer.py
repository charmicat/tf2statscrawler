# coding=utf-8

class Data:
    def __init__(self, userName="", profileURL="", statValue=-1, iconURL=""):
        self.userName = userName
        self.profileURL = profileURL

        self.statValue = statValue
        self.statText = ""

        self.iconURL = iconURL

    def __repr__(self):
        return "User " + self.userName + " | profile: " + self.profileURL + " | statValue: %d" % self.statValue + " | statName:" + self.statText


class ScoreContainer:

    def __init__(self, selectedStats, selectedClasses):
        self.scoreByStat = dict()

        for stat in selectedStats:
            classData = dict()
            for c in selectedClasses:
                classData[c] = Data()

            self.scoreByStat[stat] = classData

    def __repr__(self):
        return self.scoreByStat.__repr__()
