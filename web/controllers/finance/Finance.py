# -*- coding: utf-8 -*-
from flask import Blueprint
from common.libs.Helper import ops_render,iPagination,getCurrentDate
from  flask import request,jsonify,g
from application import app,db
import requests,json,string,random
from common.models.package import Package
from common.models.member import Member
from common.libs.UrlManager import UrlManager
from common.libs.api.PackageService import PackageService

route_finance = Blueprint( 'finance_page',__name__ )

@route_finance.route( "/index" )
def index():
    #返回的json数据
    resp_data = {}
    req = request.values
    page = int( req['p'] ) if ( 'p' in req and req['p'] ) else 1
    query = Package.query

    page_params = {
        # 总页数
        'total': query.count(),
        # 每页记录条数
        'page_size':app.config['PAGE_SIZE'],
        # 当前页数
        'page': page,
        # 显示多少页
        'display':app.config['PAGE_DISPLAY'],
        # 每页的url
        'url': request.full_path.replace( "&p={}".format(page),"" )
    }
    pages = iPagination( page_params )
    # 当前页第一条记录的下标
    offset = ( page - 1 ) * app.config['PAGE_SIZE']
    # 后一页第一条记录的下标
    limit = app.config['PAGE_SIZE'] * page
    # 当前页的记录按uid递增顺序排列
    list = query.order_by( Package.packageid.asc() ).all()[ offset:limit ]
    # list = query.order_by( User.uid.desc() ).all()
    # member_info = Member.query.filter_by(Member.)
    resp_data['list'] = list
    resp_data['pages'] = pages
    return ops_render( "finance/index.html", resp_data )

# @route_finance.route( "/pay-info" )
# def payInfo():
#     return ops_render( "finance/pay_info.html" )
#
# @route_finance.route( "/account" )
# def account():
#     return ops_render( "finance/account.html" )
