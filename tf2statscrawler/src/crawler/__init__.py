# coding=utf-8

from Crawler import Crawler
import cProfile

def real_main ():
    
    selectedStats = ["maxPoints", "maxDamage", "maxKills", "longestLife"]
    selectedClasses = dict({"Soldier":True, "Spy":True, "Scout":False,
                   "Medic":True, "Engineer":False, "Demoman":True,
                   "Heavy":False, "Pyro":False, "Sniper":True})
    
    
    c = Crawler(selectedStats, selectedClasses)
    c.getStatsFromGroupProfile("http://steamcommunity.com/groups/mixaobr")
#    c.getStatsFromGroupProfile("http://steamcommunity.com/groups/itsovergaming")
#    c.getStatsFromGroupProfile("http://steamcommunity.com/groups/blogcontinue")
    
    c.printScore()


def main():
    import logging
    import cProfile, pstats, StringIO
    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler('var/myapp.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

 # This is the main function for profiling 
 # We've renamed our original main() above to real_main()
    prof = cProfile.Profile()
    prof = prof.runctx("real_main()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(10000)  # 80 = how many to print
    # The rest is optional.
    stats.print_callees()
    stats.print_callers()
    logger.info("Profile data:\n%s", stream.getvalue())    
    
if __name__ == '__main__':
#    cProfile.run(main())
    main()
#    real_main()
