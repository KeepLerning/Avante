from django.db import models
from Produk.models import Produk
from Pelanggan.models import Pelanggan


class Ulasan(models.Model):
    isi_ulasan = models.TextField()
    bintang_ulasan = models.IntegerField()
    Produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)

    def __str__(self):
        return self.isi_ulasan
