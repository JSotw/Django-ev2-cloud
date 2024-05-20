from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SubirDumentoImagen(models.Model):
    documento = models.FileField(upload_to='documents/', null=True)
    imagen = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    user_contact = models.ForeignKey(User, null=False, on_delete=models.CASCADE)


    class Meta:
        db_table = "¨files"
        ordering = ['-created_at']

    