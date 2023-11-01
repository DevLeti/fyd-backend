from django.db import models
from django.contrib.auth.models import AbstractUser,User

class Server(models.Model):
    server_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    server_name = models.CharField(max_length=200)
    server_url = models.CharField(max_length=400)
    server_description = models.CharField(max_length=4000, null=True, blank=True)

class Tag(models.Model):
    server_id = models.ForeignKey(Server, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=100)

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    server_id = models.ForeignKey(Server, on_delete=models.CASCADE)