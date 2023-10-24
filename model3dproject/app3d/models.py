from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class Badge(models.Model):
    name = models.CharField(max_length=123, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
    

class CustomUser(AbstractUser):
    badges = models.ManyToManyField(Badge, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def has_badge(self, name):
        return self.badges.filter(name=name).exists()
    
    def is_pioneer(self):
        now = timezone.now()
        one_year_ago = now - timezone.timedelta(days=365)
        return self.date_joined <= one_year_ago


class Model3d(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=123)
    description = models.TextField()
    image = models.ImageField(upload_to="models")
    date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title
    
@receiver(pre_save, sender=Model3d)
def ajouter_badge_collector(sender, instance, **kwargs):
    if not instance.user.has_badge("Collector") and instance.user.model3d_set.count() >= 1:
        badge, _ = Badge.objects.get_or_create(name="Collector", description="Un user a uploadé plus de 5 modèles")
        instance.user.badges.add(badge)