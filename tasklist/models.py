from django.db import models


class Tasks(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    assignee = models.CharField(max_length=155)
    created = models.DateTimeField(auto_now_add=True)
    started = models.DateTimeField(null=True)
    completed = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
