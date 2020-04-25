import random
from django.shortcuts import render,redirect
from django.views import View
from django_redis import get_redis_connection
from my_blog.utils.captcha.captcha import captcha
from django.http import HttpResponse,JsonResponse   # JsonResponse格式的对象返回给ajax，完成回调

from my_blog.utils.response_code import res_json,Code,error_map
from celery_tasks.sms.tasks import send_sms_code
from my_blog.utils.yuntongxun.sms import CCP    # 云通讯的CCP对象包
from user.models import Userinfo
import logging
import json
logger = logging.getLogger("django")

# 图形验证


def Image_code(requset, img_id):
    text, image = captcha.generate_captcha()
    redis_conn = get_redis_connection('verify_code')
    # 保存

    redis_conn.setex('img_{}'.format(img_id).encode('utf8'), 60, text)

    logger.info('图形验证码是：{}'.format(text))

    return HttpResponse(content=image, content_type='image/jpg')


# 用户名验证
class CheckUsernameView(View):
    """
    验证用户名
    route ：username/(?P<username>\w{5,20})/
    :param   username
    """
    def get(self, request, username):

        """
        统计数量 如果用户名重复， 它的数量变为1
        :param username:
        :return: 数量
        """
        count = Userinfo.objects.filter(username=username).count()
        data = {
            'count': count,
            'username': username,

        }
        return res_json(data=data)


# 手机号验证
class CheckMobileView(View):

    def get(self,request, mobile):

        count = Userinfo.objects.filter(phone=mobile).count()
        data = {
            'count': count,
        }
        return res_json(data=data)


class SmsCodeView(View):

    def post(self, request):
        """
        手机号，uuid ，图形验证码
        :param request:
        :return:
        """

        json_str = request.body

        if not json_str:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')    # 4103
        dict_data = json.loads(json_str)
        image_code_client = dict_data.get('text')
        uuid = dict_data.get('image_code_id')
        mobile = dict_data.get('mobile')

        # 参数验证
        if not all([image_code_client, uuid, mobile]):
            print("参数缺失")
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        # 连接数据库
        redis_conn = get_redis_connection('verify_code')

        # 重复发送验证码验证
        send_flag = redis_conn.get('sms_flag_{}'.format(mobile))
        if send_flag:

            return res_json(errno=Code.DATAEXIST, errmsg="短信发送频繁")

        image_code_server = redis_conn.get('img_{}'.format(uuid))

        if image_code_server is None:
            print("没有找到对应验证码")
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])

        # 删除数据库的验证码
        try:
            redis_conn.delete('img_{}'.format(uuid))
        except Exception as e:
            logger.error(e)

        if image_code_client.lower() != image_code_server.lower().decode():
            return res_json(errno=Code.PARAMERR, errmsg='图形验证码输入错误')
        # 生成短信验证码  补全
        sms_code = '%06d' % random.randint(0, 999999)
        # 存到数据库，下一次使用
        redis_conn.setex('sms_{}'.format(mobile), 300, sms_code)

        # 标记手机号在60秒内有发送过短信
        redis_conn.setex('sms_flag_{}'.format(mobile), 60, 1)

        # 模拟发送
        logger.info('发送短信成功[mobile:{}] sms_code:{}]'.format(mobile,  sms_code))

        # 使用云通讯发送
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code,5],1)

        # 使用celery进行短信发送
        # send_sms_code.delay(mobile, sms_code)

        return res_json(errmsg='短信验证码发送成功')



