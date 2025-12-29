import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType


API_BASE_URL = "http://127.0.0.1:8000"


def create_pizza_mcp_server() -> FastMCP:
    # HTTP client that talks to our FastAPI backend
    client = httpx.AsyncClient(base_url=API_BASE_URL)

    # Load OpenAPI spec dynamically
    openapi_spec = httpx.get(f"{API_BASE_URL}/openapi.json").json()

    # Semantic route mapping
    route_maps = [
        # Exclude non-agent routes
        RouteMap(pattern=r"^/$", mcp_type=MCPType.EXCLUDE),
        RouteMap(pattern=r"^/health$", mcp_type=MCPType.EXCLUDE),

        # Menu is a read-only resource
        RouteMap(
            methods=["GET"],
            pattern=r"^/menu/?$",
            mcp_type=MCPType.RESOURCE,
            mcp_tags={"menu", "catalog"}
        ),

        # Order tracking is a parameterized resource
        RouteMap(
            methods=["GET"],
            pattern=r"^/orders/\{.*\}$",
            mcp_type=MCPType.RESOURCE_TEMPLATE,
            mcp_tags={"orders", "tracking"}
        ),

        # Order creation is a tool (state change)
        RouteMap(
            methods=["POST"],
            pattern=r"^/orders/?$",
            mcp_type=MCPType.TOOL,
            mcp_tags={"orders", "mutation"}
        ),
    ]

    return FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name="Pizza Ordering MCP Server",
        route_maps=route_maps,
        tags={"pizza", "ordering", "demo"}
    )


if __name__ == "__main__":
    mcp = create_pizza_mcp_server()
    mcp.run()
# To run this MCP server, ensure that the FastAPI pizza ordering backend is running at the specified API_BASE_URL.

# Use the command below to start the MCP server:
# python3 app/mcp/pizza_mcp_server.py
#/Users/shubhamdwivedi/miniconda3/envs/pizza-ai/bin/python3 app/mcp/pizza_mcp_server.py
