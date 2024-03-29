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
import wsgiref.handlers

import Constants
from google.appengine.ext import webapp

# import import_wrapper
from Collector import Collector

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library

use_library('django', '1.2')

from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.dirname(__file__) + '/interface/index.html'
        self.response.out.write(
            template.render(path, {"stats": Constants.availableStats, "classes": Constants.availableClasses}))

    def post(self):
        groupURL = self.request.get("groupURL")
        selectedStats = self.request.get_all("stat")
        selectedClasses = self.request.get_all("class")

        if len(selectedStats) < 1 or len(selectedClasses) < 1:
            self.response.out.write("<center>You need to select at least one Class and one Stat!</center><br>")
            return

        if groupURL == "":
            self.response.out.write("<center>You need to specify a group URL!</center><br>")
            return

        c = Collector(selectedStats, selectedClasses)
        filledStats = c.getStatsFromGroupProfile(self.groupURL)

        path = os.path.dirname(__file__) + '/interface/result.html'
        self.response.out.write(template.render(path, {"stats": filledStats, "groupURL": groupURL}))


class ResultHandler(webapp.RequestHandler):

    def get(self):
        path = os.path.dirname(__file__) + '/interface/result.html'
        self.response.out.write(template.render(path, Constants.availableStats))


def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/results', ResultHandler)],
                                         debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
