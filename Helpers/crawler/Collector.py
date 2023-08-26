# coding=utf-8
import urllib.request
from datetime import timedelta

import lxml.etree
# from google.appengine.api import urlfetch
# from appengine_sdk.google_appengine.google.appengine.api import urlfetch

from Helpers.crawler.Data import Constants
from Helpers.crawler.ScoreContainer import ScoreContainer


# from lxml.html import parse
# from lxml.etree import XMLParser

class Collector:

    def __init__(self, selected_stats, selected_classes):
        self.quantitySelectedStats = len(selected_stats)

        self.totalUsers = 0
        self.totalUsersTF2 = 0

        self.onlySelectedClasses = dict()

        for i in selected_classes:
            self.onlySelectedClasses[i] = ""

        self.selectedStats = selected_stats

        self.filled_stats = ScoreContainer(self.selectedStats, self.onlySelectedClasses)

        self.URL = ""
        self.parser = lxml.etree.XMLParser(encoding='utf-8')

    def get_stats_from_group_profile(self, URL):
        self.URL = URL

        # result = urlfetch.fetch(URL + "/memberslistxml/?xml=1")
        with urllib.request.urlopen(URL + "/memberslistxml/?xml=1") as response:
            result = response.read()

        page = lxml.etree.fromstring(result, self.parser)

        total_pages = int(page.find("totalPages").text)

        self.totalUsers = page.find("memberCount").text

        for i in range(total_pages):
            # 1000 users per page, index starting at 0

            for userId in page.find("members"):
                self.get_stats_from_user_profile(userId.text)

            # result = urlfetch.fetch((URL + "/memberslistxml/?xml=1&p=%d") % i)
            with urllib.request.urlopen((URL + "/memberslistxml/?xml=1&p=%d") % i) as response:
                result = response.read()
            page = lxml.etree.fromstring(result, self.parser)

            self.printScore()

        return self.filled_stats

    def get_stats_from_user_profile_list(self, url_list):
        for url in url_list:
            self.get_stats_from_user_profile(url)

    def get_stats_from_user_profile(self, Id):
        stats_url = ("http://steamcommunity.com/profiles/%s/stats/tf2/?xml=1") % Id

        try:
            # result = urlfetch.fetch(stats_url)
            with urllib.request.urlopen(stats_url) as response:
                result = response.read()
            page = lxml.etree.fromstring(result, self.parser)

            privacy_state = page.find("privacyState")

            if privacy_state is None or privacy_state.text == "private":
                # User doesn't have TF2 or profile is private
                return

            self.totalUsersTF2 += 1

            all_classes_data = page.findall("stats/classData")

            for classData in all_classes_data:
                class_name = classData.find("className").text
                class_icon = classData.find("classIcon").text
                if class_name not in self.onlySelectedClasses:
                    # class must not be parsed
                    continue

                for stat in self.selectedStats:
                    try:
                        stat_data = int(classData.find(stat).text)
                        if self.filled_stats.score_by_stat[stat][class_name].statValue < stat_data:
                            self.filled_stats.score_by_stat[stat][class_name].statValue = stat_data

                            self.filled_stats.score_by_stat[stat][class_name].iconURL = class_icon
                            self.filled_stats.score_by_stat[stat][class_name].statText = Constants.availableStatsText[stat]

                            with urllib.request.urlopen("http://steamcommunity.com/profiles/%s/?xml=1" % Id) as response:
                                result = response.read()
                            # result = urlfetch.fetch("http://steamcommunity.com/profiles/%s/?xml=1" % Id)
                            profile = lxml.etree.fromstring(result.content, self.parser)

                            name = profile.find("steamID").text
                            self.filled_stats.score_by_stat[stat][class_name].userName = name
                            self.filled_stats.score_by_stat[stat][class_name].profileURL = ("http://steamcommunity.com/profiles/%s") % Id
                    except AttributeError:
                        pass

        except lxml.etree.XMLSyntaxError:
            print(stats_url)

    def printScore(self):
        print("Summary of stats for the group: " + self.URL)
        print("Total users: %s" % self.totalUsers)
        print("Total users who play TF2: %s" % self.totalUsersTF2)
        print("\n")

        for stat in self.filled_stats.score_by_stat:
            print(stat)
            print(self.filled_stats.score_by_stat[stat])

    def parseTime(self, time_string):
        time = timedelta()

        toks = time_string.split(":")

        if len(toks) == 3:
            time = timedelta(hours=int(toks[0]), minutes=int(toks[1]), seconds=int(toks[2]))
        else:
            time = timedelta(minutes=int(toks[0]), seconds=int(toks[1]))

        return time


if __name__ == '__main__':
    a = Collector(["iplaytime", "playtimeSeconds"], dict({"Soldier": True, "Spy": False, "Scout": False,
                                                          "Medic": False, "Engineer": True, "Demoman": False,
                                                          "Heavy": False, "Pyro": False, "Sniper": False}))
    a.get_stats_from_group_profile("http://steamcommunity.com/groups/sdstf2")
