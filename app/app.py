from fastapi import FastAPI, HTTPException
from mangum import Mangum
from solver import WeaverSolver

app = FastAPI()

@app.get('/')
def index():
    return {'status': 200, 'message': 'Hello Maksk!'}

@app.get('/solver/{start}/{end}')
def solver(start: str, end: str):
    try:
        print(start, end)
        solver_instance = WeaverSolver("tmp/weaver_graph.json")
        result = solver_instance.solve(start, end)
        nb_mots = len(result)
        print(result, nb_mots)

        response_data = {
            'status': 200,
            'message': 'Success',
            'result': result,
            'nb_mots': nb_mots
        }
    except Exception as e:
        response_data = {
            'status': 500,
            'message': 'Internal Server Error',
            'error_details': str(e)
        }

    return response_data

# The following part is for AWS Lambda integration using awsgi
handler = Mangum(app, lifespan="off")