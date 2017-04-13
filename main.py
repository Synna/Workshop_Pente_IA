from flask import Flask, request, url_for
from flask import Response
from flask import json
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


@app.route('/board', methods = ['PUT'])
def api_board():
    board = json.dumps(request.json['board'])
    score = json.dumps(request.json['score']);
    score_vs = json.dumps(request.json['score_vs']);
    player = json.dumps(request.json['player']);
    round = json.dumps(request.json['round']);

    launch_ia = Start.Ai(board, score, score_vs, player, round)
    valueToReturn = launch_ia.MinMax()
    print(valueToReturn)

    js = json.dumps(valueToReturn)

    resp = Response(js, status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run()
