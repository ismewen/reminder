from django.db import models


# Create your models here.

class ExceptionRecord(models.Model):
    url = models.CharField(max_length=255, verbose_name="Url")
    traceback = models.TextField(verbose_name="Traceback")
    msg = models.CharField(max_length=255, verbose_name="msg")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    utime = models.DateTimeField(auto_now=True)

    def build_content(self):
        str_format = "domain: {domain}\n" \
                     "msg: {msg}\n" \
                     "traceback: {traceback}"
        return str_format.format(domain=self.url, msg=self.msg, traceback=self.traceback)
