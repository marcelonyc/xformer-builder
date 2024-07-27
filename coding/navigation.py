from footer import *
from navbar import *
from flask import (
    current_app as server,
)


class NavigationElements:
    def __init__(self):
        self.navbar = create_navbar()
        self.footer = create_footer()
