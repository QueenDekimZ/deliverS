# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify,redirect
from common.libs.Helper import ops_render,iPagination,getCurrentDate
from common.models.user import User
from common.libs.UrlManager import UrlManager
from common.libs.user import UserService
from application import app,db
from sqlalchemy import or_

route_account = Blueprint( 'account_page',__name__ )

@route_account.route( "/index" )
def index():
    #返回的json数据
    resp_data = {}
    req = request.values
    page = int( req['p'] ) if ( 'p' in req and req['p'] ) else 1
    query = User.query

    # 混合查找 忽略大小写 找到有相同名字或电话号码片段的记录
    if 'mix_kw' in req:
        rule = or_( User.nickname.ilike( "%{0}%".format( req['mix_kw'] ) ),User.mobile.ilike( "%{0}%".format( req['mix_kw'] ) ) )
        query = query.filter( rule )

    # 查找 状态为'已删除'或者'正常'的记录
    if 'status' in req and int( req['status'] ) > -1:
        query = query.filter( User.status == int( req['status'] ) )

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
    # app.logger.info(request.full_path)   # /account/index?
    # app.logger.info("++++++++++++++++++")
    pages = iPagination( page_params )
    # 当前页第一条记录的下标
    offset = ( page - 1 ) * app.config['PAGE_SIZE']
    # 后一页第一条记录的下标
    limit = app.config['PAGE_SIZE'] * page
    # 当前页的记录按uid递增顺序排列
    list = query.order_by( User.uid.asc() ).all()[ offset:limit ]
    # list = query.order_by( User.uid.desc() ).all()

    resp_data['list'] = list
    resp_data['pages'] = pages

    # 将要搜索的值一直显示在搜索框中
    resp_data['search_con'] = req
    # 记录的状态(正常,已删除)
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render( "account/index.html",resp_data )

@route_account.route( "/info" )
def info():
    resp_data = {}
    # request.args只取get参数
    req = request.args
    # 取uid,默认值为0
    uid = int( req.get('id',0 ))
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect( reback_url )

    # 数据库中不存在,则重定向回列表页面
    info = User.query.filter_by( uid = uid ).first()
    if not info:
        return redirect( reback_url )

    # access_list = AppAccessLog.query.filter_by( uid = uid).order_by(AppAccessLog.id.desc() ).limit(10).all()
    resp_data['info'] = info
    # resp_data['access_list'] = access_list
    return ops_render( "account/info.html",resp_data )

@route_account.route( "/set",methods = [ "GET","POST" ] )
def set():
    # default_pwd = "******"
    # 传递uid值, 数据库有uid则修改账户信息,没有uid则置为0,添加账户信息
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int( req.get( "id",0 ) )
        info = None
        if uid :
            info = User.query.filter_by( uid = uid ).first()
        resp_data['user_info'] = info
        return ops_render( "account/set.html",resp_data )

    resp = { 'code':200,'msg':'账户信息修改成功~~','data':{} }
    req = request.values

    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if nickname is None or len( nickname ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify( resp )

    if mobile is None or len( mobile ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码~~"
        return jsonify( resp )

    if email is None or len( email ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~~"
        return jsonify( resp )

    if login_name is None or len( login_name ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录用户名~~"
        return jsonify( resp )

    if login_pwd is None or len( email ) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录密码~~"
        return jsonify( resp )

    has_in = User.query.filter( User.login_name == login_name,User.uid != id ).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该登录名已存在，请换一个试试~~"
        return jsonify(resp)

    user_info = User.query.filter_by( uid = id ).first()

    if user_info:
        model_user = user_info
    else:
        resp['msg'] = "账户信息添加成功~~"
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.UserService.geneSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    # if login_pwd != default_pwd:
    #     if user_info and user_info.uid == 1:
    #         resp['code'] = -1
    #         resp['msg'] = "不准修改密码和登录用户名~~"
    #         return jsonify(resp)
        # model_user.login_pwd =  UserService.genePwd( login_pwd,model_user.login_salt  )
    model_user.login_pwd = login_pwd
    model_user.updated_time = getCurrentDate()
    db.session.add( model_user )
    db.session.commit()
    return jsonify(resp)

@route_account.route("/ops",methods = [ "POST" ])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id :
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if  act not in [ 'remove','recover' ] :
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在~~"
        return jsonify(resp)

    if act == "remove":
        resp['msg'] = "删除成功~~"
        user_info.status = 0
    elif act == "recover":
        resp['msg'] = "恢复成功~~"
        user_info.status = 1

    if user_info and user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "该用户是管理员，不准操作该账号~~"
        return jsonify(resp)

    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)