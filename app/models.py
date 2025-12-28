from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict


class Pizza(BaseModel):
    id: str = Field(
        ...,
        description="Unique identifier for the pizza (used for ordering)"
    )
    name: str = Field(
        ...,
        description="Human-readable pizza name"
    )
    sizes: Dict[str, int] = Field(
        ...,
        description="Available sizes with price in INR (e.g. {'small': 199})"
    )


class OrderCreate(BaseModel):
    pizza_id: str = Field(
        ...,
        description="ID of the pizza to order (from menu)"
    )
    size: str = Field(
        ...,
        description="Size of the pizza (small / medium / large)"
    )
    quantity: int = Field(
        default=1,
        ge=1,
        description="Number of pizzas to order"
    )


class Order(BaseModel):
    order_id: str = Field(
        ...,
        description="Unique order identifier"
    )
    pizza: Pizza = Field(
        ...,
        description="Pizza that was ordered"
    )
    size: str = Field(
        ...,
        description="Selected pizza size"
    )
    quantity: int = Field(
        ...,
        description="Quantity ordered"
    )
    status: str = Field(
        ...,
        description="Current order status (preparing, ready, delivered)"
    )
    estimated_ready_time: datetime = Field(
        ...,
        description="Estimated time when the pizza will be ready"
    )
