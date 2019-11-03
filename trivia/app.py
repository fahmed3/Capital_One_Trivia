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

#can't choose both early date and late date at once
#can't choose category

@app.route('/results', methods = ['GET', 'POST'])
def results():
    if request.method == 'POST':
        earliest = request.form.get('max_date')
        latest = request.form.get('min_date')
        category = request.form.get('category')
        difficulty = request.form.get('value')
    response = call_api(earliest, latest, category, difficulty)
    return render_template('results.html', response = response)
    
def call_api(e_date, l_date,category, difficulty):
    url = 'http://jservice.io/api/clues?max_date=%s&min_date=%s&value=%s' % (e_date, l_date, difficulty)
    #search through categories for relevant category's category id's
    #categories = get_id(category)
    #print(url)
    response = requests.get(url).json()
    return response

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(os.getenv('PORT') or 5000)
    IOLoop.instance().start()
    #app.run(debug = True)


