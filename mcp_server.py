from mcp.server.fastmcp import FastMCP
from main import app, AgentState

mcp = FastMCP("DefenseAI")

@mcp.tool()
def analyze_defense(query: str) -> str:
    initial_state = AgentState(query=query, awareness="", anomalies=[], report="")
    result = app.invoke(initial_state)
    return f"Awareness: {result['awareness']}\nAnomalies: {result['anomalies']}\nReport: {result['report']}"

if __name__ == "__main__":
    mcp.run(transport='stdio')