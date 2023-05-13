from django.db import models
from Produk.models import Produk



class Pengiriman(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE,null=False, default=1)
    nama_pelanggan = models.CharField(max_length=100)
    alamat_pengiriman = models.CharField(max_length=255, default='')
    nomor_telepon_pelanggan = models.CharField(max_length=20, default='')
    kota = models.CharField(max_length=50, default='default_kota_value')
    provinsi = models.CharField(max_length=50, default='Provinsi')
    kode_pos = models.CharField(default='00000', max_length=10)
