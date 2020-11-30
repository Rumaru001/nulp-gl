from note_maker import app

@app.route('/')
def index():
    return 'Tap <a href=\'/api/v1/hello-world-23\'>here</a> ' \
           'to go to /api/v1/hello-world-23'


@app.route('/api/v1/hello-world-23')
def print_hello_world():
    return 'Hello World 23'