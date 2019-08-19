from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)   #用户名
    password = models.CharField(max_length=256)    #密码
    email = models.EmailField(unique=True)     #注册邮箱
    create_time = models.DateField(auto_now_add=True)   #注册时间

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']  #-降序排列
        verbose_name = '用户'   #User的别名
        verbose_name_plural = '用户'



