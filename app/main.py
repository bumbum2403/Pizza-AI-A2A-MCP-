from fastapi import FastAPI
from app.routers import menu, orders
app = FastAPI(
    title="Pizza Ordering API",
    description="Mock Pizza REST API for OpenAPI → MCP conversion",
    version="1.0.0",
)


@app.get("/", tags=["System"])
async def root():
    return {
        "service": "Pizza Ordering API",
        "status": "running",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}


app.include_router(menu.router)
app.include_router(orders.router)





# Try checking the API documentation at /docs or /redoc
# http://127.0.0.1:8000/docs or http://127.0.0.1:8000/openapi.json

# To run the app, use the command:
# uvicorn app.main:app --reload

# This is the API spec we'd wanna use to convert to MCP server that can be used by the Ordering Agent. 