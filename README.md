# Pizza-Agent: Local MCP-Powered Pizza Ordering System

This is a local, agent-ready pizza ordering backend, exposed via FastAPI, and wrapped it into an MCP server that Claude Desktop can directly reason over and invoke.
It’s a real **agent-compatible system**.

##  High-level Architecture

The flow of communication moves from the user interface down to the local state, using the Model Context Protocol (MCP) as the bridge between the LLM and our API code.


```

Claude Desktop (MCP Host + Client)  
│  
│ MCP (stdio)  
▼  
Pizza Ordering MCP Server (FastMCP)  
│  
│ HTTP (httpx)  
▼  
FastAPI Local API (OpenAPI)  
│  
▼  
In-memory state (menu, orders)  

```

## 1️⃣ The Local API: Structure & Exposure

The backend is built with FastAPI to ensure it is robust, typed, and machine-discoverable.

###  What it exposes

The local FastAPI server exposes two primary resource sets:

*   **Menu APIs**
    *   GET /menu: Returns the pizza menu.
    *   _Implementation:_ Backed by an in-memory dictionary. Read-only and deterministic.
*   **Order APIs**
    *   POST /orders: Creates a new pizza order.
    *   _Inputs:_ Accepts pizza ID, size, and quantity.
    *   _Output:_ Generates a unique order ID and stores the order in memory.

###  How it works

By using **FastAPI**, the system leverages:

1.  **Python Type Hints + Pydantic:** For automatic request validation and response schemas.
2.  **OpenAPI (Swagger) Generation:** FastAPI automatically publishes an /openapi.json file.
3.  **Uvicorn:** To spin up the HTTP server.

\[!IMPORTANT\]

This OpenAPI spec is the "contract" that the MCP server consumes to understand how to interact with your code.
We convert the MCP server directly using the OpenAPI specs

##  Conceptual Map: FastAPI → OpenAPI → MCP

Understanding the roles of the host and client is critical to understanding how Claude interacts with your tools.

### The Key Idea

We did **not** build a custom MCP client. Instead, we allowed **Claude Desktop** to act as both the MCP host and the MCP client.

### Implementation Roles

| Role | Entity |
| --- | --- |
| MCP Server | pizza_mcp_server.py (via FastMCP) |
| MCP Client | Claude Desktop (Internal) |
| MCP Host | Claude Desktop |
| API Client (HTTP) | httpx.AsyncClient (inside the MCP server) |

### 🛠️ The Integration Workflow

1.  **FastAPI** produces the OpenAPI specification.
2.  **FastMCP** reads that OpenAPI spec and auto-generates MCP tools/resources.
3.  **FastMCP** runs as an MCP server communicating over stdio.
4.  **Claude Desktop** launches the server and handles tool discovery and invocation.

## ❗ Why no custom MCP Client?

We are leveraging Claude Desktop's native capabilities because it already handles:

*   **Tool Discovery:** Finding what the server can do.
*   **Invocation:** Calling the functions with the correct parameters.
*   **Response Parsing:** Taking the tool output and feeding it back into the LLM context.

_You would only build your own MCP host/client if you required a custom agent runtime, multi-agent orchestration outside of Claude, or a production deployment without the Claude Desktop wrapper._

## 🚀 Getting Started

1.  **Start the Backend:**  
    `uvicorn app.main:app --reload`  
    
2.  Launch the MCP Server:  
    Ensure your claude\_desktop\_config.json points to your
    pizza\_mcp\_server.py.
    
    `python3 app/mcp/pizza_mcp_server.py`
3.  Order Pizza:  
    Ask Claude: "What's on the menu and can I get a large pepperoni?"




## Architecture that we want to build (now)

```
┌──────────────────────────┐
│      A2A Orchestrator    │   ← Agent #0 (Coordinator)
│   (reasoning + routing)  │
└───────────┬──────────────┘
            │
   ┌────────┴─────────┐
   │                  │
┌──▼──────────┐  ┌────▼──────────┐
│ Pizza Agent │  │ Delivery Agent│
│ (Ordering)  │  │ (Scheduling)  │
└────┬────────┘  └────┬──────────┘
     │                 │
┌────▼───────┐  ┌─────▼─────────┐
│ Pizza MCP  │  │ Delivery MCP  │
│ (FastAPI)  │  │ (Time logic)  │
└────────────┘  └───────────────┘
```