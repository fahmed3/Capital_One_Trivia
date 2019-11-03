import os

from flask import Flask, render_template, request
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import requests

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/results', methods = ['GET', 'POST'])
def results():
    if request.method == 'POST':
        earliest = request.form.get('min_date')
        latest = request.form.get('max_date')
        difficulty = request.form.get('value')
    response = call_api(earliest, latest, difficulty)
    return render_template('results.html', response = response)
    

#can't choose category
def call_api(min_date, max_date, difficulty):
    if(min_date == ""):
        min_date = "1984-09-10"
    if(max_date == ""):
        max_date = "2015-04-01"    
    url = "http://jservice.io/api/clues?min_date=%s&max_date=%s&value=%s" % (min_date, max_date, difficulty)
    #print(url)
    response = requests.get(url).json()
    return response

@app.route("/challenge", methods = ['GET', 'POST'])
def challenge():
    response = requests.get("http://jservice.io/api/random").json()[0]
    return render_template("challenge.html", response = response)

@app.route("/answer", methods = ['GET', 'POST'])
def answer():
    if request.method == 'POST':
        answer = request.form.get('answer')
        c_answer = request.form.get('c_answer')
    if answer.lower() == c_answer.lower():
        return render_template("answer.html",
                               correct=True,
                               c_answer = c_answer)
    else:
        #if wrong because time ran out
        if answer == "OUT_OF_TIME":
            return render_template("answer.html",
                                   correct=False,
                                   out_of_time=True,
                                   c_answer = c_answer)
        #answer submitted on time but wrong anyway
        return render_template("answer.html",
                               correct=False,
                               out_of_time=False,
                               c_answer = c_answer)
        

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(os.getenv('PORT') or 5000)
    IOLoop.instance().start()
    #app.run(debug = True)


