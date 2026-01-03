
# Pizza-Agent: Local MCP-Powered Pizza Ordering System

This is a local, agent-ready pizza ordering backend, exposed via FastAPI, and wrapped it into an MCP server that Claude Desktop can directly reason over and invoke.
It’s a real **agent-compatible system** that uses 2 seperate MCP servers: 

    1.  mcp/delivery_mcp_server.py ( Built with OpenAPI specs)
    2. mcp/pizza_mcp_server.py ( Built the standard FastMCP way)

The project showcases how multiple independent MCP servers, each responsible for a single domain, can be composed by a host LLM (Claude Desktop) to solve a multi-step real-world task.

Instead of building a monolithic AI system, this project follows a modular, protocol-driven architecture where:

Each domain exposes its capabilities via MCP

The LLM acts as an intelligent host and coordinator

Agents collaborate without directly calling each other

The result is a realistic, production-style AI system using local infrastructure.

# What This Project Demonstrates

- A real FastAPI backend with OpenAPI specification
- Automatic OpenAPI → MCP conversion using FastMCP
- A second, independent MCP server for delivery scheduling
- Claude Desktop acting as an MCP host
- Agent-to-Agent reasoning without hardcoded orchestration
- In-memory state management (no database required)
- Deterministic business rules enforced server-side


## Run Locally

Clone the project

```bash
  git clone https://github.com/bumbum2403/Pizza-AI-A2A-MCP-.git
```

Go to the project directory

```bash
  cd Pizza-AI-A2A-MCP-
```

Install dependencies:
If you see an environment.yml file in this repo, run the following command to create a perfectly mirrored environment:

```bash
  conda env create -f environment.yml

```

- Start the FastAPI server

```bash
  uvicorn app.main:app --reload
```

- Start Pizza Delivery MCP server ( Uses the FastAPI server to spin up MCP server)
Check Reference : HERE url(https://gofastmcp.com/integrations/openapi)

```bash
  python3 app/mcp/pizza_mcp_server.py
```


- Start Schedule Delivery MCP server

```bash
  python3 app/mcp/delivery_mcp_server.py
```



## System Architecture

At a high level, the system consists of three layers:
1. Domain APIs (FastAPI / Python)
2. MCP Servers (FastMCP / stdio)
3. MCP Host (Claude Desktop)


```bash
┌──────────────────────────┐
│      Claude Desktop      │
│      (MCP Host)          │
│                          │
│  - Decides which agent   │
│    to call               │           
│  - Translates intent     │        MCP over stdio
│    into tool calls       │-------------
│  - Merges responses      │            |
└───────────┬──────────────┘            |
            │                           |       
            │ MCP over stdio            |   
            │                           |
 ┌──────────▼──────────┐     ┌──────────▼──────────┐
 │ Pizza Ordering MCP  │     │ Delivery MCP Server │
 │ (Auto from OpenAPI) │     │ (Custom MCP Server) │
 │                     │     │                     │
 │ - Menu              │     │ - Slot checking     │
 │ - Order creation    │     │ - Scheduling        │
 │ - Order status      │     │ - Time constraints  │
 └──────────┬──────────┘     └──────────┬──────────┘
            │                           │HTTP + 
            │ HTTP                      │ In-memory
            │                           │
 ┌──────────▼──────────┐     ┌──────────▼──────────┐
 │ FastAPI Application │     │ Delivery Logic      │
 │                     │     │ (Python only)       │
 └─────────────────────┘     └─────────────────────┘
```

### Pizza Ordering API (FastAPI):

The FastAPI server exposes a mock pizza ordering system with the following capabilities:

    1. Fetch available pizza menu

    2. Create pizza orders

    3. Retrieve order status
```bash
GET    /menu/                 → List pizzas
POST   /orders/               → Create an order
GET    /orders/{order_id}     → Get order status
GET    /health                → Health check
```
How It Works

Uses FastAPI with Pydantic models

Stores all data in in-memory dictionaries

Automatically generates an OpenAPI 3.1 specification

No database is required

The OpenAPI schema becomes the contract for MCP conversion.

### How It Is Built

        1. FastMCP loads the OpenAPI spec from /openapi.json
        2. Every API endpoint becomes an MCP Tool
        3. HTTP requests are executed using an internal HTTP client
        4. Transport is stdio, not HTTP

This MCP server does not contain business logic.
It is an adapter layer that exposes the API to AI systems.

## Delivery MCP Server (Custom)


The Delivery MCP server exists to demonstrate Agent-to-Agent collaboration.
It is a completely separate domain with its own logic and constraints.

Capabilities

- Check delivery slot availability
- Schedule deliveries
- Enforce business rules:
- Blackout window: 03:00–07:00
- Minimum lead time: 30 minutes

# Agent-to-Agent (A2A) Flow

When a user asks:

`“Order a small margherita and check if delivery at 2:00 AM is possible”`

Claude Desktop performs the following reasoning:
```
Call Pizza MCP → get menu
|
Call Pizza MCP → create order
|
Call Delivery MCP → check slot
|
Merge responses
|
Ask user for confirmation
|
Call Delivery MCP → schedule delivery
|
Call Pizza MCP → fetch order status
|
Present final result
```
No server directly talks to another server.
All coordination happens at the host level.
Claude Desktop acts as both:

    - MCP Host
    - MCP Client for each server