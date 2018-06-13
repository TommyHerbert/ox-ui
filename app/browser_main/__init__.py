from flask import Blueprint

bp = Blueprint('browser_main', __name__)

from app.browser_main import routes

