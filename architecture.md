# Defense AI Agentic App Architecture

## Overview
This application implements a modular agentic AI workflow for defense/intelligence analysis using LangGraph, AWS Bedrock, and MCP/A2A protocols.

## Core Architecture

```mermaid
graph TD
    A[User Query] --> B[SituationalAnalysis Node]
    B --> C[invoke_model<br/>AWS Bedrock Claude 3]
    C --> D[Awareness Output]
    D --> E[AnomalyDetection Node]
    E --> F[invoke_model<br/>AWS Bedrock Claude 3]
    F --> G[Anomalies List]
    G --> H[ReportGeneration Node]
    H --> I[invoke_model<br/>AWS Bedrock Claude 3]
    I --> J[Final Report]

    K[USE_BEDROCK=true] --> C
    K --> F
    K --> I

    L[USE_BEDROCK=false] --> M[GPT-2 Fallback]
    M --> D
    M --> G
    M --> J
```

## Components

### LangGraph Workflow
- **StateGraph**: Manages the agentic workflow state
- **AgentState**: TypedDict containing query, awareness, anomalies, report
- **Nodes**: Modular processing units connected in sequence

### AI Integration
- **Primary**: AWS Bedrock with Claude 3 Sonnet (us.anthropic.claude-3-sonnet-20240229-v1:0)
- **Fallback**: Local GPT-2 via Transformers (for offline/testing)
- **Configuration**: Controlled by USE_BEDROCK environment variable

### Deployment Options

#### Local Development
```mermaid
graph LR
    A[main.py] --> B[LangGraph App]
    C[fastapi_app.py] --> D[FastAPI Server<br/>Port 8000]
    D --> B
```

#### Cloud Deployment
```mermaid
graph LR
    A[API Gateway] --> B[Lambda Function]
    B --> C[LangGraph Workflow]
    C --> D[AWS Bedrock]
    D --> E[Claude 3 Response]
```

## Data Flow
1. User submits query via API (local or cloud)
2. SituationalAnalysis node analyzes the query for awareness
3. AnomalyDetection node identifies anomalies in awareness data
4. ReportGeneration node creates comprehensive report
5. Results returned as JSON with all intermediate outputs

## Security & Configuration
- AWS Credentials via boto3 (IAM roles in Lambda)
- Environment variables for Bedrock toggle
- MCP/A2A protocols for tool exposure
- CloudFormation for infrastructure as code