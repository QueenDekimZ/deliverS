DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:727398239809jian@127.0.0.1/deliverS'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = 'utf-8'
SERVER_PORT = 5000

AUTH_COOKIE_NAME = "deliver_auth"

##不需要拦截的url
IGNORE_URLS = [
    "^/user/login",
    "^/api",
]
##不需要验证登录的url
IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico",
]

PAGE_SIZE = 2
PAGE_DISPLAY = 10

# 下拉列表框的状态字典
STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除",
}

# RELEASE_VERSION = "202011252315"

# MINA_APP = {
#     'appid':'wxe206774d80513af3',
#     'appkey':,
# }