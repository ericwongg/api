from flask import Flask, render_template, redirect, request, url_for, flash
import json, urllib2

app=Flask(__name__)
app.secret_key = 'dont_tell'

@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        button = request.form['b']
        city = request.form['city']
        state = request.form['state']
        if city == '' or state == '':
            flash('You must enter in both a city and a state!')
            return redirect(url_for('index'))
        else:
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
    print result
    if 'errors' in result:
        return render_template("error.html")
    else:
        #getting the alert type
        try:
            atype = result['alerts'][0]['type']
        except:
            atype = "NONE"
        request.close()

    if atype in alert:
        tag = alert[atype]
    else:
        #get forecast
        url="http://api.wunderground.com/api/e67a9f7ffa697198/forecast/q/%s/%s.json"
        url = url%(state,city)
        request = urllib2.urlopen(url)
        resultstring = request.read()
        result = json.load(resultstring)
        tag = result['simpleforecast']['forecastday'][0]['conditions']
        #we can make this even more brolic if we do scrap more data like tempertaure (lows and highs), wind, humidity

    #tumblr stuff
    url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=6qjbDDaQ4vUogvpFIZ2UoaHuo6ykn1vMpjRYOdYOPCQI6dBw4K"
    url = url%(tag)
    request = urllib2.urlopen(url)
    resultstring = request.read()
    result = json.loads(resultstring)
    #pictures = result['response']
    pictures = []
    for item in result['response']:
        try:
            pictures.append(item['photos'][0]['original_size']['url'])
        except:
            pass
    request.close()

    return render_template("condition.html",tag=tag,pictures=pictures)

if __name__=="__main__":
    app.debug=True
    app.run()
