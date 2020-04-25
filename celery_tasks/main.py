 # 创建实例
import os
from celery import Celery

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'my_blog.settings.dev'

# 创建实例
celery_app = Celery('sms_code')

# 加载配置
celery_app.config_from_object("celery_tasks.config")


# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])

# celery -A celery_tasks.main worker -l info