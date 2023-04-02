from django.contrib.postgres.fields import ArrayField
from django.db import models


class InvertedIndex(models.Model):
    token = models.CharField(max_length=256, null=True, blank=True)
    pages = ArrayField(models.IntegerField(null=True, blank=True), null=True,blank=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name_plural = "InvertedIndex"
