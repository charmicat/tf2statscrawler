# coding=utf-8

class UserData:
    def __init__(self, user_name="", profile_url="", stat_value=-1, icon_url=""):
        self.userName = user_name
        self.profileURL = profile_url

        self.statValue = stat_value
        self.statText = ""

        self.iconURL = icon_url

    def __repr__(self):
        return "User " + self.userName + " | profile: " + self.profileURL + " | statValue: %d" % self.statValue + " | statName:" + self.statText


class ScoreContainer:

    def __init__(self, selected_stats, selected_classes):
        self.score_by_stat = dict()

        for stat in selected_stats:
            class_data = dict()
            for c in selected_classes:
                class_data[c] = UserData()

            self.score_by_stat[stat] = class_data

    def __repr__(self):
        return self.score_by_stat.__repr__()
