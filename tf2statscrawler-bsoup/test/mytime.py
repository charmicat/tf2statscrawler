# coding=utf-8
import time

def main():
    timeS1 = "95:23"
    timeS2 = "63:20"
    
    pTime1 = parseTime(timeS1)
    pTime2 = parseTime(timeS2)
    
    if pTime1 > pTime2:
        print "time 1 é maior"
    else:
        print "time 2 é maior"
        
    print type(pTime1)
    


def parseTime(timeString):
    parsedTimeString = timeString
    format = "%M:%S"
        
    toks = timeString.split(":")
    minutes = int(toks[0])
        
    if minutes > 60:
        hours = minutes / 60
        minutes = minutes % 60
        parsedTimeString = "%02d:%d:%s" % (hours, minutes, toks[1])
        format = "%H:%M:%S"
            
    return time.strptime(parsedTimeString, format)


if __name__ == "__main__":
    main()