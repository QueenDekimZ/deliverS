//获取应用实例
var app = getApp();
Page({
    data: {},
    onLoad() {

    },
    onShow() {
        let that = this;
        that.setData({
            user_info: {
                nickname: app.globalData.nickname,
                // avatar_url: "https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoYXrcPKhV4R4nCvROibGSk4KzEGCPqW6rlkq0JjkSDU1hINyrHUbVwBFwafQrhTiaA3lnNCFibTy9IQ/132"

                avatar_url:app.globalData.avator,
                mobile:app.globalData.mobile,
            },
        })
    }
});