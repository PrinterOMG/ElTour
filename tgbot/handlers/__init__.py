from .commands import register_commands
from .registration import register_registration
from .main_menu import register_main_menu
from .account import register_account
from .other import register_other
from .author_tour import register_author_tour
from .tour_pickup import register_tour_pickup

register_functions = (
    register_other,
    register_commands,
    register_registration,
    register_main_menu,
    register_account,
    register_author_tour,
    register_tour_pickup
)
