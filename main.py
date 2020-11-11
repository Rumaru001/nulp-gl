from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index():
    return 'Tap <a href=\'/api/v1/hello-world-23\'>here</a> ' \
           'to go to /api/v1/hello-world-23'


@app.route('/api/v1/hello-world-23')
def print_hello_world():
    return 'Hello World 23'


if __name__ == '__main__':
    # app.run(debug=True)
    serve(app, port=5000, host='0.0.0.0')
