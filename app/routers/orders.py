from fastapi import APIRouter, HTTPException
from app.models import OrderCreate, Order
from app.db import ORDERS, MENU_LOOKUP
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=Order)
async def create_order(order: OrderCreate):
    pizza = MENU_LOOKUP.get(order.pizza_id)
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    order_id = str(uuid.uuid4())
    eta = datetime.utcnow() + timedelta(minutes=15)

    new_order = Order(
        order_id=order_id,
        pizza=pizza,
        size=order.size,
        quantity=order.quantity,
        status="preparing",
        estimated_ready_time=eta,
    )

    ORDERS[order_id] = new_order
    return new_order

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
