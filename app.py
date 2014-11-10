from flask import Flask, render_template, redirect
import json, urllib2

app=Flask(__name__)

@app.route("/")
def index():
    return "Please enter a tag into url with format '/t/what_city_you_want_the_weather_for'"

@app.route("/t/<tag>")
def tag(tag="NewYork"):
    #tag will be a city
    #maybe use dictionary of city:state
    #use tag to get city then put it into the url
    city = tag
    state = list['city']
    url="http://api.wunderground.com/api/e67a9f7ffa697198/geolookup/conditions/q/%s/%c.json"
    url = url%(city, state)
    request = urllib2.urlopen(url)
    resultstring = request.read()
    result = json.loads(resultstring)
    location = result['location']['city']
    temp_f = result['current_observation']['temp_f']
    print "Curent temperature in %s is: %s" % (location, temp_f)
    request.close()

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=8000)
