from django.db import models

# Create your models here.
# TODO: User CRUD 구현
class User(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True)
    user_pw = models.CharField(max_length=200)

    # def __str__(self):
    #     return self.user_id + " " + self.user_pw

class Server(models.Model):
    server_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    server_name = models.CharField(max_length=200)
    server_url = models.CharField(max_length=400)

# TODO: Tag CRUD 구현
class Tag(models.Model):
    server_id = models.ForeignKey(Server, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=100)

# TODO: Like CRUD 구현
class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    server_id = models.ForeignKey(Server, on_delete=models.CASCADE)