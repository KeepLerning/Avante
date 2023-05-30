
from django.contrib import admin
from django.urls import path,include
from allauth.account.views import LoginView, SignupView, LogoutView, account_inactive
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from Produk.views import HomeProduk, TambahProdukKeKeranjang, KeranjangBelanja, update_keranjang, hapus_dari_keranjang, CheckoutView 



from . import views


urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.home),
    path('accounts/signup/', SignupView.as_view(template_name='account/signup.html'), name='account_signup'),
    path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/dashboard/', account_inactive, name='account_inactive'),
    # Produk
    path('Produk/', HomeProduk.as_view(), name='HomeProduk'),
    path('tambah_ke_keranjang/', TambahProdukKeKeranjang.as_view(), name='tambah_ke_keranjang'),
    path('keranjang_belanja/', KeranjangBelanja.as_view(), name='keranjang_belanja'),
    path('update_keranjang/', update_keranjang, name='update_keranjang'),
    path('hapus_dari_keranjang/', hapus_dari_keranjang, name='hapus_dari_keranjang'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),




]



