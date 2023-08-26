import http.cookiejar
import urllib.parse
import urllib.request

ageDay = '10'
ageMonth = 'January'
ageYear = '1980'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
login_data = urllib.parse.urlencode({'ageDay': ageDay, 'ageMonth': ageMonth, 'ageYear': ageYear})
resp1 = opener.open('http://store.steampowered.com/agecheck/app/8980/', login_data)
resp = opener.open('http://store.steampowered.com/app/8980/')
print(resp.read())
