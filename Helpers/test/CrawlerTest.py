import os
import unittest

from google.appengine.ext.webapp import template

from Helpers.crawler import Collector, Constants


class Collect(unittest.TestCase):
    def test_basic_crawling(self):
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

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
