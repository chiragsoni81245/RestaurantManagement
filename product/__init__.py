from itertools import product
from flask import Blueprint, render_template, abort


products = Blueprint('products', __name__)

from . import routes
