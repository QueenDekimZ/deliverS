var app = getApp();
Page({
    data: {
        list: [
            {
                date: "",
                order_number: "",
                content: "记得周六发货",
            },
            {
                date: "",
                order_number: "20180701223023001",
                content: "记得周六发货",
            }
        ]
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载

    },
    onShow: function () {
        var that = this;
    }
});
