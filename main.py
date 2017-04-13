from flask import Flask,request, url_for
from flask import Response
from flask import json
import Start

app = Flask(__name__)
#http://blog.luisrei.com/articles/flaskrest.html


@app.route('/board', methods = ['PUT'])
def api_root():
    board = json.dumps(request.json['board']);
    return board
    #score = json.dumps(request.json['score']);
    #score_vs = json.dumps(request.json['score_vs']);
    #player = json.dumps(request.json['player']);
    #round = json.dumps(request.json['round']);
#
    #valueToReturn = Start.MinMax(board,score,score_vs,player,round)
    #print(valueToReturn)
#
    #js = json.dumps(valueToReturn)
#
    #resp = Response(js, status=200, mimetype='application/json')
#
    #return resp


if __name__ == '__main__':
    app.run()
