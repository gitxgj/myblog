


$(function () {


    let $username = $('#user_name');
    let $img = $(".form-item .captcha-graph-img img");   // 获取图像
    let sImageCodeId = '';
    let isMobileFlag = false;
    let isUsernameFlag ;
    let send_flag = true;


    // let $imgCodeText = $('#input_captcha');
    // console.log(img);
    genreate();
    $img.click(genreate);
    function genreate() {
		sImageCodeId = generateUUID();
        let imageCodeUrl = '/image_code/' + sImageCodeId + '/';

        $img.attr('src', imageCodeUrl)
    }

     // 生成图片UUID验证码
  function generateUUID() {
    let d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
  }


  // 用户名获取  焦点事件 鼠标离开就会去触发
    $username.blur(fn_check_username);
  function fn_check_username() {
      isUsernameFlag = false;
      let sUsername = $username.val();
      console.log(sUsername);

  if (sUsername===''){
      message.showError("请输入用户名");
      return
  }

   //正则匹配 校验用户名是否合法
  if (!(/^[\u4e00-\u9fa5\w]{5,20}$/).test(sUsername)){
      message.showError("输入5-20位字符的用户");
      return
  }

  //发送ajax请求
  $.ajax({
      url:'/username/'+ sUsername+'/',
      type:'GET',
      dataType: 'json',

  })
    //回调
        .done(function (res){
//{'errno': '0', 'errmsg': '', 'data': {'count': 1, 'username': 'admin'}}
      console.log(res);
      if(res['data']['count']==1){
            message.showError('用户名已存在,请重新输入');
            }
      else{
          message.showInfo('【'+res['data']['username']+'】'+'用户名可以正常使用');
          isUsernameFlag = true;
          send_flag = true ;
      }

      })
        .fail(function () {
            message.showError('服务器超时，请重试!')
        })
  }



    //手机号验证

    let $mobile = $('#mobile');
    $mobile.blur(fn_check_mobile);
    function fn_check_mobile() {
        isMobileFlag = false ;
        let sMobile = $mobile.val();
        if(sMobile===''){
            message.showError('手机号不能为空');
            return
        }

        if(!(/^1[3456789]\d{9}$/).test(sMobile)){
            message.showError('手机号格式错误，请重新输入！');
            return

        }
        $.ajax({
            url:'/mobile/'+sMobile+'/',
            type:'GET',
            dataType:'json',

        })
            .done(function (res) {
                console.log(res);
                if (res.data.count==1){
                    message.showError('手机号已经被注册，请重新输入')
                }
                else{
                    message.showSuccess('可以正常使用');
                    isMobileFlag =true ;
                }

            })

            .fail(function(){
                message.showError('服务器超时，请重试！')
        })


    }


    //短信验证与发送
    let $smsCodeBtn = $('.sms-captcha');  // 获取按钮
    let $imgCodeText = $('#input_captcha');         // 验证码的id值

    $smsCodeBtn.click(function () {
        //参数验证   手机号的验证  图形验证码的值   图形文字   uuid

        if (send_flag){

            send_flag=false;
            if(!isMobileFlag){
            fn_check_mobile();
            return
        }
        let text = $imgCodeText.val();
        if(!text){
            message.showError('请输入图形验证码！');
            return
        }

        if(!sImageCodeId){
            message.showError('图形uuid为空');
            return
        }
        //发送ajax
        let DataParams = {
            'mobile':$mobile.val(),
            'text':text,
            'image_code_id':sImageCodeId,

        };
        $.ajax({
            url:'/sms_code/',
            type:'POST',
            headers:{
                "X-CSRFToken":getCookie('csrftoken')
            },
            data:JSON.stringify(DataParams),      //将json表单转换为字符串
            contentType:'application/json; charset=utf-8',
            dataType:'json',

        })

        //成功与失败回调
            .done(function (res) {
                if (res.errno==="0")
                {
                    message.showSuccess('短信验证码发送成功');

                    //倒计时
                    let num = 60;
                    let t = setInterval(function () {
                        if (num===1){
                            //清除定时器
                            clearInterval();
                            $smsCodeBtn.html('获取短信验证码');
                            send_flag = true;
                        }
                        else{
                            num-=1;
                            $smsCodeBtn.html(num+'秒')

                        }
                    },1000)
                }
                else{
                    message.showError(res.errmsg);
                    send_flag = true;



                }
            })

            .fail(function () {
                message.showError('服务器超时，请重试！')
            })


        }





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



      // 5、注册逻辑

    let $register = $('.form-contain');  // 获取注册表单元素

    $register.submit(function (e) {
    // 阻止默认提交操作
    e.preventDefault();

    // 获取用户输入的内容
    let sUsername = $username.val();  // 获取用户输入的用户名字符串
        // alert(sUsername);

    let sPassword = $("input[name=password]").val();
    // console.log(sPassword);

    let sPasswordRepeat = $("input[name=password_repeat]").val();
    // console.log(sPassword)

    let sMobile = $mobile.val();  // 获取用户输入的手机号码字符串
    let sSmsCode = $("input[name=sms_captcha]").val();

    // 判断用户名是否已注册
    if (!isUsernameFlag) {
        fn_check_username();
      return
    }

    // 判断手机号是否为空，是否已注册
    if (!isMobileFlag) {
        fn_check_mobile();
      return
    }



    // 判断用户输入的密码是否为空
    if ((!sPassword) || (!sPasswordRepeat)) {
      message.showError('密码或确认密码不能为空');
      return
    }

    // const reg = /^(?![^A-Za-z]+$)(?![^0-9]+$)[\x21-x7e]{6,18}$/
    // 以首字母开头，必须包含数字的6-18位
    // 判断用户输入的密码和确认密码长度是否为6-20位
      if (!(/^[0-9A-Za-z]{6,20}$/).test(sPassword)){
         message.showError('请输入6到20位包含数字或者字母的密码');
          return
      }


    // 判断用户输入的密码和确认密码是否一致
    if (sPassword !== sPasswordRepeat) {
      message.showError('密码和确认密码不一致');
      return
    }



    // 判断用户输入的短信验证码是否为6位数字
    if (!(/^\d{6}$/).test(sSmsCode)) {
      message.showError('短信验证码格式不正确，必须为6位数字！');
      return
    }

    // 发起注册请求
    // 1、创建请求参数
    let SdataParams = {
      "username": sUsername,
      "password": sPassword,
      "password_repeat": sPasswordRepeat,
      "mobile": sMobile,
      "sms_code": sSmsCode
    };

    // 2、创建ajax请求
    $.ajax({
      // 请求地址
      url: "/register/",  // url尾部需要添加/
      // 请求方式
      type: "POST",
      data: JSON.stringify(SdataParams),
   headers: {
              // 根据后端开启的CSRFProtect保护，cookie字段名固定为X-CSRFToken
       "X-CSRFToken": getCookie("csrftoken")
       },
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",

    })
      .done(function (res) {
        if (res.errno === "0") {
          // 注册成功
          message.showSuccess(res.errmsg);
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
      });

  });

});