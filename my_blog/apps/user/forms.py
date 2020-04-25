from django import forms
from django.contrib.auth import login
from django.db.models import Q

from .models import Userinfo
import re


class LoginForm(forms.Form):

    user_account = forms.CharField()
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={

                                   "min_length": "密码长度大于6",
                                   "max_length": "密码长度小于20",
                                   "required": '密码不能为空',
                               })
    remember = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_user_account(self):
        user_info = self.cleaned_data.get('user_account')
        if not user_info:
            raise forms.ValidationError('用户名不能为空')

        if len(user_info) < 5 or len(user_info) > 20:
            raise forms.ValidationError('参数长度不符合')

        if not re.match(r'^1[3-9]\d{9}$|^\w{5,20}$', user_info):
            raise forms.ValidationError('输入的参数格式错误')
        return user_info

    def clean(self):

        cleaned_data = super().clean()
        user_info = cleaned_data.get('user_account')
        pass_wd = cleaned_data.get('password')
        rmber = cleaned_data.get('remember')

        # 判断是否是用户名，手机号

        user_qs = Userinfo.objects.filter(Q(phone=user_info) | Q(username=user_info))

        if user_qs:
            user_login = user_qs.first()
            user = user_qs.filter(password=pass_wd).count()
            if user == 1:
                if rmber:
                    self.request.session.set_expiry(60*60*24*7)  # None:默认14天
                else:
                    self.request.session.set_expiry(0)

            else:
                raise forms.ValidationError("用户名或密码错误，请重新输入")

            return cleaned_data


