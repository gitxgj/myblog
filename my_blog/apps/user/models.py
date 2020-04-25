from django.db import models
# Create your models here.


class Userinfo(models.Model):
    """
    用户名：    username
    手机号：    phone
    密  码：    password
    是否删除：  is_delete
    """
    username = models.CharField(max_length=20, verbose_name="用户名")
    phone = models.CharField(max_length=20, verbose_name="手机号")
    password = models.CharField(max_length=20, verbose_name="密码")   # 如何对密码进行输入限制，如：必须包含字母，数字，字符
    is_delete = models.BooleanField(default=0, verbose_name="删除数值")


    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户信息'

    def __str__(self):
        return self.username



