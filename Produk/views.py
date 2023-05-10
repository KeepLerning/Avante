from django.shortcuts import render
from .models import KategoriProduk, Produk

def Produk(request):
    kategori_produk = KategoriProduk.objects.all()
    produk = Produk.objects.all()
    context = {
        'kategori_produk': kategori_produk,
        'produk': produk
    }
    return render(request, 'Produk.html', context)