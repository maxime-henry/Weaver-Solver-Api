import awsgi
from flask import Flask, jsonify

from solver import WeaverSolver


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(status=200, message='Hello Maksk!')


@app.route('/solver/<start>/<end>')
def solver(start, end):
    try :
        print(start, end)
        solver = WeaverSolver("tmp/weaver_graph.json")
        result = solver.solve(start, end)
        nb_mots = len(result)
        print(result, nb_mots)
        
        response_data = {
            'status': 200,
            'message': 'Success',
            'result': result,
            'nb_mots': nb_mots
        }
    except:
        response_data =    {
            'status': 500,
            'message': 'Internal Server Error',
        }

    return jsonify(response_data)


def handler(event, context):
    http_method = event.get('httpMethod', 'UNKNOWN_METHOD')

    # Rest of your code...

    return awsgi.response(app, event, context)