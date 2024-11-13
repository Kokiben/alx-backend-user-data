#!/usr/bin/env python3
""" Module for application initialization
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Importing routes from the views modules
from api.v1.views.index import *
from api.v1.views.users import *

# Loading user data from a file
User.load_from_file()
