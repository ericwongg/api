from flask import Flask, render_template, redirect, request
import json, urllib2

app=Flask(__name__)

@app.route("/")
def index():
    button = request.args.get("b",None)
    if button==None:
        return render_template("home.html")
    else:
        city = request.args.get("city",None)
        state = request.args.get("state",None)
        return condition(city,state)

alert = {'HUR':'Hurricane', 'TOR':'Tornado', 'TOW':'Tornado', 'WRN':'Thunderstorm', 'SEW':'Thunderstorm', 'WIN':'Winter Weather', 'FLO':'Flood', 'WAT':'Flood', 'WND':'Windy', 'SVR':'Severe Weather', 'HEA':'Heat', 'FOG':'Fog', 'SPE':'Special Weather', 'FIR':'Fire', 'VOL':'Volcanoe', 'HWW':'Hurricane'}
@app.route("/condition")
def condition(city,state):

    #weather stuff
    url="http://api.wunderground.com/api/e67a9f7ffa697198/alerts/q/%s/%s.json"
    url = url%(state, city)
    request = urllib2.urlopen(url)
    resultstring = request.read()
    result = json.loads(resultstring)
    if 'errors' in result:
        return render_template("error.html")
    else:
        #getting the alert type
        atype = result['alerts'][0]['type']
        request.close()

    if atype in alert:
        tag = alert[atype]
    else:
        tag = 'safe'

    #tumblr stuff
    url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=6qjbDDaQ4vUogvpFIZ2UoaHuo6ykn1vMpjRYOdYOPCQI6dBw4K"
    url = url%tag
    request = urllib2.urlopen(url)
    resultstring = request.read()
    result = json.loads(resultstring)
    pictures = result['response']
    request.close()

    return render_template("condition.html",tag,pictures)

if __name__=="__main__":
    app.debug=True
    app.run()
    #app.run(host="0.0.0.0",port=8000)
