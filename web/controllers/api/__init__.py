from flask import Blueprint
route_api = Blueprint('api_page',__name__)
# Member.py中引入了aoute_api需要先定义再引入
from web.controllers.api.submitorder import *
from web.controllers.api.Member import *

@route_api.route("/")
def index():
    return "QueenDekimZ Api V1.0~~"