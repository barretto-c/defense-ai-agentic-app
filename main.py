import os
from typing import Dict, Any
from langgraph.graph import StateGraph
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

class AgentState(Dict[str, Any]):
    query: str
    awareness: str
    anomalies: list
    report: str

bedrock_client = boto3.client('bedrock-runtime')
use_bedrock = os.getenv('USE_BEDROCK', 'true').lower() == 'true'

def invoke_model(prompt: str) -> str:
    if use_bedrock:
        try:
            response = bedrock_client.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 200,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            result = json.loads(response['body'].read())
            return result['content'][0]['text']
        except Exception as e:
            return f"Error: {e}"
    else:
        from transformers import pipeline
        model = pipeline("text-generation", model="gpt2")
        return model(prompt, max_length=50)[0]['generated_text']

def situational_analysis(state: AgentState) -> AgentState:
    prompt = f"Analyze situational awareness from: {state['query']}"
    state['awareness'] = invoke_model(prompt)
    return state

def anomaly_detection(state: AgentState) -> AgentState:
    prompt = f"Detect anomalies in: {state['query']} and {state['awareness']}"
    response = invoke_model(prompt)
    state['anomalies'] = [line.strip() for line in response.split('\n') if line.strip()]
    return state

def report_generation(state: AgentState) -> AgentState:
    prompt = f"Generate report from awareness: {state['awareness']} and anomalies: {', '.join(state['anomalies'])}"
    state['report'] = invoke_model(prompt)
    return state

graph = StateGraph(AgentState)
graph.add_node("SituationalAnalysis", situational_analysis)
graph.add_node("AnomalyDetection", anomaly_detection)
graph.add_node("ReportGeneration", report_generation)
graph.add_edge("SituationalAnalysis", "AnomalyDetection")
graph.add_edge("AnomalyDetection", "ReportGeneration")
graph.set_entry_point("SituationalAnalysis")
app = graph.compile()

if __name__ == "__main__":
    initial_state = AgentState(query="Analyze battlefield threat", awareness="", anomalies=[], report="")
    result = app.invoke(initial_state)
    print("Result:", result)