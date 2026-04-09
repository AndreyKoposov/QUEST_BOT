from fastapi import FastAPI, Request, Response


app = FastAPI(title='LLM')

@app.get('/chat')
def chat(request: Request):
    pass

@app.head('/ping')
def ping():
    return Response(status_code=200)
