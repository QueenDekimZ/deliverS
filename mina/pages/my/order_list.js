var app = getApp();
Page({
    data: {
        statusType: ["待收货", "已收货"],
        status: ["1", "0"],
        currentType: 0,
        tabClass: ["", ""],
        order_list: []
    },
    //代收货和已完成状态
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.data.currentType = curType;
        this.setData({
            currentType: curType
        });
        app.console(curType);
        this.onShow();
    },
    //点击快递订单细节
    orderDetail: function (e) {
        //获取点击item获取订单号 
        var position = e.currentTarget.dataset.packageid;
        app.console(position);
        //获取item数据，将对象转String 
        // let json = JSON.stringify(posts.postUtilsData[position])
        let json = JSON.stringify(position);
        //跳转传值
        wx.navigateTo({
            // url: '/pages/my/order_info/order_info?dataObject=' + json
            url: '/pages/my/order_info?dataObject=' + json
        })
        // app.console(e.currentTarget.id);
    },

    onShow: function () {
        var that = this;

        this.getPackageList();
    },
    onHide: function () {
        // 生命周期函数--监听页面隐藏

    },
    onUnload: function () {
        // 生命周期函数--监听页面卸载

    },
    onPullDownRefresh: function () {
        // 页面相关事件处理函数--监听用户下拉动作

    },
    onReachBottom: function () {
        // 页面上拉触底事件的处理函数

    },
    getPackageList: function () {
        var that = this;
        var data = {

        };
        wx.request({
            url: app.buildUrl('/mypackage'),
            // 传递form类型数据
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                status: that.data.status[that.data.currentType],
                nickname: app.globalData.nickname,
            },
            success: function (res) {
                app.console(res);
                if (res.data.code = 200) {
                    app.console(res.data.data.packge_order_list);
                    that.setData({
                        order_list: res.data.data.packge_order_list
                    })
                    // app.console(order_list);

                } else {

                    app.console("获取订单失败~");
                }
            }
        })
    }
})