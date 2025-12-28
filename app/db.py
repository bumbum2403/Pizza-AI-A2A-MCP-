from app.models import Pizza
from app.routers.menu import MENU

ORDERS = {}
MENU_LOOKUP = {pizza.id: pizza for pizza in MENU}
