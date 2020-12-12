# -*- coding: utf-8 -*-
import hashlib,requests,random,string,json
from application import  app
import datetime
class PackageService():

    @staticmethod
    def genePackageId( length = 20 ):
        # 订单编号为年月日时分秒14个数字+6位随机数
        format = "%Y%m%d%H%M%S"
        keylist = []
        keylist.extend(datetime.datetime.now().strftime(format))
        random_key = [ random.choice( string.digits ) for i in range( length - 14 ) ]
        keylist.extend(random_key)
        return ( "".join( keylist ) )


