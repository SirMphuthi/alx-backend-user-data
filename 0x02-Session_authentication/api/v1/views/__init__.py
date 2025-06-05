#!/usr/bin/env python3
"""
Views Blueprint
"""
from flask import Blueprint

# Create a Blueprint instance for API v1 views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import view modules to register their routes with the blueprint
from api.v1.views.index import *
from api.v1.views.users import *
