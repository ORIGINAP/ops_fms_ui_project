from fastapi import FastAPI

api = FastAPI()

@api.get('/hello')
def hello(name):
    result_str = 'Hello. ' + name

    return result_str