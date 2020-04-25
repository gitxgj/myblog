# 实现异步处理短信
from celery_tasks.main import celery_app
from my_blog.utils.yuntongxun.sms import CCP
from user.views import logger

# bind


@celery_app.task(bind=True, name='send_sms_code', retry_backoff=3)
def send_sms_code(self, mobile, sms_code):
    """
    手机号
    短信验证码
    :param self:
    :param mobile:
    :param sms_code:
    :return:
    """
    try:
        send_res = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    except Exception as e:
        logger.error(e)
        # 有异常触发3次
        raise self.retry(exc=e, max_retries=3)
    if send_res != 0:
        raise self.retry(exc=Exception("发送短信失败"), max_retries=3)
    return send_res



