import urllib2
import json


url = """

"""

web = urllib2.urlopen(url)
res = web.read()
data = json.loads(res)

def getinfo():
    result = data[][]
