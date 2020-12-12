//index.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {

    region: ['--请', '选', '择--'],

    hideModal: true, //模态框的状态  true-隐藏  false-显示
    animationData: {},
    price: 12,
    //加减框变量
    num: 1,
    minusStatus: 'disable',
    fromaddress:app.globalData.fromaddress,
    total_price: 0,
    remark: '',
    insurance: 0,


  },
  // 备注
  beizhu_input: function (e) {
    this.setData({
      remark: e.detail.value
    })
  },
  // 保价
  baojia_input: function (e) {
    this.setData({
      insurance: e.detail.value * 0.01
    })
    this.setData({
      total_price: this.data.price +  this.data.insurance
    })
  },
  // 显示遮罩层
  showModal: function () {
    var that = this;
    that.setData({
      hideModal: false
    })
    var animation = wx.createAnimation({
      duration: 20, //动画的持续时间   数值越大，动画越慢   数值越小，动画越快
      timingFunction: 'ease', //动画的效果 默认值是linear
    })
    this.animation = animation
    setTimeout(function () {
      that.fadeIn(); //调用显示动画
    }, 200)
  },

  // 隐藏遮罩层
  hideModal: function () {
    var that = this;
    var animation = wx.createAnimation({
      duration: 20, //动画的持续时间   数值越大，动画越慢   数值越小，动画越快
      timingFunction: 'ease', //动画的效果 默认值是linear
    })
    this.animation = animation
    that.fadeDown(); //调用隐藏动画   
    setTimeout(function () {
      that.setData({
        hideModal: true
      })
    }, 200) //先执行下滑动画，再隐藏模块
  },
  //动画集
  fadeIn: function () {
    this.animation.translateY(-55).step()
    this.setData({
      animationData: this.animation.export() //动画实例的export方法导出动画数据传递给组件的animation属性
    })
  },
  fadeDown: function () {
    this.animation.translateY(-55).step()
    this.setData({
      animationData: this.animation.export(),
    })
  },
  //事件处理函数
  /*点击减号*/
  bindMinus: function () {
    var num = this.data.num;
    if (num >= 1) {
      num--;
    }
    var minusStatus = num >= 1 ? 'normal' : 'disable';
    if (minusStatus == 'normal') {
      this.setData({
        num: num,
        minusStatus: minusStatus,
        price: this.data.price - 2,
      });
      this.setData({
        total_price: this.data.price + this.data.insurance
      });
    }

    app.console(this.data.num);
    app.console(this.data.price);


  },
  /*点击加号*/
  bindPlus: function () {
    var num = this.data.num;
    num++;
    var minusStatus = num >= 1 ? 'normal' : 'disable';
    if (minusStatus == 'normal') {
      this.setData({
        num: num,
        minusStatus: minusStatus,
        price: this.data.price + 2,
      })
      this.setData({
        total_price: this.data.price + this.data.insurance
      })
    }
    app.console(this.data.num);
    app.console(this.data.price);

  },
  // 下单处理函数
  submitOrder: function () {
    var that = this;
    app.console(that.data.remark);
    app.console(that.data.insurance);

    wx.request({
      url: app.buildUrl('/submitorder'),
      // 传递form类型数据
      header: app.getRequestHeader(),
      method: 'POST',
      data: {
        price: that.data.price,
        nickname: app.globalData.nickname,
        frommobile: app.globalData.frommobile,
        fromaddress: app.globalData.fromaddress,
        fromname: app.globalData.fromname,
        tomobile: app.globalData.tomobile,
        toaddress: app.globalData.toaddress,
        toname: app.globalData.toname,
        remark: that.data.remark,
        weight: that.data.num,
        insurance: that.data.insurance
      },
      success: function (res) {
        app.console(res);
        if (res.data.code = 200) {
          wx.showModal({
            cancelColor: 'cancelColor',
            title: 'ok',
            content: res.data.data.packageid,
          })

        } else {

          that.goToIndex();
        }
      }
    })
  },
  goToIndex: function () {
    wx.reLaunch({
      url: '/pages/index/index',
    });
  },
  /*输入框事件*/
  // bindManual: function(e) {
  //   var num = e.detail.value;
  //   var minusStatus = num > 1 ? 'normal' : 'disable';

  //   this.setData({
  //     num:num,
  //     minusStatus: minusStatus,
  //     price:12+num*2,
  //   })
  // },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },




})