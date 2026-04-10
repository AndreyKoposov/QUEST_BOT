from fastapi import FastAPI, Response


app = FastAPI(title='LLM')

@app.get('/chat')
def chat():
    return Response(status_code=200)

@app.head('/ping')
def ping():
    return Response(status_code=200)
