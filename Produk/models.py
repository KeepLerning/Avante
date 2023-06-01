from django.db import models

class KategoriProduk(models.Model):
    id_kategori = models.IntegerField(primary_key=True, default=0)
    nama_kategori = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_kategori


class Produk(models.Model):
    nama_produk = models.CharField(max_length=255)
    harga_produk = models.DecimalField(max_digits=10, decimal_places=2)
    deskripsi_produk = models.TextField()
    gambar_produk = models.ImageField(upload_to='produk/', default='default.png') # Memberikan nilai default untuk kolom gambar_produk
    kategori_produk = models.ForeignKey(KategoriProduk, on_delete=models.CASCADE, default=1)

    
    def __str__(self):
        return self.nama_produk






