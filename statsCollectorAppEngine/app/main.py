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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# import import_wrapper
# from Collector import Collector
from Helpers.crawler import Collector
from Helpers.crawler import Constants

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class MainHandler(webapp.RequestHandler):
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

        c = Collector(selected_stats, selected_classes)
        filled_stats = c.getStatsFromGroupProfile(self.groupURL)

        path = os.path.dirname(__file__) + '/interface/result.html'
        self.response.write(str(template.render(path, {"stats": filled_stats, "groupURL": group_url,
                                                       "statsName": Constants.availableStatsText})))


class ResultHandler(webapp.RequestHandler):

    def get(self):
        path = os.path.dirname(__file__) + '/interface/result.html'
        #        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(str(template.render(path, Constants.availableStats)))


application = webapp.WSGIApplication([('/', MainHandler), ('/results', ResultHandler)],
                                     debug=True)


def main():
    #     application = webapp.WSGIApplication([('/', MainHandler), ('/results', ResultHandler)],
    #                                        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
