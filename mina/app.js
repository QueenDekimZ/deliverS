//app.js
App({
    onLaunch: function () {
    },
    globalData: {
        userInfo: null,
        version: "1.0",
        shopName: "仁爱速运",
        domain:"http://127.0.0.1:5000/api",
        // avator: "https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoYXrcPKhV4R4nCvROibGSk4KzEGCPqW6rlkq0JjkSDU1hINyrHUbVwBFwafQrhTiaA3lnNCFibTy9IQ/132"
        avator:"",
        nickname:"",
        mobile:"",
        fromaddress:'',
        fromname:'',
        frommobile:'',
        toaddress:'',
        toname:'',
        tomobile:'',
    },
    tip:function( params ){
        var that = this;
        var title = params.hasOwnProperty('title')?params['title']:'提示信息';
        var content = params.hasOwnProperty('content')?params['content']:'';
        wx.showModal({
            title: title,
            content: content,
            success: function(res) {

                if ( res.confirm ) {//点击确定
                    if( params.hasOwnProperty('cb_confirm') && typeof( params.cb_confirm ) == "function" ){
                        params.cb_confirm();
                    }
                }else{//点击否
                    if( params.hasOwnProperty('cb_cancel') && typeof( params.cb_cancel ) == "function" ){
                        params.cb_cancel();
                    }
                }
            }
        })
    },
    alert:function( params ){
        var title = params.hasOwnProperty('title')?params['title']:'提示信息';
        var content = params.hasOwnProperty('content')?params['content']:'';
        wx.showModal({
            title: title,
            content: content,
            showCancel:false,
            success: function(res) {
                if (res.confirm) {//用户点击确定
                    if( params.hasOwnProperty('cb_confirm') && typeof( params.cb_confirm ) == "function" ){
                        params.cb_confirm();
                    }
                }else{
                    if( params.hasOwnProperty('cb_cancel') && typeof( params.cb_cancel ) == "function" ){
                        params.cb_cancel();
                    }
                }
            }
        })
    },
    //打上断点就可以不用打印日志
    console:function( msg ){
        console.log( msg);
    },
    getRequestHeader:function(){
        return {
            'content-type': 'application/x-www-form-urlencoded'
        }
    },
    buildUrl:function(path,params){
        var url = this.globalData.domain + path;
        var _paramUrl = "";
        if (params) {
            _paramUrl = Object.keys(params).map(function (k) {
                return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=");
            }).join("&");
            _paramUrl = "?" + _paramUrl;
        }
        return url + _paramUrl;
    },
    getCache:function(key){
        var value = undefined;
        //同步
        try{
            value = wx.getStorageSync(key);
        }catch(e){

        }
        return value;
    },
    setCache:function(key,value){
        //异步
        wx.setStorage({
          data: value,
          key: key,
        })
    },

});