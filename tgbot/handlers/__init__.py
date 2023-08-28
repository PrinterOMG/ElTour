from .commands import register_commands
from .registration import register_registration
from .main_menu import register_main_menu
from .account import register_account
from .other import register_other

register_functions = (
    register_other,
    register_commands,
    register_registration,
    register_main_menu,
    register_account
)
