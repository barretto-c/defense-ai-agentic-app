import json
from main import app, AgentState

def lambda_handler(event, context):
    payload = json.loads(event.get('body', '{}'))
    query = payload.get('query', '')
    initial_state = AgentState(query=query, awareness="", anomalies=[], report="")
    result = app.invoke(initial_state)
    return {"statusCode": 200, "body": json.dumps(result)}