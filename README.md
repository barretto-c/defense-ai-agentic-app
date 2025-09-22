# Defense AI Agentic App

A modular agentic AI app for defense/intelligence analysis using LangGraph, MCP, A2A, AWS Bedrock.

## Features
- Situational Awareness Analysis
- Anomaly Detection
- Report Generation
- MCP Tool Integration
- Public API via AWS Lambda + API Gateway

## Setup
1. Install deps: `pip install -r requirements.txt`
2. Set env vars in `.env`
3. Run locally: `python main.py` or `python fastapi_app.py`
4. Deploy: `aws cloudformation deploy --template-file template.yaml --stack-name defense-ai`

## Usage
- Local API: POST to http://localhost:8000/analyze with {"query": "your text"}
- Public API: Use the URL from CloudFormation outputs
- MCP: `python mcp_server.py`

## Tech Stack
- Python, LangGraph, AWS Bedrock, MCP, FastAPI, CloudFormation