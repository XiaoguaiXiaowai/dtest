from django.db import models

# Create your models here.
class Host(models.Model):
    host = models.CharField(max_length=255, verbose_name="名称", unique=True, blank=False)
    ip = models.GenericIPAddressField(verbose_name="IP", blank=False)
    disk = models.TextField(verbose_name="硬盘", null=True, blank=True)
    memory = models.TextField(verbose_name="内存", null=True, blank=True)
    cpu = models.TextField(verbose_name="CPU", null=True, blank=True)
    desc = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.host