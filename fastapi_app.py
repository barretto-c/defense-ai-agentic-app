from fastapi import FastAPI
from pydantic import BaseModel
from main import app, AgentState

app_api = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app_api.post("/analyze")
def analyze(request: QueryRequest):
    initial_state = AgentState(query=request.query, awareness="", anomalies=[], report="")
    result = app.invoke(initial_state)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_api, host="0.0.0.0", port=8000)