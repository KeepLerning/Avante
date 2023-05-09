from django.db import models

class Pelanggan(models.Model):
    nama_pelanggan = models.CharField(max_length=100)
    email_pelanggan = models.EmailField()
    password_pelanggan = models.CharField(max_length=100)
    alamat_pelanggan = models.TextField()
    nomor_telepon_pelanggan = models.CharField(max_length=20)

    def __str__(self):
        return self.nama_pelanggan
