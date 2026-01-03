from fastmcp import FastMCP
from datetime import datetime, timedelta
import uuid

mcp = FastMCP("Pizza Delivery MCP Server")

# -------------------------
# In-memory delivery store
# -------------------------
deliveries = {}

# -------------------------
# Configuration
# -------------------------
MIN_LEAD_TIME_MINUTES = 30
BLACKOUT_START_HOUR = 3
BLACKOUT_END_HOUR = 7


# -------------------------
# Internal helpers (NOT tools)
# -------------------------
def _parse_time(time_str: str) -> datetime:
    """
    Parse ISO-8601 datetime string.
    Claude Desktop will usually retry with correct format automatically.
    """
    return datetime.fromisoformat(time_str)


def _is_in_blackout_window(dt: datetime) -> bool:
    return BLACKOUT_START_HOUR <= dt.hour < BLACKOUT_END_HOUR


def _has_min_lead_time(dt: datetime) -> bool:
    return dt >= datetime.now() + timedelta(minutes=MIN_LEAD_TIME_MINUTES)


def _validate_delivery_time(dt: datetime) -> tuple[bool, str]:
    """
    Shared validation logic used by multiple tools.
    """
    if _is_in_blackout_window(dt):
        return False, "Delivery is unavailable between 03:00 and 07:00."

    if not _has_min_lead_time(dt):
        return False, "Requested time does not meet the minimum lead time (30 minutes)."

    return True, "Slot available"


# -------------------------
# MCP Tools
# -------------------------
@mcp.tool()
def check_delivery_slot(requested_time: str) -> dict:
    """
    Check whether a delivery slot is available for the given time.
    """
    try:
        dt = _parse_time(requested_time)
    except ValueError:
        return {
            "available": False,
            "reason": "Invalid datetime format. Use ISO format: YYYY-MM-DDTHH:MM:SS"
        }

    valid, reason = _validate_delivery_time(dt)

    return {
        "available": valid,
        "reason": reason
    }


@mcp.tool()
def schedule_delivery(order_id: str, delivery_time: str) -> dict:
    """
    Schedule a delivery for an order at a given time.
    """
    try:
        dt = _parse_time(delivery_time)
    except ValueError:
        return {
            "scheduled": False,
            "reason": "Invalid datetime format. Use ISO format: YYYY-MM-DDTHH:MM:SS"
        }

    valid, reason = _validate_delivery_time(dt)
    if not valid:
        return {
            "scheduled": False,
            "reason": reason
        }

    delivery_id = f"delivery_{uuid.uuid4().hex[:8]}"

    deliveries[delivery_id] = {
        "order_id": order_id,
        "delivery_time": delivery_time,
        "status": "Scheduled"
    }

    return {
        "scheduled": True,
        "delivery_id": delivery_id,
        "order_id": order_id,
        "delivery_time": delivery_time,
        "status": "Scheduled"
    }


# -------------------------
# Entrypoint
# -------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")


# python3 app/mcp/delivery_mcp_server.py
