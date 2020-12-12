from application import app

'''
统计拦截器
'''
from web.interceptors.AuthInterceptor import *
'''
蓝图功能，对所有url进行蓝图功能配置
'''
from web.controllers.index import route_index
from web.controllers.user.User import route_user
from web.controllers.static import route_static
from web.controllers.account.Account import route_account
from web.controllers.finance.Finance import route_finance
from web.controllers.member.Member import route_member
from web.controllers.stat.Stat import route_stat
#默认访问__init__
from web.controllers.api import route_api

app.register_blueprint(route_index,url_prefix="/")

# 账户登录相关界面
app.register_blueprint(route_user,url_prefix="/user")
# 账户管理相关界面
app.register_blueprint(route_account,url_prefix="/account")
# 会员管理相关界面
app.register_blueprint(route_member,url_prefix="/member")
# 物流管理相关界面
app.register_blueprint(route_finance,url_prefix="/finance")
# # 统计管理相关界面
# app.register_blueprint(route_stat,url_prefix="/stat")

# 加载静态页面
app.register_blueprint(route_static,url_prefix="/static")

# 小程序接口
app.register_blueprint(route_api,url_prefix="/api")