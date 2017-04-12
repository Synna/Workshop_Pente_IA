from flask import Flask, url_for
from flask import request
from flask import json

app = Flask(__name__)
#http://blog.luisrei.com/articles/flaskrest.html


@app.route('/board', methods = ['PUT'])
def api_root():
    if request.headers['Content-Type'] == 'application/json':

        return '{"x":"12","y":"5"}'
    else:
        return 'Pas de JSON'


if __name__ == '__main__':
    app.run()
