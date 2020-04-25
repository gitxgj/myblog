

$(function(){
    let $login = $(".form-contain");


    $login.submit(function(e){
        e.preventDefault();
        let sUsername = $('input[name=telephone]').val();

        if (sUsername ===''){
            message.showError('用户名不能为空！');
            return
        }

        if(!(/^\w{5,20}$/.test(sUsername))){
            message.showError('请输入5-20位字符的用户名');
            return
        }

        //密码验证

        let sPassword = $('input[name=password]').val();
        if (!sPassword){
            message.showError('密码不能为空');
            return
        }

        //验证用户名
        if(sPassword.length<6 ||sPassword.length>20)
        {
            message.showError("密码长度需要在6-20之间");
            return
        }
        let status = $("input[type='checkbox']").is(':checked');


        let sData = {
            'user_account' :sUsername,
            'password' :sPassword,
            'remember':status,

        };
        $.ajax({
            url:'/login/',
            type:'POST',
            data:JSON.stringify(sData),
            contentType:"application/json; charset=utf-8",
            dataType:'json',


        })
            .done(function (res)
            {   if (res.errno==='0') {
                message.showSuccess("贵宾登录，登录成功！");
                setTimeout(function () {
                    window.location.href = '/'+"user"+res.data+"/";
                },1500)
            }   else{
                message.showError(res.errmsg)
                }
            })
            .fail(function () {
                message.showError('访问超时，请重试')

            })



    })


});