from django.db import models


class QQUser(models.Model):

    user = models.ForeignKey('user.Userinfo', on_delete=models.CASCADE)
    openid = models.CharField(max_length=64, verbose_name="openid")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tb_qq'
        verbose_name = "QQ绑定用户"
        verbose_name_plural = verbose_name






