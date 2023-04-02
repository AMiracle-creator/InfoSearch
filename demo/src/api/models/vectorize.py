from django.contrib.postgres.fields import ArrayField
from django.db import models


class VectorizeModel(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    vector = ArrayField(models.DecimalField(max_digits=22, decimal_places=15, null=True, blank=True), null=True, blank=True)
    page_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Vectors"
