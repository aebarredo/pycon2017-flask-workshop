from flask import Flask, url_for

app = Flask(__name__)
app.config.from_object('config')


@app.route("/")
def index():
    return "Index sample at lesson2"


@app.route("/hello")
def hello_world():
    return "Hello World!"


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_world2(name=''):
    return 'Hi {}!'.format(name)


@app.route("/info")
def get_info():
    return "Info"

with app.test_request_context():
    print (url_for('get_info'))
    print (url_for('hello_world2'))
    print (url_for('hello_world2', name='juan'))
    print (url_for('hello_world'))
