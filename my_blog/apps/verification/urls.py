from django.urls import path,re_path
from . import views


urlpatterns = [

    path('image_code/<uuid:img_id>/', views.Image_code, name="image_code"),

    re_path('username/(?P<username>[\u4e00-\u9fa5\w]{5,20})/', views.CheckUsernameView.as_view(), name='c_username'),
    re_path('mobile/(?P<mobile>1[3-9]\d{9}?)/', views.CheckMobileView.as_view(), name='c_mobile'),
    path('sms_code/', views.SmsCodeView.as_view(), name='c_smscode'),

]