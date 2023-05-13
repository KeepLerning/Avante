from django.shortcuts import render, get_object_or_404
from .models import KategoriProduk, Produk
from django.views.generic import TemplateView
from django.views.generic import FormView
from Pengiriman.forms import FormPengiriman
from Pengiriman.models import  Pengiriman
from django.views.generic import View

from django.http import HttpResponse
import json


class HomeProduk(TemplateView):
    template_name = 'Produk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori_produk'] = KategoriProduk.objects.filter(id_kategori=0).values_list('nama_kategori', flat=True)
        context['produk'] = Produk.objects.filter(pk__in=[1,4,3]).values('harga_produk', 'deskripsi_produk', 'nama_produk','id')
        return context


class CheckoutView(FormView):
    template_name = 'checkout.html'
    form_class = FormPengiriman


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produk = get_object_or_404(Produk, pk=self.kwargs['produk_id'])
        context['produk'] = produk
        return context

    def form_valid(self, form):
        produk = get_object_or_404(Produk, pk=self.kwargs['produk_id'])
        pengiriman = form.save(commit=False)
        pengiriman.produk = produk
        pengiriman.save()
        return super().form_valid(form)

    def get_success_url(self, pengiriman_id):
        return reverse('konfirmasi', args=(pengiriman_id,))

    def get_success_url(self):
        pengiriman_id = self.request.session['pengiriman_id']
        return reverse_lazy('konfirmasi', args=[pengiriman_id])


class KonfirmasiView(View):
    def get(self, request, pengiriman_id):
        pengiriman = get_object_or_404(Pengiriman, nomor_telepon_pelanggan=pengiriman_id)
        context = {
            'pengiriman': pengiriman,
        }
        return render(request, 'konfirmasi.html', context)


def tambah_ke_keranjang(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        produk_id = data['produk_id']
        jumlah = data['jumlah']
        produk = Produk.objects.get(id=produk_id)

        # cek apakah ada keranjang belanja pada sesi
        keranjang = request.session.get('keranjang', {})

        # tambahkan produk ke keranjang belanja atau update jumlah produk yang sudah ada
        if produk_id in keranjang:
            keranjang[produk_id]['jumlah'] += jumlah
        else:
            keranjang[produk_id] = {'id': produk_id, 'nama': produk.nama_produk, 'harga': float(produk.harga_produk), 'jumlah': jumlah}

        # simpan keranjang belanja ke dalam sesi
        request.session['keranjang'] = keranjang

        return HttpResponse('Produk berhasil ditambahkan ke keranjang belanja')
    else:
        return HttpResponse('Permintaan tidak valid')

def keranjang_belanja(request):
    keranjang = request.session.get('keranjang', {})
    total_harga = 0
    daftar_produk = []

    # hitung total harga dan daftar produk pada keranjang belanja
    for produk_id, data in keranjang.items():
        subtotal_harga = data['harga'] * data['jumlah']
        total_harga += subtotal_harga
        daftar_produk.append({'id': produk_id, 'nama': data['nama'], 'harga': data['harga'], 'jumlah': data['jumlah'], 'subtotal': subtotal_harga})

    # kirim daftar produk dan total harga ke template
    context = {'daftar_produk': daftar_produk, 'total_harga': total_harga}
    return render(request, 'keranjang.html', context)
