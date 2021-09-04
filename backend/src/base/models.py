from django.db import models

class Setting(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=64)
    type = models.CharField(max_length=8)
    criterias = models.TextField(default='[]')

    def __str__(self):
        return self.name