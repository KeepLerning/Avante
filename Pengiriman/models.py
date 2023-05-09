from django.db import models

class Pengiriman(models.Model):
    nama_pengiriman = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_pengiriman
