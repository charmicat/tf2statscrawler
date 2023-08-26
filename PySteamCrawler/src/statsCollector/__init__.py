# coding=utf-8

import cProfile

import web

from . import Constants
from .Collector import Collector

render = web.template.render('interface/')

urls = (
    '/', 'index',
)
app = web.application(urls, globals())


class index:
    def GET(self):
        return render.index(Constants.availableStats, Constants.availableClasses)

    def POST(self):
        self.groupURL = ""
        selectedStats = []
        selectedClasses = []
        i = web.input()

        for tag, value in i.items():
            if value == "stat":
                selectedStats.append(tag)
            elif value == "class":
                selectedClasses.append(tag)
            elif tag == "groupURL":
                self.groupURL = value

        if len(selectedStats) < 1 or len(selectedClasses) < 1:
            return render.result("<center>You need to select at least one Class and one Stat!</center><br>")

        if self.groupURL == "":
            return render.result("<center>You need to specify a group URL!</center><br>")

        c = Collector(selectedStats, selectedClasses)
        self.filledStats = c.getStatsFromGroupProfile(self.groupURL)

        return render.result(self.groupURL, self.filledStats)


if __name__ == "__main__":
    app.run()


def main_profiling():
    import logging
    import cProfile, pstats, io
    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler('var/myapp.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    # This is the main function for profiling
    # We've renamed our original main() above to real_main()
    prof = cProfile.Profile()
    prof = prof.runctx("main()", globals(), locals())
    stream = io.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(10000)  # 80 = how many to print
    # The rest is optional.
    stats.print_callees()
    stats.print_callers()
    logger.info("Profile data:\n%s", stream.getvalue())


if __name__ == '__main__':
    cProfile.run(main_profiling())
#    app.run()
