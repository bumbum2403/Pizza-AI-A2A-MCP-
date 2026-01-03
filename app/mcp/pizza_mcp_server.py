from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType
import httpx

client = httpx.AsyncClient(base_url="http://127.0.0.1:8000")

openapi_spec = httpx.get("http://127.0.0.1:8000/openapi.json").json()

route_maps = [
    # Force menu listing to be a TOOL
    RouteMap(
        methods=["GET"],
        pattern=r"^/menu/?$",
        mcp_type=MCPType.TOOL,
        mcp_tags={"menu", "read"}
    ),
]

mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    route_maps=route_maps,
    name="Pizza Ordering MCP Server"
)

if __name__ == "__main__":
    mcp.run()

# To run this MCP server, ensure that the FastAPI pizza ordering backend is running at the specified API_BASE_URL.

# Use the command below to start the MCP server:
# python3 app/mcp/pizza_mcp_server.py
#/Users/shubhamdwivedi/miniconda3/envs/pizza-ai/bin/python3 app/mcp/pizza_mcp_server.py
