from flask import Blueprint


orders = Blueprint('order', __name__)

from . import routes
