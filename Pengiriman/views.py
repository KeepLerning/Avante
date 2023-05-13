from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Pengiriman

class KonfirmasiView(View):
    def get(self, request, nomortelepon_pelanggan):
        pengiriman = get_object_or_404(Pengiriman, nomor_telepon_pelanggan=nomor_telepon_pelanggan)
        context = {
            'pengiriman': pengiriman,
        }
        return render(request, 'konfirmasi.html', context)




