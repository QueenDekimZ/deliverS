;
var account_index_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;
        // 点击搜素按钮提交form表单
        $(".wrap_search .search").click(function(){
            $(".wrap_search").submit();
        });

        $(".remove").click( function(){
            that.ops( "remove",$(this).attr("data") );
        } );

        $(".recover").click( function(){
            that.ops( "recover",$(this).attr("data") );
        } );
    },
    // 传递两个参数,动作(删除or恢复)和uid
    ops:function( act,id ){
        // callback提示确认函数的回调值
        var callback = {
            'ok':function(){
                $.ajax({
                    url:common_ops.buildUrl( "/account/ops" ),
                    type:'POST',
                    data:{
                        act:act,
                        id:id
                    },
                    dataType:'json',
                    success:function( res ){
                        var callback = null;
                        if( res.code == 200 ){
                            callback = function(){
                                // 本页面刷新
                                window.location.href = window.location.href;
                            }
                        }
                        common_ops.alert( res.msg,callback );
                    }
                });
            },
            'cancel':null
        };
        common_ops.confirm( ( act == "remove" ? "确定删除？":"确定恢复？" ), callback );
    }

};

$(document).ready( function(){
    account_index_ops.init();
} );