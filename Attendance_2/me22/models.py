from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_fac = models.BooleanField('Is Faculty',default=False)
    def __str__(self):
        return str(self.username)

class att(models.Model):
    id_s = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.id)