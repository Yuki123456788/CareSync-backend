from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    related_user = models.OneToOneField(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True
    )
