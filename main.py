from flask import Flask, url_for
app = Flask(__name__)
#http://blog.luisrei.com/articles/flaskrest.html


@app.route('/board', methods = ['PUT'])
def api_root():
    return 'Welcome'


if __name__ == '__main__':
    app.run()
