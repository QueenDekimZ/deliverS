# -*- coding: utf-8 -*-
from flask import Blueprint,g,redirect
from common.libs.Helper import ops_render
from common.libs.UrlManager import UrlManager


route_index = Blueprint( 'index_page',__name__ )

@route_index.route("/")
def index():
    current_user = g.current_user
    # print(g.current_user.nickname)
    # print("+++++++++++++++++++++++++++++++++++++")
    return redirect(UrlManager.buildUrl("/account/index"))
    # return render_template( "index/index.html",current_user=current_user )