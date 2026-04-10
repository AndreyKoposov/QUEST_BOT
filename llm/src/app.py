from fastapi import FastAPI, Response, Depends

from .engine import AIEngine


app = FastAPI(title='LLM')

@app.get('/chat')
async def chat(text: str,
               engine: AIEngine = Depends(AIEngine.get_engine)):
    answer = await engine.chat(text)
    return Response(answer, status_code=200)

@app.head('/ping')
def ping():
    return Response(status_code=200)
