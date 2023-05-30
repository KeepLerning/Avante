from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, View
from django.http import JsonResponse, HttpResponseBadRequest
import json
from .models import KategoriProduk, Produk
from Pengiriman.forms import FormPengiriman
from Pengiriman.models import Pengiriman
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class HomeProduk(TemplateView):
    template_name = 'Produk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori_produk'] = KategoriProduk.objects.filter(id_kategori=2).values_list('nama_kategori', flat=True)
        context['produk'] = Produk.objects.filter(pk__in=[3, 5]).values('harga_produk', 'deskripsi_produk', 'nama_produk', 'id', 'gambar_produk')
        return context

class TambahProdukKeKeranjang(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest('Invalid JSON format')

        produk_id = data['id']
        jumlah = data['jumlah']
        produk = get_object_or_404(Produk, id=produk_id)

        keranjang = request.session.get('keranjang', {})
        if produk_id in keranjang:
            keranjang[produk_id]['jumlah_produk'] += jumlah
        else:
            keranjang[produk_id] = {
                'id': produk_id,
                'nama_produk': produk.nama_produk,
                'harga_produk': float(produk.harga_produk),
                'jumlah_produk': jumlah
            }
        request.session['keranjang'] = keranjang

        return redirect('keranjang_belanja')

class KeranjangBelanja(TemplateView):
    template_name = 'keranjang.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keranjang = self.request.session.get('keranjang', {})
        total_harga = 0
        daftar_produk = []

        for produk_id, data in keranjang.items():
            subtotal_harga = data['harga_produk'] * data['jumlah_produk']
            total_harga += subtotal_harga
            daftar_produk.append({
                'id': produk_id,
                'nama_produk': data['nama_produk'],
                'harga': data['harga_produk'],
                'jumlah': data['jumlah_produk'],
                'subtotal': subtotal_harga
            })

        context['daftar_produk'] = daftar_produk
        context['total_harga'] = total_harga
        return context

class CheckoutView(FormView):
    template_name = 'checkout.html'
    form_class = FormPengiriman
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keranjang = self.request.session.get('keranjang', {})
        total_harga = 0
        daftar_produk = []

        for produk_id, data in keranjang.items():
            produk = get_object_or_404(Produk, id=produk_id)
            subtotal_harga = data['harga_produk'] * data['jumlah_produk']
            total_harga += subtotal_harga
            daftar_produk.append({
                'id': produk.id,
                'nama_produk': produk.nama_produk,
                'harga': produk.harga_produk,
                'jumlah': data['jumlah_produk'],
                'subtotal': subtotal_harga,
            })

        context['daftar_produk'] = daftar_produk
        context['total_harga'] = total_harga
        return context

    def form_valid(self, form):
        keranjang = self.request.session.get('keranjang', {})
        total_harga = 0
        daftar_produk = []

        for produk_id, data in keranjang.items():
            produk = get_object_or_404(Produk, id=produk_id)
            subtotal_harga = data['harga_produk'] * data['jumlah_produk']
            total_harga += subtotal_harga
            daftar_produk.append({
                'id': produk.id,
                'nama_produk': produk.nama_produk,
                'harga': produk.harga_produk,
                'jumlah': data['jumlah_produk'],
                'subtotal': subtotal_harga,
            })

        # Simpan data pengiriman
        nama_pelanggan = form.cleaned_data['nama_pelanggan']
        alamat_pengiriman = form.cleaned_data['alamat_pengiriman']
        nomor_telepon_pelanggan = form.cleaned_data['nomor_telepon_pelanggan']
        kota = form.cleaned_data['kota']
        provinsi = form.cleaned_data['provinsi']
        kode_pos = form.cleaned_data['kode_pos']

        # Lakukan pemrosesan pesanan sesuai kebutuhan

        # Clear keranjang belanja
        self.request.session['keranjang'] = {}

        return super().form_valid(form)
def update_keranjang(request):
    if request.method == 'POST':
        produk_id = request.POST.get('id')
        jumlah = int(request.POST.get('jumlah'))

        # Lakukan validasi dan pemrosesan data sesuai kebutuhan
        # Contoh: Validasi apakah produk_id dan jumlah valid, dan apakah pengguna memiliki akses ke produk tersebut

        # Misalnya, dapatkan objek produk berdasarkan ID
        produk = get_object_or_404(Produk, id=produk_id)

        # Cek apakah ada keranjang belanja pada sesi
        keranjang = request.session.get('keranjang', {})

        # Perbarui kuantitas produk dalam keranjang belanja
        if produk_id in keranjang:
            keranjang[produk_id]['jumlah_produk'] = jumlah
        else:
            keranjang[produk_id] = {'id': produk_id, 'nama_produk': produk.nama_produk, 'harga_produk': float(produk.harga_produk), 'jumlah_produk': jumlah}

        # Simpan keranjang belanja ke dalam sesi
        request.session['keranjang'] = keranjang

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def hapus_dari_keranjang(request):
    if request.method == 'POST':
        produk_id = request.POST.get('id')

        # Lakukan validasi dan pemrosesan data sesuai kebutuhan
        # Contoh: Validasi apakah produk_id valid dan apakah pengguna memiliki akses ke produk tersebut

        # Misalnya, dapatkan objek produk berdasarkan ID
        produk = get_object_or_404(Produk, id=produk_id)

        # Cek apakah ada keranjang belanja pada sesi
        keranjang = request.session.get('keranjang', {})

        # Hapus produk dari keranjang belanja
        if produk_id in keranjang:
            del keranjang[produk_id]

        # Simpan keranjang belanja ke dalam sesi
        request.session['keranjang'] = keranjang

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})
