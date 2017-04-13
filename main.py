from flask import Flask, request, url_for, make_response, current_app, Response, json
from flask_cors import CORS, cross_origin
from datetime import timedelta
from functools import update_wrapper
import Start

app = Flask(__name__)
CORS(app)
#http://blog.luisrei.com/articles/flaskrest.html
# {
# "board":[["0","1","0"],["0","0","2"],["0","0","0"]],
# "score":"3",
# "score_vs":"2",
# "player":"1",
# "round":"3"
# }

@app.route('/board/', methods = ['PUT'])
def api_board():
    board = json.loads(json.dumps(request.json['board']))
    score = json.dumps(request.json['score']);
    score_vs = json.dumps(request.json['score_vs']);
    player = json.dumps(request.json['player']);
    round = json.dumps(request.json['round']);


    launch_ia = Start.Ai(board, score, score_vs, player, round)
    returnSet = launch_ia.MinMax()


    isT = launch_ia.isPosTheirs(0,0)
    isM = launch_ia.isPosMine(0,0)

    print(isT)
    print(isM)

    valueToReturn = list(returnSet)

    js = json.dumps({"x":valueToReturn[0][0],"y":valueToReturn[0][1]})

    resp = Response(js, status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run()
