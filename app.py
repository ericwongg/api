from flask import Flask, render_template, redirect
import json, urllib2

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")
        
@app.route("/t/<tag>")
def tag(city):
    state = list['city']
    url="http://api.wunderground.com/api/e67a9f7ffa697198/alerts/q/%s/%c.json"
    url = url%(city, state)
    request = urllib2.urlopen(url)
    resultstring = request.read()
    result = json.loads(resultstring)
    #getting the alert type
    atype = result['alerts']['type']
    request.close()

if __name__=="__main__":
    app.debug=True
    app.run()
    #app.run(host="0.0.0.0",port=8000)
