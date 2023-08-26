#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import wsgiref

import webapp2
# from google.appengine.ext import webapp
from django import template

from Helpers.crawler.Data import Constants
from Helpers.crawler.Collector import Collector

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class MainHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.dirname(__file__) + '/interface/index.html'
        #        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(
            str(template.render(path, {"stats": Constants.availableStats, "classes": Constants.availableClasses})))

    def post(self):
        group_url = self.request.get("groupURL")
        selected_stats = self.request.get_all("stat")
        selected_classes = self.request.get_all("class")

        if len(selected_stats) < 1 or len(selected_classes) < 1:
            self.response.write("<center>You need to select at least one Class and one Stat!</center><br>")
            return

        if group_url == "":
            self.response.out.write("<center>You need to specify a group URL!</center><br>")
            return

        c = Collector(["iplaytime", "playtimeSeconds"], dict({"Soldier": True, "Spy": False, "Scout": False,
                                                              "Medic": False, "Engineer": True, "Demoman": False,
                                                              "Heavy": False, "Pyro": False, "Sniper": False}))
        filled_stats = c.get_stats_from_group_profile("http://steamcommunity.com/groups/sdstf2")

        # c = Collector(selected_stats, selected_classes)
        # filled_stats = c.get_stats_from_group_profile(self.groupURL)

        path = os.path.dirname(__file__) + '/interface/result.html'
        self.response.write(str(template.render(path, {"stats": filled_stats, "groupURL": group_url,
                                                       "statsName": Constants.availableStatsText})))


class ResultHandler(webapp2.RequestHandler):

    def get(self):
        path = os.path.dirname(__file__) + '/interface/result.html'
        #        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(str(template.render(path, Constants.availableStats)))


application = webapp2.WSGIApplication([('/', MainHandler), ('/results', ResultHandler)],
                                      debug=True)


def main():
    #     application = webapp.WSGIApplication([('/', MainHandler), ('/results', ResultHandler)],
    #                                        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
