//index.js
var app = getApp();
Page({
    data: {
        packageid: "",
        // PACKAGE_INFO:[{
        //     created_time:"",
        //     mobile:"",
        //     nickname:"",
        //     packageid:"",
        //     price:0,
        //     weight:0,
        // }]
        info_flag: false,
        created_time: "",
        nickname: "",
        packageid: "",
        price: '',
        weight: '',
        fromaddress: '',
        fromname: '',
        frommobile: '',
        toaddress: '',
        toname: '',
        tomobile: '',
        remark: '',
    },
    listenerSearchInput: function (e) {
        var val = e.detail.value;
        this.setData({
            packageid: val
        })
    },
    toSearch: function () {
        var that = this;
        var packageid = this.data.packageid;
        app.console(packageid);
        wx.request({
            url: app.buildUrl('/searchorder'),
            // 传递form类型数据
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                packageid: packageid
            },
            success: function (res) {
                app.console(res);
                if (res.data.code = 200) {
                    app.console(res.data.data);
                    let data = res.data.data;
                    that.setData({
                        info_flag: true,
                        created_time: data.created_time,
                        nickname: data.nickname,
                        packageid: data.packageid,
                        price: data.price,
                        weight: data.weight,
                        fromaddress: data.fromaddress,
                        fromname: data.fromname,
                        frommobile: data.frommobile,
                        toaddress: data.toaddress,
                        toname: data.toname,
                        tomobile: data.tomobile,
                        remark: data.remark,
                    });
                    // app.console(that.data.PACKAGE_INFO);
                    // wx.reLaunch({
                    //   url: '/pages/cart/index',
                    //   success: (res) => {},
                    //   fail: (res) => {},
                    //   complete: (res) => {},
                    // });
                }


                // wx.reLaunch({
                //     url: '/pages/cart/index',
                //     success: (res) => {},
                //     fail: (res) => {},
                //     complete: (res) => {},
                //   });
            }
        })
    },


    onLoad: function () {

    },

});