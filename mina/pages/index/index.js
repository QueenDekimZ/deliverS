//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {},
    regFlag:true,
    nickName: app.getCache("token").split("#")[2], //从token缓存中获取nickname
  },
  goToIndex:function(){
    wx.switchTab({
      url: '/pages/fajian/index',
    });
  },
  onLoad:function(){
    wx.setNavigationBarTitle({
      title: app.globalData.shopName
    })
    this.checkLogin();
  },
  onShow:function(){

  },
  onReady: function(){
    var that = this;
    setTimeout(function(){
      that.setData({
        remind: ''
      });
    }, 1000);
    wx.onAccelerometerChange(function(res) {
      var angle = -(res.x*30).toFixed(1);
      if(angle>14){ angle=14; }
      else if(angle<-14){ angle=-14; }
      if(that.data.angle !== angle){
        that.setData({
          angle: angle
        });
      }
    });
  },
  //检查nickname是否登录过
  checkLogin:function(){
    // app.console((app.getCache("token")));
    // app.console(app.getCache("token").split("#")[2]);
    var that = this;
    wx.login({
      success:function(res) {
        if (!res.code) {
          app.alert({'content':'登陆失败~~'});
          return;
        }
        // data['code'] = res.code;
        app.console(res);
        wx.request({
          url: app.buildUrl('/member/check-reg'),
          // 传递form类型数据
          header: app.getRequestHeader(),
          method: 'POST',
          data: {code:res.code,
            nickName:that.data.nickName},
          success:function(res){
              app.console(res);
              if(res.data.code != 200){
                that.setData({
                  regFlag:false
                });
                app.console(app.globalData.nickname);
                app.console(app.globalData.avator);
                return;
              }
              app.setCache("token",res.data.data.token);
              //获取头像和昵称、电话号码放入全局变量
              app.globalData.nickname = res.data.data.nickname;
              app.globalData.avator = res.data.data.avator;
              app.globalData.mobile = res.data.data.mobile;
              app.console(app.globalData.nickname);
              app.console(app.globalData.avator);
              
              that.goToIndex();
          }
        })
      }
    })
  },
  login:function(e){
    var that = this;
    // app.console(e)
    if(!e.detail.userInfo){
      app.alert({'content':'登陆失败~~'})
    }
    var data = e.detail.userInfo;
    wx.login({
      success (res) {
        if (!res.code) {
          app.alert({'content':'登陆失败~~'});
          return;
        }
        data['code'] = res.code;
        wx.request({
          url: app.buildUrl('/member/login'),
          // 传递form类型数据
          header: app.getRequestHeader(),
          method: 'POST',
          data: data,
          success:function(res){
              app.console(res);
              if(res.data.code!=200){
                app.alert({'content':res.msg});
                return;
              }
              app.setCache("token",res.data.data.token);
              that.goToIndex();
          }
        })
      }
    })

  }
});