import logging
import os
import unittest

import requests
# from appengine_sdk.google_appengine.google.appengine.ext.webapp import template
from django import template
from django.template import Context

from Helpers.crawler.Collector import Collector
from Helpers.crawler.Data import Constants


class Collect(unittest.TestCase):
    def test_basic_crawling(self):
        # user_url = "http://steamcommunity.com/id/charmicat"
        # group_url = self.request.get("groupURL")
        # selected_stats = self.request.get_all("stat")
        # selected_classes = self.request.get_all("class")
        group_url = "http://steamcommunity.com/id/charmicat"
        selected_stats = "idamagedealt"
        selected_classes = "Demoman"

        user_id = "charmicat"

        if len(selected_stats) < 1 or len(selected_classes) < 1:
            # self.response.write("<center>You need to select at least one Class and one Stat!</center><br>")
            logging.info("<center>You need to select at least one Class and one Stat!</center><br>")
            return

        if user_id == "":
            # self.response.out.write("<center>You need to specify a group URL!</center><br>")
            logging.info("<center>You need to specify a user ID!</center><br>")
            return

        c = Collector(selected_stats, selected_classes)
        # filled_stats = c.get_stats_from_group_profile(self.group_url)
        filled_stats = c.get_stats_from_user_profile(user_id)
        self.assertIsNotNone(filled_stats)
        logging.info(filled_stats)

        path = os.path.dirname(__file__) + '/interface/result.html'
        # self.response.write(str(template.render(path, {"stats": filled_stats, "groupURL": group_url,
        #                                                "statsName": Constants.availableStatsText})))
        stats_data = Context()
        stats_data.render_context = {'stats': filled_stats, 'groupURL': group_url,
                                     'statsName': Constants.availableStatsText}
        data_template = template.Template.render(stats_data)
        logging.info(data_template)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
