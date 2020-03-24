from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello Flask!<h1>'


@app.route('/hi')
@app.route('/hello', methods=['GET', 'POST'])
def say_hello():
    return '<h1>Hello Flask</h1>'


@app.route('/greet', defaults={'name': 'Beck'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' %name


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')
    return '<h1>Hello, %s!</h1>' %name


@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>'  %(2020 - year)


@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful'




