var app = getApp();
Page({
    data: {
        info: [],
        packageid: '',
    },
    onLoad: function (e) {
        var that = this;
        let item = JSON.parse(e.dataObject);
        app.console("info页面订单号为：");
        app.console(item);
        this.setData({
            packageid: item
        })
    },
    onShow: function () {
        var that = this;
        that.getPackageInfo();
    },
    //根据订单编号获取详细信息
    getPackageInfo: function () {
        var that = this;
        var data = {

        };
        wx.request({
            url: app.buildUrl('/mypackageinfo'),
            // 传递form类型数据
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                packageid: that.data.packageid
            },
            success: function (res) {
                app.console(res);
                if (res.data.code = 200) {
                    app.console(res.data.data);
                    var single_date = res.data.data.packge_order_info[0];
                    that.setData({
                        info: single_date
                    });
                    // app.console(res.data.data.packge_order_info[0].fromaddress);
                } else {
                    app.console("获取订单信息失败~");
                    //   that.goToIndex();
                }
            }
        })
    },
    //确认收货后改变订单状态
    changeStatus: function () {
        var that = this;
        var data = {

        };
        wx.request({
            url: app.buildUrl('/changeMypackageStatus'),
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                packageid: that.data.packageid
            },
            success: function (res) {
                app.console(res);
                if (res.data.code = 200) {
                    app.console(res.data.data);
                    wx.reLaunch({
                        url: '/pages/my/order_list',
                    })
                } else {
                    app.console("确认收货失败~");
                    wx.reLaunch({
                        url: '/pages/my/order_list',
                    })
                }
            }
        })
    },
     //删除订单记录
     deleteOrder: function () {
        var that = this;
        var data = {

        };
        wx.request({
            url: app.buildUrl('/deleteMyOrder'),
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                packageid: that.data.packageid
            },
            success: function (res) {
                app.console(res);
                if (res.data.code = 200) {
                    app.console(res.data.data);
                    wx.reLaunch({
                        url: '/pages/my/order_list',
                    })
                } else {
                    app.console("删除订单失败~");
                    wx.reLaunch({
                        url: '/pages/my/order_list',
                    })
                }
            }
        })
    }
});