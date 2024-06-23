from django.db import models
from .member import Member


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Member, blank=True, related_name="groups")
