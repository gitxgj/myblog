import json
import re
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseForbidden
from my_blog.utils.response_code import res_json, Code, error_map
from .models import Userinfo
from django_redis import get_redis_connection
import logging
from .forms import LoginForm
# from my_blog.utils.captcha.captcha import captcha
from django.views import View

logger = logging.getLogger("django")


# 首页面视图
def demo1(request):
    content = {
        "name": "",
    }
    return render(request, "news/index.html", context=content)


def demo(request, username):
    content = {
        "name": username,
    }
    print(content)
    return render(request, "news/index.html", context=content)


# 注册视图
class RegisterView(View):

    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        js_str = request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(js_str)
        username = dict_data.get('username')
        password = dict_data.get('password')
        password2 = dict_data.get('password_repeat')
        mobile = dict_data.get('mobile')
        sms_code = dict_data.get('sms_code')
        if not all([username,password,password2,mobile,sms_code]):
            return HttpResponseForbidden('请准确填写信息参数')

        # 用户名验证

        if not re.match(r'^[\u4e00-\u9fa5\w]{5,20}$', username):
            return HttpResponseForbidden('用户名输入错误')
        if Userinfo.objects.filter(username=username).count() >0:
            return HttpResponseForbidden('用户名已存在')

        # 密码验证

        if not re.match(r'^[0-9A-Za-z]{6,20}$', password):
            return HttpResponseForbidden('密码输入错误')
        if not password == password2:
            return res_json(errmsg='两次输入的密码不一致')

        # 手机号验证

        if not re.match(r'^1[3456789]\d{9}$', mobile):
            return HttpResponseForbidden('密码输入错误')
        if Userinfo.objects.filter(phone=mobile).count() >0:
            return HttpResponseForbidden(errmsg='手机号已经存在')

        # 验证码
        redis_conn = get_redis_connection('verify_code')
        sms_real_code = redis_conn.get('sms_'+mobile)   # 二进制数据
        if sms_real_code is None:
            return res_json(errno=Code.PARAMERR, errmsg='验证码已经过期')
        redis_conn.delete('sms_{}'.format(mobile))
        redis_conn.delete('sms_flag_{}'.format(mobile))
        if sms_code != sms_real_code.decode():
            return HttpResponseForbidden('验证码错误')

        user = Userinfo.objects.create(username=username, phone=mobile, password=password)

        # 保存连接
        # login(request, user)  # 将用户数据以session形式存储起来
        return res_json(errno=Code.OK, errmsg='注册成功!')


class LoginView(View):

    def get(self, request):

        return render(request, "users/login.html")


    def post(self, request):
        js_str = request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR, errmsg="参数错误")
        dict_data = json.loads(js_str.decode())
        form_check = LoginForm(data=dict_data, request=request)
        if form_check.is_valid():

            return res_json(errno=Code.OK, data=dict_data.get("user_account"))
        else:
            # 失败处理
            msg_list = []
            for i in form_check.errors.get_json_darta().values():
                msg_list.append(i[0].get('message'))
            msg_str = '/'.join(msg_list)

            return res_json(errno=Code.PARAMERR, errmsg=msg_str,)


class ChangePassword(View):

    def get(self, request):

        return render(request, "users/changepassword.html")

    def post(self, request):

        if not request.body:
            return res_json(errno=Code.PARAMERR,errmsg="参数错误")

        dict_data = json.loads(request.body.decode())
        mobile = dict_data.get("mobile")
        oldpwd = dict_data.get("oldpwd")
        newpwd = dict_data.get("newpwd")
        if oldpwd == newpwd:
            return res_json(errno=Code.PARAMERR, errmsg="新密码不能与旧密码相同")
        print("check0")
        user = Userinfo.objects.filter(phone=mobile, password=oldpwd)
        if user.count() >= 1:
                user.update(password=newpwd)
                print("check2")
                return res_json(errno=Code.OK, errmsg="密码修改成功")
        else:

            print("check3")
            return res_json(errno=Code.PARAMERR, errmsg="手机号或密码错误")


# def Image_code(requset, img_id):
#     text, image = captcha.generate_captcha()
#     redis_conn = get_redis_connection('verify_code')
#     # 保存
#     redis_conn.setex('img_{}'.format(img_id).encode('utf8'), 300, text)
#
#     logger.info('图形验证码是：{}'.format(text))
#
#     return HttpResponse(content=image, content_type='image/jpg')
#
#
# # 使用session来存储验证码
# #
# #
# # def Image_code(request, img_id):
# #     text, image = captcha.generate_captcha()
# #     # 保存
# #     request.session['image_code'] = text
# #     request.session.set_expiry(60)
# #     # print(request.session.keys())
# #     # print(request.session.values)
# #     # print(request.session.get('image_code'))    # 获取图形验证码的值
# #     return HttpResponse(content=image, content_type='image/jpg')


