from fastapi import FastAPI, Request, Response


app = FastAPI(title='AI Service')

@app.get('/chat')
def chat(request: Request):
    pass

@app.head('/ping')
def ping():
    return Response(status_code=200)
