
from django.contrib import admin
from django.urls import path,include
from allauth.account.views import LoginView, SignupView, LogoutView, account_inactive
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from Produk.views import HomeProduk, CheckoutView, KonfirmasiView, tambah_ke_keranjang, keranjang_belanja



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
    path('checkout/<int:produk_id>/', CheckoutView.as_view(), name='checkout'),
    path('konfirmasi/<int:pengiriman_id>/', KonfirmasiView.as_view(), name='konfirmasi'),
    path('tambah_ke_keranjang/', tambah_ke_keranjang, name='tambah_ke_keranjang'),
    path('keranjang_belanja/', keranjang_belanja, name='keranjang_belanja'),




]



