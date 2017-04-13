from flask import Flask, request, url_for
from flask import Response
from flask import json
from datetime import timedelta
from flask import make_response, current_app
from functools import update_wrapper
import Start

app = Flask(__name__)
#http://blog.luisrei.com/articles/flaskrest.html
# {
# "board":[["0","1","0"],["0","0","2"],["0","0","0"]],
# "score":"3",
# "score_vs":"2",
# "player":"1",
# "round":"3"
# }

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    basestring = (str, bytes)
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/board/', methods = ['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def api_board():
    print('coucou1')
    board = json.loads(json.dumps(request.json['board']))
    print('coucou2')
    score = json.dumps(request.json['score']);
    print('coucou3')
    score_vs = json.dumps(request.json['score_vs']);
    print('coucou4')
    player = json.dumps(request.json['player']);
    print('coucou5')
    round = json.dumps(request.json['round']);
    print('coucou6')

    launch_ia = Start.Ai(board, score, score_vs, player, round)
    print('coucou7')
    returnSet = launch_ia.MinMax()
    print('coucou8')

    valueToReturn = list(returnSet)
    print('coucou1')
    print(valueToReturn)


    js = json.dumps({"x":valueToReturn[0][0],"y":valueToReturn[0][1]})

    resp = Response(js, status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run()
