from django.db import models

class Registration(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    checked_in = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name} - {self.phone}"

