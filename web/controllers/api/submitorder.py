# -*- coding: utf-8 -*-
from web.controllers.api import route_api
from  flask import request,jsonify,g
from application import app,db
import requests,json,string,random
from common.models.package import Package
from common.models.member import Member
# from common.models.member.OauthMemberBind import OauthMemberBind
# from common.models.food.WxShareHistory import WxShareHistory
from common.libs.Helper import getCurrentDate,selectFilterObj,getFormatDate
from common.libs.api.PackageService import PackageService

import time
import datetime

@route_api.route("/submitorder", methods = [ "GET","POST" ])
def submitOrder():
    resp = { 'code':200 ,'msg':'下单成功~','data':{} }
    req = request.values
    price = req['price'] if 'price' in req else 0
    fromaddress = req['fromaddress'] if 'fromaddress' in req else ''
    fromname = req['fromname'] if 'fromname' in req else ''
    frommobile = req['frommobile'] if 'frommobile' in req else ''
    toaddress = req['toaddress'] if 'toaddress' in req else ''
    toname = req['toname'] if 'toname' in req else ''
    tomobile = req['tomobile'] if 'tomobile' in req else ''
    weight = req['weight'] if 'weight' in req else 0
    nickname = req['nickname'] if 'nickname' in req else 0
    remark = req['remark'] if 'remark' in req else ''
    insurance = req['insurance'] if 'insurance' in req else ''

    # 订单初始状态为1，即待收货
    status = int(req['status']) if 'status' in req else 1

    # 随机数生成packageid
    packageid = PackageService.genePackageId()
    if Package.query.filter_by(packageid = packageid).first():
        resp['msg'] = "当前系统繁忙，订单生成失败~~"
        resp['code'] = -1
        return jsonify(resp)
    member = Member.query.filter_by(nickname = nickname).first()
    if not member:
        resp['msg'] = "会员账号未创建~~"
        resp['code'] = -1
        return jsonify(resp)
    order_info = Package()
    order_info.packageid = packageid
    order_info.mid = member.id
    order_info.price = price
    order_info.fromaddress = fromaddress
    order_info.fromname = fromname
    order_info.frommobile = frommobile
    order_info.toaddress = toaddress
    order_info.toname = toname
    order_info.tomobile = tomobile
    order_info.weight = weight
    order_info.remark = remark
    order_info.insurance = insurance
    order_info.packageid = PackageService.genePackageId()
    order_info.created_time = getCurrentDate()
    order_info.status = status
    db.session.add(order_info)
    db.session.commit()

    resp['data']['packageid'] = packageid
    return jsonify(resp)

@route_api.route("/searchorder", methods = [ "GET","POST" ])
def searchorder():
    data = {}
    resp = { 'code':200 ,'msg':'查询成功~','data':{} }
    req = request.values
    packageid = req['packageid'] if 'packageid' in req else 0
    print(packageid)
    print(type(packageid))
    order_info = Package.query.filter_by(packageid=packageid).first()
    print(order_info)
    if not order_info:
        resp['msg'] = "您查询的订单编号不存在~~"
        resp['code'] = -1
        return jsonify(resp)
    nickname = Member.query.filter_by(id=order_info.mid).first().nickname
    data['nickname'] = nickname
    data['packageid'] = order_info.packageid
    data['fromaddress'] = order_info.fromaddress
    data['fromname'] = order_info.fromname
    data['frommobile'] = order_info.frommobile
    data['toaddress'] = order_info.toaddress
    data['toname'] = order_info.toname
    data['tomobile'] = order_info.tomobile
    data['weight'] = order_info.weight
    data['price'] = str(float(order_info.price) + (order_info.insurance))
    data['created_time'] = getFormatDate(order_info.created_time)
    data['remark'] = order_info.remark
    data['insurance'] = order_info.insurance

    resp['data'] = data
    return jsonify(resp)

