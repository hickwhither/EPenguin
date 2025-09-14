from flask import Blueprint, request
import json

from website import db
from website.models import FreeProblem

bp = Blueprint('updater', __name__, url_prefix='/api')

# @bp.route("/problems")
# def get_problem