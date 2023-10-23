from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.




class Badge(models.Model):
    name = models.CharField(max_length=123, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
    

class CustomUser(AbstractUser):
    badge = models.ForeignKey(Badge, blank=True, null=True, on_delete=models.SET_NULL)


class Model3d(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=123)
    description = models.TextField()
    image = models.ImageField(upload_to="models")
    date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title