@route_api.route("/mypackage", methods = [ "GET","POST" ])
def mypackage():
    data = {}
    resp = { 'code':200 ,'msg':'订单查询成功~','data':{} }
    req = request.values

    status = int(req['status']) if 'status' in req else 1
    nickname = req['nickname'] if 'nickname' in req else ''
    # nickname对应的id
    mid = Member.query.filter_by(nickname = nickname).first().id
    print("++++++++++++++")
    print(mid)
    # 查询所有当前会员nickname的订单记录
    query = Package.query.filter_by(mid = mid)
    # 待收货
    if status == 1:
        query = query.filter(Package.status == status)
    # 已完成
    elif status == 0:
        query = query.filter(Package.status == status)

    package_list = query.order_by(Package.created_time.desc()).all()
    if package_list:
        package_item_list = {}
        package_ids = selectFilterObj(package_list, "packageid")
        print("+++++++++++++++++++++++++++")
        print(package_ids)
        # from_address_list = selectFilterObj(package_list, "fromaddress")
        # to_address_list = selectFilterObj(package_list, "toaddress")

        # package_item_list = {}
        # for item in package_list:
        #     # print(item.fromaddress)
        #     if item.packageid not in package_item_list:
        #         package_item_list[item.packageid] = []
        #     package_item_list[item.packageid].append({
        #         "packageid":item.packageid,
        #         "fromaddress":item.fromaddress,
        #         "fromname":item.fromname,
        #         "frommobile":item.frommobile,
        #         "toaddress":item.toaddress,
        #         "toname":item.toname,
        #         "tomobile":item.tomobile,
        #         "weight":item.weight,
        #         "price":item.price,
        #         "created_time":item.created_time,
        #         "remark":item.remark
        #     })
        #     # package_return_list.extend()
    package_order_list = []
    for item in package_list:
        # timeArray = time.strptime(item.created_time, '%Y-%m-%d %H:%M:%S.%f')
        tmp_data = {
            "packageid": item.packageid,
            "fromaddress": item.fromaddress,
            "fromname": item.fromname,
            "frommobile": item.frommobile,
            "toaddress": item.toaddress,
            "toname": item.toname,
            "tomobile": item.tomobile,
            "weight": item.weight,
            "price": item.price,
            "insurance": item.insurance,
            "status": item.status,

            "created_time": getFormatDate(item.created_time),
            "remark": item.remark,
            # 计算总价
            "total_price": str(float(item.insurance) + float(item.price))
        }
        package_order_list.append(tmp_data)
    resp['data']['packge_order_list'] = package_order_list
    # print(package_item_list)
    return jsonify(resp)

@route_api.route("/mypackageinfo", methods = [ "GET","POST" ])
def mypackageinfo():
    data = {}
    resp = { 'code':200 ,'msg':'订单查询成功~','data':{} }
    req = request.values
    # 从前端post的数据中取出packageid
    packageid = req['packageid'] if 'packageid' in req else ''

    # 查询所有当前订单编号的记录
    item = Package.query.filter_by(packageid = packageid).first()
    package_order_info = []
    status_desc = ['已收货','待收货']
    # 时间往后推7天，作为预计到达截止时间
    deadline_time = item.created_time + datetime.timedelta(days=7)
    tmp_data = {
        "packageid": item.packageid,
        "fromaddress": item.fromaddress,
        "fromname": item.fromname,
        "frommobile": item.frommobile,
        "toaddress": item.toaddress,
        "toname": item.toname,
        "tomobile": item.tomobile,
        "weight": item.weight,
        "price": item.price,
        "insurance": str(float(item.insurance)),
        "status": item.status,
        "status_desc": status_desc[int(item.status)],
        "created_time": getFormatDate(item.created_time),
        "deadline": getFormatDate(deadline_time),
        "remark": item.remark,
        # 计算总价
        "total_price": str(float(item.insurance) + float(item.price))
    }
    package_order_info.append(tmp_data)
    resp['data']['packge_order_info'] = package_order_info
    print(package_order_info)
    return jsonify(resp)

@route_api.route("/changeMypackageStatus", methods = [ "GET","POST" ])
def changeMypackageStatus():
    data = {}
    resp = { 'code':200 ,'msg':'确认收货成功~','data':{} }
    req = request.values
    try:
        # 从前端post的数据中取出packageid
        packageid = req['packageid'] if 'packageid' in req else ''

        # 查询所有当前订单编号的记录
        item = Package.query.filter_by(packageid = packageid).first()
        item.status = 0
        db.session.add(item)
        db.session.commit()

        return jsonify(resp)
    except:
        resp['msg'] = "确认收货失败~~"
        resp['code'] = -1
        return jsonify(resp)

@route_api.route("/deleteMyOrder", methods = [ "GET","POST" ])
def deleteMyOrder():
    data = {}
    resp = { 'code':200 ,'msg':'订单记录删除成功~','data':{} }
    req = request.values
    try:
        # 从前端post的数据中取出packageid
        packageid = req['packageid'] if 'packageid' in req else ''

        # 删除当前订单编号的记录
        Package.query.filter_by(packageid = packageid).delete()
        db.session.commit()

        return jsonify(resp)
    except:
        resp['msg'] = "删除订单记录失败~~"
        resp['code'] = -1
        return jsonify(resp)
