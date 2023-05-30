from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from allauth.account.adapter import DefaultAccountAdapter
from Produk.models import Produk, KategoriProduk
from Pengiriman.forms import FormPengiriman


def home(request):
    context = {
    }
        
    return render(request,'account/home.html',context)


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            return '/home/'
        else:
            return '/accounts/login/'


