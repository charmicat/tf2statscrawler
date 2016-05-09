import urllib, urllib2, cookielib

ageDay = '10'
ageMonth = 'January'
ageYear = '1980'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'ageDay' : ageDay, 'ageMonth' : ageMonth, 'ageYear' : ageYear})
resp1 = opener.open('http://store.steampowered.com/agecheck/app/8980/', login_data)
resp = opener.open('http://store.steampowered.com/app/8980/')
print resp.read()
