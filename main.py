from flask import Flask,request,json,Response
import sco_functions

app = Flask(__name__)
#http://blog.luisrei.com/articles/flaskrest.html


@app.route('/board', methods = ['PUT'])
def api_root():
    board = json.dumps(request.json['board']);
    score = json.dumps(request.json['score']);
    score_vs = json.dumps(request.json['score_vs']);
    player = json.dumps(request.json['player']);
    round = json.dumps(request.json['round']);

    valueToReturn = MinMax(board,score,score_vs,player,round)

    js = json.dumps(valueToReturn)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


if __name__ == '__main__':
    app.run()
