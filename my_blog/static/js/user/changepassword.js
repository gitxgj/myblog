$(function () {

    let is_flag_mobile = false;
    let is_flag_oldpassword = false;
    let is_flag_newpassword = false;
    //旧密码检查
    let $mobile = $("input[name='telephone']");
     $mobile.blur(F_check_moblie);
         function F_check_moblie (){
        let check_mobile = $mobile.val();
        if(check_mobile === ""){
            message.showError("手机号为空");
        }
        else if (!(/^1[3456789]\d{9}$/).test(check_mobile)) {
            message.showError("请输入正确格式的手机号");
        }
        else{
            is_flag_mobile = true;
            message.showSuccess("手机号"+check_mobile+"可正常使用");
        }
    }
     let $check_old_password = $("#old_pwd");
     $check_old_password.blur(F_check_oldpwd);
     function F_check_oldpwd() {
         let old_pwd = $("#old_pwd").val();
         if(old_pwd===""){
             message.showError("旧密码为空");
         }
         if(!(/^[0-9A-Za-z]{6,20}$/).test(old_pwd)){
             message.showError("请输入正确格式的旧密码");
         }

         else{
             message.showSuccess("旧密码验证通过");
             is_flag_oldpassword = true;
         }

     }
    //新密码检查
    let $check_new_password = $("#new_pwd");
     $check_new_password.blur(F_check_newpwd);
     function F_check_newpwd () {
         let old_pwd = $("#old_pwd").val();
         let new_pwd = $("#new_pwd").val();
         if(new_pwd ===""){
             message.showError("新密码为空");
         }
         if(!(/^[0-9A-Za-z]{6,20}$/).test(new_pwd)){
             message.showError("请输入正确格式的新密码");
         }
         else if (old_pwd === new_pwd){
             message.showError("新旧密码不能相同！");

         }
         else {
             message.showSuccess("新密码验证通过");
            is_flag_newpassword = true;
         }

     }
    //提交检查
    let $change_password = $('.form-contain');
    $change_password.submit(function (e) {
        e.preventDefault();
        let S_mobile = $("#mobile").val();
        let S_oldpwd = $("#old_pwd").val();
        let S_newpwd = $("#new_pwd").val();

        if(!is_flag_mobile){
            F_check_moblie();
            return
        }
        if(!is_flag_oldpassword){
            F_check_oldpwd();
            return
        }
        if (!is_flag_newpassword){
            F_check_newpwd();
            return
        }
        if(!(/^1[3456789]\d{9}$/).test(S_mobile)) {
            message.error("手机号输入有误");
            return
        }
        if(!(/^[0-9A-Za-z]{6,20}$/).test(S_oldpwd)){
            message.error("旧密码输入有误");
            return
        }
        if(!(/^[0-9A-Za-z]{6,20}$/).test(S_newpwd)){
            message.error("新密码输入有误");
            return
        }
        if(S_oldpwd === S_newpwd){
            message.error("新旧密码不能相同！");
            return
        }
        let FORM_information = {
        "mobile" : S_mobile,
        "oldpwd" : S_oldpwd,
        "newpwd" : S_newpwd,
    };
        $.ajax({
            url: "/changepassword/",

            type: "POST",
            data: JSON.stringify(FORM_information),
            headers: {
                    "X-CSRFToken": getCookie("csrftoken")
            },
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            })
        .done(function (res) {
        if (res.errno === "0") {
          // 注册成功
          message.showSuccess(res.errmsg);
          alert("密码修改成功，欢迎进入登录界面！");
           setTimeout(() => {
            // 注册成功之后重定向到主页
            window.location.href = '/login/';
          }, 1500)
        } else {
          // 注册失败，打印错误信息
          message.showError(res.errmsg);
        }
      })
        .fail(function(){
        message.showError('服务器超时，请重试！');
      })




    });

        // get cookie using jQuery
    function getCookie(name) {
    let cookieValue = null;
    // && 都要满足
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          // $.trim() 函数用于去除字符串两端的空白字符。
        let cookie = jQuery.trim(cookies[i]);
        console.log(cookie);

        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));


          break;
        }
      }
    }
    return cookieValue;
  }


});