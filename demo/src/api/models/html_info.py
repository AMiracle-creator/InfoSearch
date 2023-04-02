from django.db import models


class HtmlInfoModel(models.Model):
    href = models.CharField(max_length=512, null=True, blank=True)
    title = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    icon = models.CharField(max_length=512, null=True, blank=True)
    page_number = models.IntegerField(null=True, blank=True)

    @property
    def domen(self):
        return f'{self.href or " "}'.strip('https://').strip('http://')
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "HtmlInfo"