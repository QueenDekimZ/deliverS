# -*- coding: utf-8 -*-
from application import app
from flask import request,g,redirect

from common.models.user import ( User )
from common.libs.user.UserService import ( UserService )
from common.libs.UrlManager import ( UrlManager )
# from common.libs.LogService import LogService
import re

'''
调用controllers之前使用拦截器,注解，flask自动解析
'''
@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path
    #
    # 如果是静态文件就不要查询用户信息了
    pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    # if '/api' in path:
    #     return


    user_info = check_login()

    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return
    # 取当前登录用户信息到g对象
    g.current_user = None
    if user_info:
        g.current_user = user_info

    # #加入日志
    # LogService.addAccessLog()
    # pattern = re.compile('%s' % "|".join(ignore_urls))
    # if pattern.match(path):
    #     return

    # 如果登录失败，没取到cookies，重定向到登录界面
    if not user_info :
        return redirect( UrlManager.buildUrl( "/user/login" ) )

    return


'''
判断用户是否已经登录
'''
def check_login():
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None


    # if '/api' in request.path:
    #     app.logger.info(request.path)
    #     auth_cookie = request.headers.get("Authorization")
    #     app.logger.info( request.headers.get("Authorization") )

    if auth_cookie is None:
        return False

    # cookies设置时用#分成两个部分
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    # 账户uid校验
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return False
    if user_info is None:
        return False

    #加密校验
    if auth_info[0] != UserService.geneAuthCode( user_info ):
        return False

    #账户可用校验
    if user_info.status != 1:
        return False

    return user_info