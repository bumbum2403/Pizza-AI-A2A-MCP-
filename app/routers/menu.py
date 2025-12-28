from fastapi import APIRouter
from app.models import Pizza

router = APIRouter(prefix="/menu", tags=["Menu"])

MENU = [
    Pizza(
        id="margherita",
        name="Margherita",
        sizes={"small": 199, "medium": 299, "large": 399},
    )
]

@router.get("/", response_model=list[Pizza])
async def get_menu():
    return MENU
