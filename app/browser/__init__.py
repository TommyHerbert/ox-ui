from flask import Blueprint

bp = Blueprint('browser', __name__)

from app.browser import routes

