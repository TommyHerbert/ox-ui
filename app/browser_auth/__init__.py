from flask import Blueprint

bp = Blueprint('browser_auth', __name__)

from app.browser_auth import routes
