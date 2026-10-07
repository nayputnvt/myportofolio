from django.db import models

# model contact buat nyimpen data kontak di tutorial 6 htmx
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.name
