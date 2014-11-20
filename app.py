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
        c = request.form['city']
        s = request.form['state']
        if c == '' or s == '':
            flash('You must enter in both a city and a state!')
            return redirect(url_for('index'))
        else:
            res = ""
            c = c.title()
            s = s.upper()
            return redirect(url_for('condition', city = c, state = s))#condition(city,state)


alert = {'HUR':'Hurricane', 'TOR':'Tornado', 'TOW':'Tornado', 'WRN':'Thunderstorm', 'SEW':'Thunderstorm', 'WIN':'Winter Weather', 'FLO':'Flood', 'WAT':'Flood', 'WND':'Windy', 'SVR':'Severe Weather', 'HEA':'Heat', 'FOG':'Fog', 'SPE':'Special Weather', 'FIR':'Fire', 'VOL':'Volcanoe', 'HWW':'Hurricane'}
@app.route("/condition/<state>/<city>")
def condition(city,state):
    #weather stuff
    city = city.replace(" ","_")
    url="http://api.wunderground.com/api/e67a9f7ffa697198/alerts/q/%s/%s.json"
    url = url%(state, city)
    request = urllib2.urlopen(url)
    resultstring = request.read()
    result = json.loads(resultstring)
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
        url = url%(state, city)
        request = urllib2.urlopen(url)
        resultstring = request.read()
        result = json.loads(resultstring)
        try:
            tag = result['forecast']['simpleforecast']['forecastday'][0]['conditions']
        except:
            flash('Invalid city and state')
            return redirect(url_for('index'))
    url = "http://api.wunderground.com/api/e67a9f7ffa697198/conditions/q/%s/%s.json"
    url = url%(state, city)
    try:
        request = urllib2.urlopen(url)
    except:
        return render_template("error.html")
    resultstring = request.read()
    result = json.loads(resultstring)
    temp = result['current_observation']['temperature_string']
        #we can make this even more brolic if we do scrap more data like tempertaure (lows and highs), wind, humidity

    #tumblr stuff
    url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=6qjbDDaQ4vUogvpFIZ2UoaHuo6ykn1vMpjRYOdYOPCQI6dBw4K"
    tag2 = tag 
    if tag2 == "Partly Cloudy":
        tag2 = "Cloudy"
    if tag2 == "Cloudy" or tag2 == "Clear":
        tag2 = tag2 + "skies"
    url = url%(tag2)
    try:
        request = urllib2.urlopen(url)
    except:
        return render_template("error.html")
    resultstring = request.read()
    result = json.loads(resultstring)
    pictures = []
    for item in result['response']:
        try:
            pictures.append(item['photos'][0]['original_size']['url'])
        except:
            pass
    request.close()
    bgcolors = {'Cloudy':'darkgray', 'Partly Cloudy': 'gainsboro', 'Sunny':'yellow', 'Rain':'lightsteelblue', 'Snow':'snow', 'Clear':'lightskyblue', 'Windy':'whitesmoke', 'Thunderstorm':'gray'}
    try:
        color = bgcolors[tag]
    except:
        color = 'white'
    return render_template("condition.html",tag=tag,pictures=pictures,temp=temp, color = color)

if __name__=="__main__":
    app.debug=True
    app.run()
