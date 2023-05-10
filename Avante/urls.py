
from django.contrib import admin
from django.urls import path,include
# from Akun.views import user_login
from allauth.account.views import LoginView, SignupView, LogoutView, account_inactive
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from Produk.views import Produk

from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', SignupView.as_view(template_name='account/signup.html'), name='account_signup'),
    path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/dashboard/', account_inactive, name='account_inactive'),
    # Produk
    

]



