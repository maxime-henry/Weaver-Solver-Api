import os
import requests
from fastapi import FastAPI
from mangum import Mangum
from solver import WeaverSolver


app = FastAPI()
# Set the API endpoint and your API key
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = os.environ["OPENAI_API_KEY"]  # Set the API endpoint and your API key


@app.get("/")
def index():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"status": 200, "message": "Hello Maksk!"}


# function to make a joke using two words and chat gtp
def make_joke(word1, word2):
    model_engine = "gpt-4-1106-preview"
    payload = {
        "model": model_engine,
        "messages": [
            {
                "role": "system",
                f"content": f"Write a small joke or pun usning the words {word1} and {word2}",
            },
        ],
        "max_tokens": 50,
        "n": 1,
        "stop": "?|.",
        "temperature": 0.7,
        "presence_penalty": 0.5,
    }
    raw = requests.post(
        API_ENDPOINT,
        json=payload,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30,
    )
    raw_data = raw.json()
    joke = raw_data["choices"][0]["message"]["content"]
    return joke


from fastapi import FastAPI, Form

app = FastAPI()

# @app.get("/solve")
# async def solve_wordle(start: str = Form(...), end: str = Form(...)):
#     try:
#         solver_instance = WeaverSolver("tmp/weaver_graph.json")
#         result = solver_instance.solve(start, end)
#         nb_mots = len(result)
#         print(result, nb_mots)
#         joke = make_joke(start, end)

#         response_data = {
#             "status": 200,
#             "message": "Success",
#             "result": result,
#             "nb_mots": nb_mots,
#             "joke": joke,
#         }
#     except Exception as e:
#         response_data = {
#             "status": 500,
#             "message": "Internal Server Error",
#             "error_details": str(e),
#         }

#     return response_data


@app.get("/solver/{start}/{end}")
def solver(start: str, end: str):
    try:
        solver_instance = WeaverSolver("tmp/weaver_graph.json")
        result = solver_instance.solve(start, end)
        nb_mots = len(result)
        print(result, nb_mots)
        joke = make_joke(start, end)

        response_data = {
            "status": 200,
            "message": "Success",
            "result": result,
            "nb_mots": nb_mots,
            "joke": joke,
        }
    except Exception as e:
        response_data = {
            "status": 500,
            "message": "Internal Server Error",
            "error_details": str(e),
        }

    return response_data


handler = Mangum(app, lifespan="off")
