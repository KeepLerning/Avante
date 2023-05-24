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
        context['produk'] = Produk.objects.filter(pk__in=[1, 4, 3, 5]).values('harga_produk', 'deskripsi_produk', 'nama_produk', 'id', 'gambar_produk')
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

    def get_success_url(self):
        pengiriman_id = self.request.session['pengiriman_id']
        return reverse('konfirmasi', args=[pengiriman_id])

class KonfirmasiView(View):
    def get(self, request, pengiriman_id):
        pengiriman = get_object_or_404(Pengiriman, nomor_telepon_pelanggan=pengiriman_id)
        context = {
            'pengiriman': pengiriman,
        }
        return render(request, 'konfirmasi.html', context)

class TambahProdukKeKeranjang(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest('Invalid JSON format')

        produk_id = data['id']
        jumlah = data['jumlah']
        produk = get_object_or_404(Produk, id=produk_id)

        # Cek apakah ada keranjang belanja pada sesi
        keranjang = request.session.get('keranjang', {})

        # Tambahkan produk ke keranjang belanja atau update jumlah produk yang sudah ada
        if produk_id in keranjang:
            keranjang[produk_id]['jumlah'] += jumlah
        else:
            keranjang[produk_id] = {'id': produk_id, 'nama_produk': produk.nama_produk, 'harga_produk': float(produk.harga_produk), 'jumlah_produk': jumlah}

        # Simpan keranjang belanja ke dalam sesi
        request.session['keranjang'] = keranjang

        return redirect('keranjang_belanja')

class KeranjangBelanja(View):
    def get(self, request, *args, **kwargs):
        keranjang = request.session.get('keranjang', {})
        total_harga = 0
        daftar_produk = []

        # Hitung total harga dan daftar produk pada keranjang belanja
        for produk_id, data in keranjang.items():
            subtotal_harga = data['harga_produk'] *data['jumlah_produk']
            total_harga += subtotal_harga
            daftar_produk.append({'id': produk_id, 'nama_produk': data['nama_produk'], 'harga': data['harga_produk'], 'jumlah': data['jumlah_produk'], 'subtotal': subtotal_harga})

                # Kirim daftar produk dan total harga ke template
        context = {'daftar_produk': daftar_produk, 'total_harga': total_harga}
        return render(request, 'keranjang.html', context)



def update_keranjang(request):
    if request.method == 'POST':
        produk_id = request.POST.get('id')
        jumlah = int(request.POST.get('jumlah'))

        # Lakukan validasi dan pemrosesan data sesuai kebutuhan
        # Contoh: Validasi apakah produk_id dan jumlah valid, dan apakah pengguna memiliki akses ke produk tersebut

        # Misalnya, dapatkan objek produk berdasarkan ID
        produk = get_object_or_404(Produk, id=produk_id)

        # Perbarui kuantitas produk dalam keranjang belanja
        # Contoh: keranjang_belanja adalah objek keranjang belanja yang terkait dengan pengguna saat ini
        keranjang_belanja.update_produk_quantity(produk, jumlah)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


def hapus_dari_keranjang(request):
    if request.method == 'POST':
        produk_id = request.POST.get('id')

        # Lakukan validasi dan pemrosesan data sesuai kebutuhan
        # Contoh: Validasi apakah produk_id valid dan apakah pengguna memiliki akses ke produk tersebut

        # Misalnya, dapatkan objek produk berdasarkan ID
        produk = get_object_or_404(Produk, id=produk_id)

        # Hapus produk dari keranjang belanja
        # Contoh: keranjang_belanja adalah objek keranjang belanja yang terkait dengan pengguna saat ini
        keranjang_belanja.remove_produk(produk)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})